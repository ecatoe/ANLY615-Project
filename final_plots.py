# Plotting script for the Data Dominators project 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the merged dataset
df = pd.read_excel("Merged_Data.xlsx")

# Walkability vs Obesity
plt.figure(figsize=(8, 6))
plt.scatter(
    results_df["wtd_avg_walk_index"],
    results_df["Obesity among adults"],
    alpha=0.6
)
plt.xlabel("Weighted Walkability Index")
plt.ylabel("Obesity (%)")
plt.title("Walkability vs. Obesity in Texas Counties")
plt.grid(True)
plt.show()

# Food Insecurity vs Obesity
plt.figure(figsize=(8, 6))
plt.scatter(df["Food insecurity in the past 12 months among adults"], 
            df["Obesity among adults"], 
            alpha=0.6)
plt.xlabel("Food Insecurity (%)")
plt.ylabel("Obesity (%)")
plt.title("Food Insecurity vs Obesity")
plt.grid(True)
plt.show()

# Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    results_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Matrix for Walkability, Food Access, and Health Measures")
plt.show()
