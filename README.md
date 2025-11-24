# Data Dominators — Texas Walkability, Food Access & Obesity Analysis

## Project Overview
This project analyzes relationships between walkability, food access, food insecurity, and obesity rates across Texas counties. Multiple public datasets were cleaned, standardized, and merged into a single analysis-ready dataset. The goal is to provide a consistent foundation for statistical modeling and visualization.

## Purpose of the Project
The purpose of this project is to:
- Combine several large datasets into a unified structure
- Align geographic boundaries (county vs. metro)
- Resolve inconsistent identifiers (state names vs. FIPS codes)
- Remove duplicate entries
- Recalculate totals and weighted metrics
- Produce a clean dataset for analysis

This README summarizes what the project does and how to run the associated code.

## How the Code Works
The Python code performs the following steps:

1. Load raw datasets (EPA Walkability, USDA Food Access, Census Demographics, etc.)
2. Filter all data to Texas only (STATEFP = 48)
3. Standardize columns used as join keys
4. Merge a FIPS lookup file to convert identifiers where needed
5. Identify and remove duplicate county rows
6. Group counties and recalculate totals and weighted averages
7. Condense datasets to only the required columns
8. Merge all cleaned datasets into one final DataFrame
9. Export the final dataset as a CSV and/or SQL table

### Example Code Snippets

**Merging walkability data with FIPS lookup:**
```python
walk_tx_df = pd.read_csv(walk_tx_path)
county_fp_df = pd.read_csv("COUNTYFP_TX.csv")
merged_df = walk_tx_df.merge(county_fp_df, how='left')
```

**Condensing duplicate county entries:**
```python
new_walk_tx_df = merged_df.groupby(["Texas County"]).apply(condense_function).reset_index()
```

**Filtering walkability dataset to Texas only:**
```python
walk_df = pd.read_csv("EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv")
walk_tx_df = walk_df[walk_df["STATEFP"] == 48]
```

**Recalculating totals after grouping:**
```python
def condense_function(df):
    return pd.Series({
        "COUNTY_POP": df["TotPop"].sum(),
        "COUNTY_EMP": df["TotEmp"].sum()
    })
```

## How to Run the Code

### Requirements
Install Python 3.8 or higher and the following packages:

```bash
pip install pandas numpy sqlalchemy
```

### Steps
1. Place all raw datasets in the project folder.
2. Open the Jupyter Notebook or Python script.
3. Run all cells in order.
4. The final cleaned dataset will be saved as:
   ```
   Merged_Main.csv
   ```
   or as an SQL table named:
   ```
   Merged_Main
   ```

### Running the SQL Query
If using SQLite or SQLAlchemy:

```sql
SELECT 
    "Texas County",
    "TotalPopulation",
    "TotalPop18plus",
    "Food insecurity in the past 12 months among adults",
    "No leisure-time physical activity among adults",
    "Obesity among adults",
    "pct_low_wage_emp",
    "pct_med_wage_emp",
    "pct_hi_wage_emp",
    "pct_low_wage_wrk",
    "pct_med_wage_wrk",
    "pct_hi_wage_wrk",
    "HH_total",
    "0_autos_pct",
    "1_autos_pct",
    "2_autos_pct",
    "wtd_WrkAge_pop_pct",
    "wtd_avg_walk_index"
FROM Merged_Main;
```

## Supporting Document
Download the full Methods Memo here:  
[Project Methods Memo - Data Dominators (1).docx](/mnt/data/Project Methods Memo - Data Dominators (1).docx)

## Folder Structure (Recommended)

```
ANLY615-DataDominators/
│
├── data/                # Raw datasets
├── cleaned/             # Cleaned datasets
├── code/                # Python scripts or notebooks
├── Merged_Main.csv      # Final merged dataset
└── README.md            # Project documentation
```

## Summary
This README explains the project's purpose, data sources, wrangling steps, and how to run the code. The full Methods Memo provides additional details on the challenges encountered and how they were addressed.


 
