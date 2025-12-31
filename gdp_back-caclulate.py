import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD AND CLEAN POPULATION DATA
# ==========================================
df_pop = pd.read_csv('population_malaysia.csv')

# Filter for: Total Population (Both Sexes, All Ages, All Ethnicities)
# Based on your file structure, we need: sex='both', age='overall', ethnicity='overall'
df_pop_clean = df_pop[
    (df_pop['sex'] == 'both') &
    (df_pop['age'] == 'overall') &
    (df_pop['ethnicity'] == 'overall')
].copy()

# Convert date to Year and keep relevant columns
df_pop_clean['Year'] = pd.to_datetime(df_pop_clean['date']).dt.year
df_pop_final = df_pop_clean[['Year', 'population']].sort_values('Year')

# Rename column (Population is likely in '000s based on DOSM standards, let's keep as is for now)
df_pop_final.columns = ['Year', 'Population_000s']

# ==========================================
# 2. LOAD AND CLEAN GDP DATA (The Tricky Part)
# ==========================================
df_gdp = pd.read_csv('gdp_state_real_supply.csv')

# Filter for "abs" (absolute values) only
df_gdp = df_gdp[df_gdp['series'] == 'abs']

# Group by Date to sum up ALL States and Sectors for the Total National GDP
df_gdp_agg = df_gdp.groupby('date')['value'].sum().reset_index()
df_gdp_agg['Year'] = pd.to_datetime(df_gdp_agg['date']).dt.year
df_gdp_final = df_gdp_agg[['Year', 'value']].sort_values('Year')
df_gdp_final.columns = ['Year', 'GDP_RM_Million']

# --- FIX MISSING YEARS (2010-2014) ---
# Your file starts in 2015. We must back-calculate using official Malaysia GDP growth rates.
# Growth rates: 2014(6.0%), 2013(4.7%), 2012(5.5%), 2011(5.3%), 2010(7.4%)
# We take the 2015 value and divide by (1 + growth_rate) to go backwards.

base_2015_gdp = df_gdp_final[df_gdp_final['Year'] == 2015]['GDP_RM_Million'].values[0]

# Calculate backwards
gdp_2014 = base_2015_gdp / 1.050  # 2015 growth was ~5.0%
gdp_2013 = gdp_2014 / 1.060
gdp_2012 = gdp_2013 / 1.047
gdp_2011 = gdp_2012 / 1.055
gdp_2010 = gdp_2011 / 1.053

# Create a dataframe for these missing years
missing_years = pd.DataFrame({
    'Year': [2010, 2011, 2012, 2013, 2014],
    'GDP_RM_Million': [gdp_2010, gdp_2011, gdp_2012, gdp_2013, gdp_2014]
})

# Combine missing years with your actual data
df_gdp_complete = pd.concat([missing_years, df_gdp_final], ignore_index=True)

# ==========================================
# 3. LOAD OPR DATA
# ==========================================
df_opr = pd.read_csv('opr-decision.csv')
# Keep only relevant years
df_opr = df_opr[['Year', 'OPR_Rate_Percentage']]

# ==========================================
# 4. MERGE EVERYTHING
# ==========================================
# Merge Population and GDP
df_merged = pd.merge(df_pop_final, df_gdp_complete, on='Year', how='inner')

# Merge with OPR
df_merged = pd.merge(df_merged, df_opr, on='Year', how='inner')

# Filter for project years (2010 - 2024 if available, otherwise up to 2023)
df_final = df_merged[(df_merged['Year'] >= 2010) & (df_merged['Year'] <= 2024)]

print("SUCCESS! Here is your cleaned X variable dataset:")
print(df_final)

# Save to use in the next step
df_final.to_csv('project_final_data_X.csv', index=False)
