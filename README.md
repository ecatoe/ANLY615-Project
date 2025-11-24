#  Data Dominators — Texas Walkability & Food Access Integration
### ANLY 615 · Methods Memo · Data Wrangling & Integration
**Team:** Suad Castellanos · Ethan Catoe · Tejas Perwala · Mychael Haywood  
**Methods Memo Source:** [METHODS MEMO](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fecatoe%2FANLY615-Project%2Frefs%2Fheads%2Fmain%2FProject%2520Methods%2520Memo%2520-%2520Data%2520Dominators.docx&wdOrigin=BROWSELINK)



##  Project Overview
This project integrates multiple public datasets related to:

- Walkability  
- Food access  
- Food insecurity  
- Obesity  
- Wage distribution  
- Transportation access  
- Demographic & household characteristics  

The goal was to create a single, clean, Texas-only dataset that could be used for analysis and visualization.



##  Key Data Wrangling Challenges & Solutions  

### 1. Inconsistent Geographic Boundaries
Some datasets provided county-level data, while others reported at metro-area levels.

**Solution:**  
Standardized everything by merging counties into consistent metro-area groupings.

```python
walk_tx_df = pd.read_csv(walk_tx_path)
county_fp_df = pd.read_csv("COUNTYFP_TX.csv")
merged_df = walk_tx_df.merge(county_fp_df, how='left')
```



### 2. Duplicate Rows for Counties
Certain datasets included multiple rows for the same county.

**Solution:**  
Grouped and condensed duplicates into one consolidated county record.

```python
new_walk_tx_df = merged_df.groupby(["Texas County"]).apply(condense_function).reset_index()
```



### 3. Mismatched State Identifiers
Walkability used state **names**, while food access used numeric **FIPS codes**.

**Solution:**  
Converted identifiers so all datasets matched before merging.



### 4. Large, Unfiltered National Datasets
Original datasets were extremely large and contained thousands of irrelevant rows.

**Solution:**  
Filtered down to only Texas entries and selected the necessary variables.

```python
walk_df = pd.read_csv("EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv")
walk_tx_df = walk_df[walk_df["STATEFP"] == 48]
```



### 5. Recalculation After Grouping (Totals & Weighted Measures)
When merging geographic units, many values needed to be recomputed.

**Solution:**  
Recalculated population totals, employment totals, household counts, percentages, and weighted walkability metrics.

```python
def condense_function(df):
    return pd.Series({
        "COUNTY_POP": df["TotPop"].sum(),
        "COUNTY_EMP": df["TotEmp"].sum(),
    })
```



##  Database Schema

| Table Name      | Description                                          |
|-----------------|------------------------------------------------------|
| `Merged_Main`   | Final consolidated dataset for Texas counties        |
| `WalkabilityTX` | Filtered EPA walkability dataset                     |
| `FoodAccessTX`  | USDA food access indicators                          |
| `CountyFP`      | FIPS-to-county lookup table                          |



##  Final SQL Query
```sql
SELECT 
    'Texas County', 
    'TotalPopulation', 
    'TotalPop18plus', 
    'Food insecurity in the past 12 months among adults', 
    'No leisure-time physical activity among adults', 
    'Obesity among adults', 
    'pct_low_wage_emp',
    'pct_med_wage_emp',
    'pct_hi_wage_emp',
    'pct_low_wage_wrk',
    'pct_med_wage_wrk',
    'pct_hi_wage_wrk',
    'HH_total',
    '0_autos_pct',
    '1_autos_pct',
    '2_autos_pct',
    'wtd_WrkAge_pop_pct',
    'wtd_avg_walk_index'
FROM Merged_Main;
```



##  DataFrame Profile
<img width="879" height="191" alt="image" src="https://github.com/user-attachments/assets/4a24a2a5-1c2f-46d0-ab92-106880f2b826" />




##  Summary
Through filtering, merging, recalculation, and standardization of identifiers and geographic boundaries, we produced a unified dataset representing all Texas counties. This cleaned dataset supports reliable analysis of the relationships between walkability, food insecurity, and public health outcomes.

 
