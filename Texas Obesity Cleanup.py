import pandas as pd

#Load File
df = pd.read_excel("Texas_df.xlsx")

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

#Save Clean Data
df_counties.to_excel("df_tx_counties_health.xlsx", index=False)

print("Cleaned file written to df_tx_counties_health.xlsx")