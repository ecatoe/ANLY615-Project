#Data Dominators Walkability vs Obesity#
import pandas as pd

# Ethan's Section
# ====================================================================================================================== #
# filtering walkability dataset down to Texas (state 48)
walk_path = "EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv"
print("="*10, f"Importing {walk_path}", "="*10)
walk_df = pd.read_csv(walk_path)

print("="*10, f"Creating {'walk_tx_df'}", "="*10)
walk_tx_df = walk_df[walk_df['STATEFP'] == 48]

print("="*10, f"Exporting to {'WalkabilityTX.csv'}", "="*10)
walk_tx_df.to_csv('WalkabilityTX.csv', index=False)

# ====================================================================================================================== #
# Import walkability dataset filtered earlier by state (Texas)
walk_tx_path = "WalkabilityTX.csv"
print("="*10, f"Importing {walk_tx_path}", "="*10)
walk_tx_df = pd.read_csv(walk_tx_path)

# Importing and joining county name data on to walkability data
county_fp_path = "COUNTYFP_TX.csv"
county_fp_df = pd.read_csv(county_fp_path)

merged_df = walk_tx_df.merge(county_fp_df, how='left')

# defining new columns with calculations done to collapse date into single rows of county data
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

# exporting condensed dataset
output_file = "Walkability_County_Condensed.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    new_walk_tx_df.to_excel(writer, sheet_name='Walkability_Condensed', index=False)


# Tejas' Section 

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

