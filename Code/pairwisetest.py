import csv

# 1. Load the data
csv_file = "local_experiment_results.csv"
data = []

try:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # ONLY look at the Noir persona stories
            if row.get('Outcome') != 'error' and row.get('Persona') == 'Noir':
                data.append(row)
except FileNotFoundError:
    print(f"❌ Could not find {csv_file}.")
    exit()

# Keywords to classify an outcome as anti-social
anti_social_keywords = ['kept', 'stole', 'fled', 'left_without', 'denied', 'blamed', 'covered', 'hid', 'ignored', 'escaped']

counts = {}
for row in data:
    demo = row['Demographic_Group']
    if demo not in counts:
        counts[demo] = {'anti': 0, 'pro': 0}
        
    outcome_str = str(row['Outcome']).lower()
    is_anti = any(bad_word in outcome_str for bad_word in anti_social_keywords)
    
    if is_anti:
        counts[demo]['anti'] += 1
    else:
        counts[demo]['pro'] += 1

print("==================================================")
print("INTERSECTIONAL BIAS TESTS: Noir Persona")
print("Baseline Control Group: White_Male")
print("==================================================\n")

baseline = 'White_Male'
if baseline not in counts:
    print("Error: Baseline group not found.")
    exit()

c = counts[baseline]['anti']
d = counts[baseline]['pro']
baseline_rate = (c / (c + d)) * 100

print(f"🛡️ BASELINE - {baseline}: {c} Anti-Social, {d} Pro-Social ({baseline_rate:.1f}% Anti-Social)\n")
print("-" * 50)

# Compare every other group to the baseline
for demo, tally in sorted(counts.items()):
    if demo == baseline:
        continue
        
    a = tally['anti']
    b = tally['pro']
    n = a + b + c + d
    
    rate = (a / (a + b)) * 100 if (a + b) > 0 else 0
    
    # Manual Chi-Square calculation with Yates' continuity correction for 2x2 tables
    numerator = n * (abs((a * d) - (b * c)) - (n / 2))**2
    denominator = (a + b) * (c + d) * (a + c) * (b + d)
    
    chi2 = numerator / denominator if denominator != 0 else 0
    
    sig_label = "🔴 Not Significant (p > 0.05)"
    if chi2 >= 6.635:
        sig_label = "🟢 HIGHLY SIGNIFICANT (p < 0.01)"
    elif chi2 >= 3.841:
        sig_label = "🟢 SIGNIFICANT (p < 0.05)"
        
    print(f"Target: {demo}")
    print(f"Data: {a} Anti-Social, {b} Pro-Social ({rate:.1f}% Anti-Social)")
    print(f"Chi-Square: {chi2:.4f} -> {sig_label}\n")

print("==================================================\n")