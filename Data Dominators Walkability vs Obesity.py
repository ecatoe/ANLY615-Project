# Data Dominators - Walkability vs Obesity
# ANLY 615 Final Project
# Suad Castellanos, Ethan Catoe, Mychael Haywood, Tejas Perwala

# PREREQUISITE FILES:
#   EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv
#   COUNTYFP_TX.csv
#   PLACES__Local_Data_for_Better_Health,_County_Data_2024_release_20251119.xlsx

import pandas as pd

# ====================================================================================================================== #
#                                                  DATA CLEANING                                                         #
# ====================================================================================================================== #

# --------- Ethan's Section --------- #
# filtering walkability dataset down to Texas (state 48)
walk_path = "EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv"
print("="*10, f"Importing {walk_path}", "="*10)
walk_df = pd.read_csv(walk_path)
print("Filtering data down to Texas (FIP code 48000)")
walk_tx_df = walk_df[walk_df['STATEFP'] == 48]
walk_tx_df.to_csv('WalkabilityTX.csv', index=False)

# Importing and joining county name data on to walkability data
print("Merging Texas county FIP codes with county names.")
county_fp_df = pd.read_csv("COUNTYFP_TX.csv")
merged_df = walk_tx_df.merge(county_fp_df, how='left')

# Defining new columns with calculations done to collapse region data into single rows of county data
def condense_function(df):
    new_df = pd.Series({
        'COUNTY_POP': df['TotPop'].sum(), # Total population of county
        'COUNTY_EMP': df['TotEmp'].sum(), # Total employed population of county
        'total_low_wage_emp': df['E_LowWageWk'].sum(),
        'total_med_wage_emp': df['E_MedWageWk'].sum(),
        'total_hi_wage_emp': df['E_HiWageWk'].sum(),
        'pct_low_wage_emp': df['E_LowWageWk'].sum() / df['TotEmp'].sum(),
        'pct_med_wage_emp': df['E_MedWageWk'].sum() / df['TotEmp'].sum(),
        'pct_hi_wage_emp': df['E_HiWageWk'].sum() / df['TotEmp'].sum(),
        'COUNTY_WRK': df['Workers'].sum(), # Total worker population of county
        'total_low_wage_wrk': df['R_LowWageWk'].sum(),
        'total_med_wage_wrk': df['R_MedWageWk'].sum(),
        'total_hi_wage_wrk': df['R_HiWageWk'].sum(),
        'pct_low_wage_wrk': df['R_LowWageWk'].sum() / df['Workers'].sum(),
        'pct_med_wage_wrk': df['R_MedWageWk'].sum() / df['Workers'].sum(),
        'pct_hi_wage_wrk': df['R_HiWageWk'].sum() / df['Workers'].sum(),
        'HH_total': df['HH'].sum(), # total number of households in county
        'total_0_autos': df['AutoOwn0'].sum(), # number of households with 0 vehicles
        'total_1_autos': df['AutoOwn1'].sum(), # number of households with 1 vehicles
        'total_2_autos': df['AutoOwn2p'].sum(), # number of households with 2 or more vehicles
        '0_autos_pct': df['AutoOwn0'].sum() / df['HH'].sum(), # percentage of households with 0 vehicles
        '1_autos_pct': df['AutoOwn1'].sum() / df['HH'].sum(), # percentage of households with 1 vehicles
        '2_autos_pct': df['AutoOwn2p'].sum() / df['HH'].sum(), # percentage of households with 2 or more vehicles
        'wtd_WrkAge_pop_pct': (df['P_WrkAge'] * df['TotPop']).sum() / df['TotPop'].sum(), # percentage of working age people in population
        'wtd_avg_walk_index': (df['NatWalkInd'] * df['TotPop']).sum() / df['TotPop'].sum() # average walkability index weighted by region population in county
    })
    return new_df
new_walk_tx_df = merged_df.groupby(['Texas County']).apply(condense_function).reset_index()

# Exporting condensed dataset to view and verify
print("Dataset cleaned.")
output_file = "Walkability_County_Condensed.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    new_walk_tx_df.to_excel(writer, sheet_name='Walkability_Condensed', index=False)
print("="*10, f"Exported to {output_file}", "="*10)

