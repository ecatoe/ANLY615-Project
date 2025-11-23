import pandas as pd
import matplotlib.pyplot as plt
County_Health = pd.read_excel('C:/Users/USER/Desktop/Data Anly 615/df_tx_counties_health (1).xlsx', sheet_name='Sheet1')
Walkability_Df = pd.read_excel('C:/Users/USER/Desktop/Data Anly 615/Walkability_County_Condensed.xlsx', sheet_name='Walkability_Condensed')
Merged_df = County_Health.merge (Walkability_Df, how='left')
print (Merged_df.head)
Merged_df.to_excel('C:/Users/USER/Desktop/Data Anly 615/Merged_Data.xlsx', index=False)
from sqlalchemy import create_engine
engine = create_engine('sqlite:///my_database.db')
Merged_df.to_sql('Merged_Main', con=engine, if_exists='replace', index=False)
query="SELECT 'Texas County', 'TotalPopulation', 'TotalPop18plus', 'Food insecurity in the past 12 months among adults', 'No leisure-time physical activity among adults', 'Obesity among adults', 'pct_low_wage_emp',	'pct_med_wage_emp',	'pct_hi_wage_emp', 'pct_low_wage_wrk', 'pct_med_wage_wrk',	'pct_hi_wage_wrk',	'HH_total', '0_autos_pct',	'1_autos_pct',	'2_autos_pct',	'wtd_WrkAge_pop_pct',	'wtd_avg_walk_index' FROM Merged_Main;"
Results_df = pd.read_sql(query,engine) 
print (Results_df.head)
print (Results_df.describe(include='all'))


