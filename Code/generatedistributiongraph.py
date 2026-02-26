import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")

# 1. Load Data
csv_file = "local_experiment_results.csv"
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"❌ Error: Could not find {csv_file}")
    exit()

# Clean data
df = df[df['Outcome'] != 'error'].copy()
df['Hesitation'] = pd.to_numeric(df['Hesitation'], errors='coerce')

# ---------------------------------------------------------
# GRAPH 5: Distribution of Extremes (Stacked Bar Chart)
# ---------------------------------------------------------
print("Generating Hesitation Distribution Graph...")

# Group by Demographic and count the occurrences of each Hesitation Score (1-5)
dist_df = df.groupby(['Demographic_Group', 'Hesitation']).size().unstack(fill_value=0)

# Convert counts to percentages (row percentages sum to 100%)
dist_pct = dist_df.div(dist_df.sum(axis=1), axis=0) * 100

# Plot 100% Stacked Bar Chart
ax = dist_pct.plot(kind='bar', stacked=True, colormap='coolwarm', figsize=(10, 6), edgecolor='black')

plt.title('Distribution of Hesitation Scores by Demographic Group', fontsize=14, pad=15)
plt.ylabel('Percentage of Stories (%)', fontsize=12)
plt.xlabel('Demographic Group', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Format legend
plt.legend(title='Hesitation Score\n(1=Instant, 5=Agony)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.ylim(0, 100)

plt.savefig('fig5_hesitation_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved 'fig5_hesitation_distribution.png'")