# --------- Tejas' Section --------- # 
# Load File
# df = pd.read_excel("Texas_df.xlsx")
health_path = "PLACES__Local_Data_for_Better_Health,_County_Data_2024_release_20251119.xlsx"
print("="*10, f"Importing {health_path}", "="*10)
df = pd.read_excel(health_path)
print("Filtering data down to Texas.")
df = df[df["StateAbbr"] == "TX"]

# Drop Columns
drop_cols = [
    "DataSource",
    "Data_Value_Footnote_Symbol",
    "Data_Value_Footnote",
    "CategoryID",
    "Geolocation",
    "Data_Value_Unit"
]

df = df.drop(columns=[c for c in drop_cols if c in df.columns])
df = df.drop_duplicates()

measures_to_keep = [
    "Obesity among adults",
    "Food insecurity in the past 12 months among adults",
    "No leisure-time physical activity among adults"
]

df = df[df["Measure"].isin(measures_to_keep)]

# Pivot Table
df_counties = df.pivot_table(
    index=["LocationName", "TotalPopulation", "TotalPop18plus"],
    columns="Measure",
    values="Data_Value",
    aggfunc="mean"
).reset_index()

# Round Numbers 
measure_cols = [
    "Obesity among adults",
    "Food insecurity in the past 12 months among adults",
    "No leisure-time physical activity among adults"
]

for col in measure_cols:
    df_counties[col] = pd.to_numeric(df_counties[col], errors="coerce").round(1)

# Rename LocationName
df_counties = df_counties.rename(columns={
    "LocationName": "Texas County"
})

# Save Clean Data
df_counties.to_excel("df_tx_counties_health.xlsx", index=False)

print("Cleaned file written to df_tx_counties_health.xlsx")

# ====================================================================================================================== #
#                                                  MERGE DATASETS                                                        #
# ====================================================================================================================== #
# --------- Mychael/Group Section --------- # 
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
county_health_df = pd.read_excel('df_tx_counties_health.xlsx', sheet_name='Sheet1')
walkability_df = pd.read_excel('Walkability_County_Condensed.xlsx', sheet_name='Walkability_Condensed')

merged_df = county_health_df.merge (walkability_df, how='left')
print (merged_df.head)
merged_df.to_excel('Merged_Data.xlsx', index=False)

engine = create_engine('sqlite:///my_database.db')
merged_df.to_sql('Merged_Main', con=engine, if_exists='replace', index=False)
query = """
    SELECT
        "TotalPopulation", "TotalPop18plus", "Food insecurity in the past 12 months among adults", 
        "No leisure-time physical activity among adults", "Obesity among adults", "pct_low_wage_emp",
        "pct_med_wage_emp", "pct_hi_wage_emp", "pct_low_wage_wrk", "pct_med_wage_wrk", "pct_hi_wage_wrk",
        "HH_total", "0_autos_pct", "1_autos_pct", "2_autos_pct", "wtd_WrkAge_pop_pct", "wtd_avg_walk_index"
    FROM
        Merged_Main;
"""
results_df = pd.read_sql(query, engine) 
print(results_df.head)
print(results_df.describe(include='all'))

# ====================================================================================================================== #
#                                                      ANALYSIS                                                          #
# ====================================================================================================================== #
# --------- PCA - Ethan --------- # 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler    # pip install scikit-learn
from sklearn.decomposition import PCA

df = results_df.copy()

X = df.drop(columns=["Obesity among adults", "TotalPopulation", "TotalPop18plus", "HH_total"])
y = df["Obesity among adults"]

# Data Normalization
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Run PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

print("\nPercentages of explained variance (Scree Plot Data):")
print(np.round(pca.explained_variance_ratio_, 4))

loadings = pd.DataFrame(
    pca.components_,
    columns=X.columns,
    index=[f"PC{i+1}" for i in range(len(X.columns))]
)

pca_df = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(X_pca.shape[1])])
pca_df['Obesity'] = y.values

corr = pca_df.corr()['Obesity'].sort_values(ascending=False)
print("\nCorrelation of Principal Components with Obesity:")
print(corr)

# Getting loadings for PC1 & PC2
loadings = pca.components_.T[:, 0:2]

plt.figure(figsize=(10,8))

