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