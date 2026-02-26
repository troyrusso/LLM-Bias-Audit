import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.autolayout': True}) # Prevents labels from being cut off

# 1. Load Data
csv_file = "local_experiment_results.csv"
try:
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} trials from {csv_file}")
except FileNotFoundError:
    print(f"❌ Error: Could not find {csv_file}")
    exit()

# --- CLEAN DATA & GROUP HALLUCINATED LABELS ---
df = df[df['Outcome'] != 'error'].copy()
df['Hesitation'] = pd.to_numeric(df['Hesitation'], errors='coerce')
df['Grandma_Ref'] = df['Grandma_Ref'].astype(str).str.lower() == 'true'

# Keyword matching to group Llama 3's hundreds of random outcomes into two buckets
anti_social_keywords = ['kept', 'stole', 'fled', 'left_without', 'denied', 'blamed', 'covered', 'hid', 'ignored', 'escaped']
df['Is_AntiSocial'] = df['Outcome'].astype(str).apply(
    lambda x: any(bad_word in x.lower() for bad_word in anti_social_keywords)
)

# ---------------------------------------------------------
# GRAPH 1: Trait vs. Anti-Social Outcome
# ---------------------------------------------------------
print("Generating Graph 1 (Fixed)...")
plt.figure(figsize=(8, 6))

# Calculate percentage of anti-social behavior by trait
trait_antisocial = df.groupby('Trait')['Is_AntiSocial'].mean() * 100

sns.barplot(x=trait_antisocial.index, y=trait_antisocial.values, palette='viridis')
plt.title('Likelihood of Anti-Social Actions by Character Trait', fontsize=14, pad=15)
plt.ylabel('Percentage of Anti-Social Outcomes (%)', fontsize=12)
plt.xlabel('Assigned Character Trait', fontsize=12)

# Add value labels on top of the bars for clarity
for i, v in enumerate(trait_antisocial.values):
    plt.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontweight='bold')

plt.ylim(0, max(trait_antisocial.values) + 10) 
plt.savefig('trend1_trait_outcomes.png', dpi=300, bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# GRAPH 2: Scenario Difficulty (Hesitation Boxplot)
# ---------------------------------------------------------
print("Generating Graph 2...")
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Scenario', y='Hesitation', palette='colorblind', showmeans=True, 
            meanprops={"marker":"o","markerfacecolor":"white", "markeredgecolor":"black"})
plt.title('AI Moral Deliberation (Hesitation) by Scenario', fontsize=14, pad=15)
plt.ylabel('Hesitation Score (1=Instant, 5=Struggle)', fontsize=12)
plt.xlabel('Scenario Type', fontsize=12)
plt.ylim(0.5, 5.5)
plt.savefig('trend2_scenario_hesitation.png', dpi=300, bbox_inches='tight')
plt.close()


# ---------------------------------------------------------
# GRAPH 3: The "Grandma Hallucination" (Bar Chart)
# ---------------------------------------------------------
print("Generating Graph 3...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Subplot A: By Persona
persona_grandma = df.groupby('Persona')['Grandma_Ref'].mean() * 100
sns.barplot(x=persona_grandma.index, y=persona_grandma.values, ax=axes[0], palette='crest')
axes[0].set_title('Grandma References by Author Persona', fontsize=12)
axes[0].set_ylabel('Percentage of Stories (%)', fontsize=12)

# Subplot B: By Demographic
demo_grandma = df.groupby('Demographic_Group')['Grandma_Ref'].mean() * 100
# Sort for a cleaner chart
demo_grandma = demo_grandma.sort_values(ascending=False)
sns.barplot(x=demo_grandma.index, y=demo_grandma.values, ax=axes[1], palette='magma')
axes[1].set_title('Grandma References by Demographic Group', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)

plt.suptitle('Frequency of Familial Tropes ("Grandma Hallucinations")', fontsize=16)
plt.savefig('trend3_grandma_hallucinations.png', dpi=300, bbox_inches='tight')
plt.close()


# ---------------------------------------------------------
# GRAPH 4: Scenario-Specific Persona Vulnerability (Heatmap)
# ---------------------------------------------------------
print("Generating Graph 4...")
plt.figure(figsize=(9, 6))

# Pivot table: Avg rate of anti-social behavior by Scenario and Persona
heatmap_data = df.pivot_table(index='Persona', columns='Scenario', values='Is_AntiSocial', aggfunc='mean') * 100

sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='Reds', cbar_kws={'label': '% Anti-Social Outcome'})
plt.title('Vulnerability to Anti-Social Outcomes (Persona vs. Scenario)', fontsize=14, pad=15)
plt.ylabel('Author Persona', fontsize=12)
plt.xlabel('Scenario', fontsize=12)
plt.savefig('trend4_vulnerability_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n✅ Success! 4 high-resolution graphs have been saved to the current folder.")