# PCA Biplot
plt.scatter(pca_df["PC1"], pca_df["PC2"], alpha=0.4)
for i, var in enumerate(X.columns):
    plt.arrow(0, 0, loadings[i,0]*5, loadings[i,1]*5,
              head_width=0.05, color='red')
    plt.text(loadings[i,0]*5*1.1, loadings[i,1]*5*1.1, var,
             color='darkred', fontsize=9)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Biplot")
plt.grid(True)
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.show()

# --------- PCR - Tejas --------- # 

# PCR ANALYSIS
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# Load Merged DF
Merged_Data = pd.read_excel(
    r"C:/Users/tejas/Downloads/Merged_Data.xlsx",
    sheet_name="Sheet1"
)

# Walkability predictor
walkability_cols = [
    "pct_low_wage_emp", "pct_med_wage_emp", "pct_hi_wage_emp",
    "pct_low_wage_wrk", "pct_med_wage_wrk", "pct_hi_wage_wrk",
    "0_autos_pct", "1_autos_pct", "2_autos_pct",
    "wtd_WrkAge_pop_pct", "wtd_avg_walk_index"
]

# Data Cleaning
df = Merged_Data[walkability_cols + ["Obesity among adults"]].copy()

df["Obesity_clean"] = (
    df["Obesity among adults"]
      .astype(str)        # ensure string
      .str.strip()        # remove spaces
      .str.rstrip("%")    # drop % sign if present
)

df["Obesity_clean"] = pd.to_numeric(df["Obesity_clean"], errors="coerce")
df = df.dropna(subset=walkability_cols + ["Obesity_clean"])

X = df[walkability_cols]
y = df["Obesity_clean"]     

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA Analysis

n_components = min(5, X_scaled.shape[1])
pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X_scaled)

print("Explained variance for selected components:")
for i, ev in enumerate(pca.explained_variance_ratio_):
    print(f"PC{i+1}: {ev:.4f}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_pca, y, test_size=0.2, random_state=42
)

# Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("\nPCR Model Results:")
print(f"R-squared: {r2:.4f}")
print(f"MSE: {mse:.4f}")

pc_names = [f"PC{i+1}" for i in range(n_components)]
coeffs = pd.Series(model.coef_, index=pc_names)

print("\nRegression coefficients on PCs:")
print(coeffs)

loading_matrix = pd.DataFrame(
    pca.components_.T,          # predictors x components
    index=walkability_cols,
    columns=pc_names
)

contrib = loading_matrix.mul(coeffs.values, axis=1).sum(axis=1)
contrib = contrib.sort_values(ascending=False)

print("\nFeature contributions to Obesity (PCR interpretation):")
print(contrib)

# --------- Regression Anaylsis - Mychael --------- #

import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression

for col in walkability_cols:
    plt.figure()
    sns.regplot(x=df[col], y=df["Obesity_clean"], scatter_kws={"alpha":0.5})
    plt.xlabel(col)
    plt.ylabel("Obesity_clean")
    plt.title(f"{col} vs Obesity")
    plt.show()

X_pca_3 = pca.fit_transform(X_scaled)[:, :3]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(X_pca_3[:,0], X_pca_3[:,1], X_pca_3[:,2],
                c=df["Obesity_clean"], cmap="viridis")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
fig.colorbar(sc, label="Obesity_clean")
plt.show()

x_var="pct_low_wage_emp"
y_var="pct_med_wage_emp"

x_grid =np.linspace(df[x_var].min(), df[x_var].max(), 30)
y_grid =np.linspace(df[y_var].min(), df[y_var].max(), 30)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

base = df[walkability_cols].mean() #this averages all of the predictors
grid_df = pd.DataFrame({
    col: base[col] for col in walkability_cols
})
grid_df[x_var] = X_grid.ravel()
grid_df[y_var] = Y_grid.ravel()

grid_scaled = scaler.transform(grid_df)
grid_pca = pca.transform(grid_scaled)
y_grid_pred = model.predict(grid_pca).reshape(X_grid.shape)

#Plotting#

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_grid, Y_grid_pred, cmap= "viridis", alpha=0.8)
ax.set_xlabel(x_var)
ax.set_ylabel(y_var)
ax.set_zlabel("Predicted Obesity")
plt.show()

# --------- # Plotting script for the Data Dominators project  - Suad --------- # 

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

