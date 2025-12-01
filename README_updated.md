# Data Dominators — Texas Walkability, Food Access, Food Insecurity, and Obesity Analysis
Suad Castellanos, Ethan Catoe, Mychael Haywood, Tejas Perwala
## Project Overview
This project brings together several public datasets related to walkability, food access, food insecurity, and obesity in Texas. The goal was to clean, standardize, and merge these datasets into one file that can be used for analysis.

## Purpose
The main objectives were to:
- Combine multiple datasets into a single structure
- Align geographic boundaries across sources
- Fix inconsistent identifiers such as state names and FIPS codes
- Remove duplicate county entries
- Recalculate totals and weighted values when needed
- Preparing the final dataset for PCA, PCR, regression, and plotting

This README provides a summary of the project and instructions for running the code.

---

## Dataset Sources
Public datasets used in this project include:

- [EPA Smart Location Database](https://www.epa.gov/smartgrowth/smart-location-database)

- [PLACES: Local Data for Better Health](https://www.cdc.gov/places/index.html)

- [U.S. Census Bureau — County FIPS Codes](https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt)

Files included in this folder:
- Data Dominators Walkability vs Obesity.py  
- EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv
- COUNTYFP_TX.csv
- PLACES__Local_Data_for_Better_Health,_County_Data_2024_release_20251119.xlsx 
---

## How the Code Works

### Steps Performed
1. Load raw datasets.
2. Filter records to Texas counties.
3. Standardize the fields used for merging.
4. Join datasets using FIPS or county names.
5. Remove duplicates and combine repeating counties.
6. Recalculate totals and weighted metrics after grouping.
7. Select the final variables needed for analysis.
8. Export the merged dataset as a CSV file or SQL table.
9. Conduct PCA, PCR, and Linear Regression analyses.
10. Generate plots to showcase relationships in the data.

### Example Code Snippets

**Merge walkability data with FIPS lookup:**
```python
walk_tx_df = pd.read_csv(walk_tx_path)
county_fp_df = pd.read_csv("COUNTYFP_TX.csv")
merged_df = walk_tx_df.merge(county_fp_df, how="left")
```

**Group and condense duplicate county entries:**
```python
new_walk_tx_df = merged_df.groupby(["Texas County"]).apply(condense_function).reset_index()
```

**Filter walkability data to Texas only:**
```python
walk_df = pd.read_csv("EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv")
walk_tx_df = walk_df[walk_df["STATEFP"] == 48]
```

**Recalculate totals during grouping:**
```python
def condense_function(df):
    return pd.Series({
        "COUNTY_POP": df["TotPop"].sum(),
        "COUNTY_EMP": df["TotEmp"].sum()
    })
```

---

## How to Run the Code

### Requirements
Install Python 3.8 or later and the following packages:

```bash
pip install numpy pandas sqlalchemy scikit-learn matplotlib seaborn
```

### Instructions
1. Download or clone this repository.  
2. Place all raw datasets in the project directory.  
3. Run the Python script:
   - Data Dominators Walkability vs Obesity.py
4. The final dataset will be created as:
   ```
   Merged_Main.csv
   ```
   or as a SQL table named:
   ```
   Merged_Main
   ```

---

## Final SQL Query

```sql
SELECT
    "TotalPopulation", "TotalPop18plus", "Food insecurity in the past 12 months among adults", 
    "No leisure-time physical activity among adults", "Obesity among adults", "pct_low_wage_emp",
    "pct_med_wage_emp", "pct_hi_wage_emp", "pct_low_wage_wrk", "pct_med_wage_wrk", "pct_hi_wage_wrk",
    "HH_total", "0_autos_pct", "1_autos_pct", "2_autos_pct", "wtd_WrkAge_pop_pct", "wtd_avg_walk_index"
FROM
    Merged_Main;
```

---

## Supporting Document

Full methods memo:

[Project Methods Memo - Data Dominators.docx](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fecatoe%2FANLY615-Project%2Frefs%2Fheads%2Fmain%2FProject%2520Methods%2520Memo%2520-%2520Data%2520Dominators.docx&wdOrigin=BROWSELINK)


---

## Summary
The repository contains the cleaned datasets, processing scripts, and documentation needed to reproduce the final merged file. The methods memo goes into more detail about the challenges and the steps taken during the wrangling process.

