import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

import numpy as np
import pandas as pd

def getGroceryStores():
    # Laden der Daten für 2015
    excel_pfad_2015 = '/Users/jasmin/Desktop/Livability Score Data/2015/Neighborhood/GroceryStores_2015.xlsx'
    df_2015 = pd.read_excel(excel_pfad_2015, sheet_name=2)
    
    # Laden der Daten für 2019
    excel_pfad_2019 = '/Users/jasmin/Desktop/Livability Score Data/2019/Neighborhood/GroceryStores_2019.xlsx'
    df_2019 = pd.read_excel(excel_pfad_2019, sheet_name=2)

    # Daten aufbereiten
    def prepare_data(df, year):
        df = df.filter(['State', 'County', 'lapophalfshare'])
        df['County'] = df['County'].str.replace('County', '').str.strip()
        df = df.rename(columns={'County': 'County Name'})
        if year == 2015:
            df['lapophalfshare'] = df['lapophalfshare'] * 100
        df['Year'] = year
        return df.groupby(['State', 'County Name', 'Year'])['lapophalfshare'].mean().reset_index()

    df_2015_prepared = prepare_data(df_2015, 2015)
    df_2019_prepared = prepare_data(df_2019, 2019)

    # Kombinieren der Daten
    combined_df = pd.concat([df_2015_prepared, df_2019_prepared], ignore_index=True)

    # Liste der Staaten und Countys
    states_counties = combined_df[['State', 'County Name']].drop_duplicates()

    interpolated_data = []

    for _, row in states_counties.iterrows():
        state = row['State']
        county = row['County Name']

        # Extrahieren der Werte für 2015 und 2019 für diesen State und County
        value_2015 = combined_df[(combined_df['State'] == state) & (combined_df['County Name'] == county) & (combined_df['Year'] == 2015)]['lapophalfshare'].values
        value_2019 = combined_df[(combined_df['State'] == state) & (combined_df['County Name'] == county) & (combined_df['Year'] == 2019)]['lapophalfshare'].values

        if len(value_2015) > 0 and len(value_2019) > 0:
            # Werte für 2015 und 2019 vorhanden
            known_years = [2015, 2019]
            known_values = [value_2015[0], value_2019[0]]

            # Lineare Interpolation
            for year in [2016, 2017, 2018]:
                interpolated_value = value_2015[0] + (value_2019[0] - value_2015[0]) * (year - 2015) / (2019 - 2015)
                interpolated_data.append({'State': state, 'County Name': county, 'Year': year, 'lapophalfshare': interpolated_value})

    interpolated_df = pd.DataFrame(interpolated_data)

    # Zusammenführen der interpolierten Daten mit den ursprünglichen Daten
    df_combined = pd.concat([combined_df, interpolated_df], ignore_index=True)

    df_combined['Perzentil_Grocery'] = df_combined.groupby(['State', 'County Name'])['lapophalfshare'].rank(pct=True) * 100
    df_combined['Inverted_Perzentil_Grocery'] = 100 - df_combined['Perzentil_Grocery']

    median_value = df_combined['lapophalfshare'].median()
    print("Median:", median_value)

    print(df_combined)

    # Exportieren als CSV
    output_path = '/Users/jasmin/Desktop/Livability Score Data/Combined_GroceryStores_2015-2019.csv'
    df_combined.to_csv(output_path, index=False)

    return df_combined

getGroceryStores()  # Beispielaufruf
