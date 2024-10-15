import pandas as pd
from os import path
import numpy as np
import os 

year = 2016 

def calculate_percentage(x, max_value = None):
    if max_value==None:
        max_value=x.max()
    return (x / max_value) * 100 if max_value != 0 else 0

def calculate_inverted_percentage(x, max_value=None):
    return 100 - calculate_percentage(x, max_value)

def rank_percentage(series):
    return series.rank(method='min').apply(lambda x: (x-1) / (len(series)-1) * 100)

def merge_with_population(df_housing, year):
    
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    population_file = os.path.join(base_dir, 'cross-year files/CleanedPop2015-2019NEU.xlsx')

    # Bevölkerungsdaten einlesen
    df_population_cleaned = pd.read_excel(population_file)

    # Sicherstellen, dass die Jahr-Spalten als Strings behandelt werden
    df_population_cleaned.columns = df_population_cleaned.columns.astype(str)
    
    # Merge der DataFrames basierend auf den Spalten "State" und "County"
    df_merged = pd.merge(df_housing, df_population_cleaned, on=['State', 'County Name'], how='left')
    
    return df_merged


def adjust_fips(tract_fips):
    # Konvertieren der TractFIPS in einen String, um mit den Zeichen zu arbeiten
    tract_fips_str = str(tract_fips)
    
    # Überprüfen der Länge von TractFIPS, um zu bestimmen, ob eine Anpassung nötig ist
    if len(tract_fips_str) == 4:  # FIPS-Code hat nur 4 Stellen, hinzufügen einer führenden 0 
        adjusted_fips = '0' + tract_fips_str
    else:  # FIPS-Code hat bereits 5 Stellen, keine Anpassung nötig
        adjusted_fips = tract_fips_str
    
    return adjusted_fips



def prepareMultiFamilyHousing(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    base_path = os.path.join(base_dir)


    if year == 2018:
        # Laden der Daten von 2017 und 2019
        data_2017 = pd.read_csv(os.path.join(base_path, '2017/Housing/Housing_2017.csv'), dtype=str, usecols=['GEO_ID', 'NAME', 'DP04_0008E', 'DP04_0009E', 'DP04_0010E', 'DP04_0011E', 'DP04_0012E', 'DP04_0013E'], skiprows=[1])
        data_2019 = pd.read_csv(os.path.join(base_path, '2019/Housing/Housing_2019.csv'), dtype=str, usecols=['GEO_ID', 'NAME', 'DP04_0008E', 'DP04_0009E', 'DP04_0010E', 'DP04_0011E', 'DP04_0012E', 'DP04_0013E'], skiprows=[1])

        # Konvertieren zu Numerisch
        spalten_auswahl = ['DP04_0008E', 'DP04_0009E', 'DP04_0010E', 'DP04_0011E', 'DP04_0012E', 'DP04_0013E']
        data_2017[spalten_auswahl] = data_2017[spalten_auswahl].apply(pd.to_numeric, errors='coerce')
        data_2019[spalten_auswahl] = data_2019[spalten_auswahl].apply(pd.to_numeric, errors='coerce')

        # Berechnung der Summe für jedes Jahr
        data_2017['Summe_2017'] = data_2017[spalten_auswahl].sum(axis=1)
        data_2019['Summe_2019'] = data_2019[spalten_auswahl].sum(axis=1)

        # Merge der Datasets anhand von GEO_ID und NAME
        merged_data = pd.merge(data_2017[['GEO_ID', 'NAME', 'Summe_2017']], data_2019[['GEO_ID', 'NAME', 'Summe_2019']], on=['GEO_ID', 'NAME'], how='outer')

        # Interpolate für 2018
        merged_data['Summe_2018'] = (
            merged_data['Summe_2017'] + 
            (merged_data['Summe_2019'] - merged_data['Summe_2017']) / 2
        )

        # Extrahieren von FIPS, County, and State information
        merged_data['FIPS'] = merged_data['GEO_ID'].str.replace('.*US', '', regex=True)
        merged_data['County Name'] = merged_data['NAME'].apply(lambda x: x.split(',')[0].replace(" County", "").strip())
        merged_data['State'] = merged_data['NAME'].apply(lambda x: x.split(',')[1].strip() if ',' in x else None)

        # Speichern der interpolated data für 2018
        result = merged_data[['FIPS', 'County Name', 'State', 'Summe_2018']]
        result.rename(columns={'Summe_2018': 'Summe'}, inplace=True)
        output_pfad = os.path.join(base_path, 'Ausgabe-Dateien', 'Multi Family Housing', f'MultiFamilyHousing2018.csv')
        
        result.to_csv(output_pfad, index=False)
        print(result)
    else:
        # Laden des Datasets für das sepzifische Jahr
        csv_pfad = os.path.join(base_path, f'{year}/Housing/Housing_{year}.csv')
        columns_to_load = ['GEO_ID', 'NAME', 'DP04_0008E', 'DP04_0009E', 'DP04_0010E', 'DP04_0011E', 'DP04_0012E', 'DP04_0013E']
        
        df = pd.read_csv(csv_pfad, dtype=str, usecols=columns_to_load, skiprows=[1])
        df.columns = df.columns.str.strip()
        
        spalten_auswahl = ['DP04_0008E', 'DP04_0009E', 'DP04_0010E', 'DP04_0011E', 'DP04_0012E', 'DP04_0013E']
        df[spalten_auswahl] = df[spalten_auswahl].apply(pd.to_numeric, errors='coerce')
        df['Summe'] = df[spalten_auswahl].sum(axis=1)
        
        df['FIPS'] = df['GEO_ID'].str.replace('.*US', '', regex=True)
        df['County Name'] = df['NAME'].apply(lambda x: x.split(',')[0].replace(" County", "").strip())
        df['State'] = df['NAME'].apply(lambda x: x.split(',')[1].strip() if ',' in x else None)
        
         # Dynamischer Speicherpfad für die CSV-Datei 
        output_pfad = os.path.join(base_path, 'code generated interim files', 'Multi Family Housing', f'MultiFamilyHousing{year}.csv')

        df.to_csv(output_pfad, index=False)
        print(df)

# Aufrufen der Funktion
prepareMultiFamilyHousing(year)
        

def getMultiFamilyHousing(year):
    # Dynamisch den Pfad basierend auf dem Verzeichnis des Skripts erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    csv_pfad = os.path.join(base_dir, f'code generated interim files/Multi Family Housing/MultiFamilyHousing{year}.csv')

    # CSV-Datei laden
    df_multi_family_housing = pd.read_csv(csv_pfad)
    df_merged = merge_with_population(df_multi_family_housing, year)
    
    # Anpassung der Spalte für das Bevölkerungsjahr und weitere Verarbeitung...
    population_column = str(year)
    if population_column in df_merged.columns:
        df_merged['Housing_to_Population'] = df_merged['Summe'] / df_merged[population_column]
        # df_merged['MultiFamilyHousing_Rank_Percentage'] = rank_percentage(df_merged['Housing_to_Population'])
        # Berechnung des Perzentils für jede Zeile
        df_merged['Perzentil_MultiFamily'] = df_merged.groupby('FIPS')['Housing_to_Population'].transform(lambda x: np.percentile(x, 50))

        df_merged['Perzentil_MultiFamily'] = df_merged['Housing_to_Population'].rank(pct=True) * 100

        median_value = df_merged['Housing_to_Population'].median()
        print("Median:", median_value)

    else:
        print(f"Warnung: Bevölkerungsspalte für {year} nicht gefunden.")
    
    output_pfad = os.path.join(base_dir, 'code generated interim files', 'Multi Family Housing', f'MultiFamilyPop_Index_{year}.csv')
    df_merged.to_csv(output_pfad, index=False)

    print (df_merged)

    return df_merged

getMultiFamilyHousing(year)


def getHousingCosts(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    base_path = os.path.join(base_dir)

    if year == 2018:
        # Laden der Daten für 2017 und 2019
        data_2017 = pd.read_csv(os.path.join(base_path, '2017/Housing/Housing_2017.csv'), dtype=str, usecols=['GEO_ID', 'NAME', 'DP04_0101E', 'DP04_0109E', 'DP04_0134E'], skiprows=[1])
        data_2019 = pd.read_csv(os.path.join(base_path, '2019/Housing/Housing_2019.csv'), dtype=str, usecols=['GEO_ID', 'NAME', 'DP04_0101E', 'DP04_0109E', 'DP04_0134E'], skiprows=[1])

        # Konvertieren der Spalten zu Numerisch
        spalten_auswahl = ['DP04_0101E', 'DP04_0109E', 'DP04_0134E']
        data_2017[spalten_auswahl] = data_2017[spalten_auswahl].apply(pd.to_numeric, errors='coerce')
        data_2019[spalten_auswahl] = data_2019[spalten_auswahl].apply(pd.to_numeric, errors='coerce')

        # Kappen der Werte bei 4000
        data_2017[spalten_auswahl] = data_2017[spalten_auswahl].clip(upper=4000)
        data_2019[spalten_auswahl] = data_2019[spalten_auswahl].clip(upper=4000)

        # Berechnen der Summe
        data_2017['Summe_2017'] = data_2017[spalten_auswahl].sum(axis=1)
        data_2019['Summe_2019'] = data_2019[spalten_auswahl].sum(axis=1)

        # Merge der Datasets anhand von GEO_ID und NAME
        merged_data = pd.merge(data_2017[['GEO_ID', 'NAME', 'Summe_2017']], data_2019[['GEO_ID', 'NAME', 'Summe_2019']], on=['GEO_ID', 'NAME'], how='outer')

        # Interpolate für 2018
        merged_data['Summe_2018'] = (
            merged_data['Summe_2017'] + 
            (merged_data['Summe_2019'] - merged_data['Summe_2017']) / 2
        )

        # Extrahieren von FIPS, County, und State information
        merged_data['FIPS'] = merged_data['GEO_ID'].str.replace('.*US', '', regex=True)
        merged_data['County'] = merged_data['NAME'].apply(lambda x: x.split(',')[0].replace(" County", "").strip())
        merged_data['State'] = merged_data['NAME'].apply(lambda x: x.split(',')[1].strip() if ',' in x else None)

        # Berechnung de Perzentils
        merged_data['Perzentil_HousingCosts'] = merged_data.groupby('FIPS')['Summe_2018'].transform(lambda x: np.percentile(x, 50))
        merged_data['Perzentil_HousingCosts'] = merged_data['Summe_2018'].rank(pct=True) * 100
        merged_data['Inverted_Perzentil_HousingCosts'] = 100 - merged_data['Perzentil_HousingCosts']

        median_value = merged_data['Summe_2018'].median()
        print("Median:", median_value)

        # Speichern dder interpolated data für 2018
        save_path = os.path.join(base_dir, 'code generated interim files', 'Housing Costs', f'Housing_Costs_Summary_2018.csv')
        merged_data.to_csv(save_path, index=False)

        print(merged_data)

        return merged_data
    else:
        csv_pfad = os.path.join(base_path, f'{year}/Housing/Housing_{year}.csv')
        
        # Spalten die geladen werden müssen
        columns_to_load = ['GEO_ID', 'NAME', 'DP04_0101E', 'DP04_0109E', 'DP04_0134E'] 
        
        # Einlesen der Data, Skippen der Metadata der ersten Zeile
        df = pd.read_csv(csv_pfad, dtype=str, usecols=columns_to_load, skiprows=[1])

        # Bereinigen der Spaltennamen
        df.columns = df.columns.str.strip()

        # Konvertierung zu Numerisch
        spalten_auswahl = ['DP04_0101E', 'DP04_0109E', 'DP04_0134E']
        df[spalten_auswahl] = df[spalten_auswahl].apply(pd.to_numeric, errors='coerce')


        # Kappen der Werte bei 4000
        df[spalten_auswahl] = df[spalten_auswahl].clip(upper=4000)

        # Summe berechnen
        df['Summe'] = df[spalten_auswahl].sum(axis=1)

        # Extrahieren von FIPS, County, and State information
        df['FIPS'] = df['GEO_ID'].str.replace('.*US', '', regex=True)
        df['County'] = df['NAME'].apply(lambda x: x.split(',')[0].replace(" County", "").strip())
        df['State'] = df['NAME'].apply(lambda x: x.split(',')[1].strip() if ',' in x else None)

        # Perzentile berechnen
        df['Perzentil_HousingCosts'] = df.groupby('FIPS')['Summe'].transform(lambda x: np.percentile(x, 50))
        df['Perzentil_HousingCosts'] = df['Summe'].rank(pct=True) * 100
        df['Inverted_Perzentil_HousingCosts'] = 100 - df['Perzentil_HousingCosts']

        median_value = df['Summe'].median()
        print("Median:", median_value)

        save_path = os.path.join(base_dir, 'code generated interim files', 'Housing Costs', f'Housing_Costs_Summary_{year}.csv')
        df.to_csv(save_path, index=False)

        print(df)

        return df

# Aufruf der Funktion
getHousingCosts(year)


def getHousingCostBurden(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    base_path = os.path.join(base_dir)

    if year == 2018:
        # Daten laden für 2017 und 2019
        data_2017 = pd.read_csv(os.path.join(base_path, '2017/Housing/Housing_2017.csv'), dtype=str, usecols=['GEO_ID', 'NAME', 'DP04_0101E', 'DP04_0109E', 'DP04_0134E'], skiprows=[1])
        data_2019 = pd.read_csv(os.path.join(base_path, '2019/Housing/Housing_2019.csv'), dtype=str, usecols=['GEO_ID', 'NAME', 'DP04_0101E', 'DP04_0109E', 'DP04_0134E'], skiprows=[1])

        # Konvertierung zu Numerisch
        spalten_auswahl = ['DP04_0101E', 'DP04_0109E', 'DP04_0134E']
        data_2017[spalten_auswahl] = data_2017[spalten_auswahl].apply(pd.to_numeric, errors='coerce')
        data_2019[spalten_auswahl] = data_2019[spalten_auswahl].apply(pd.to_numeric, errors='coerce')

        # Kappen bei 4000
        data_2017[spalten_auswahl] = data_2017[spalten_auswahl].clip(upper=4000)
        data_2019[spalten_auswahl] = data_2019[spalten_auswahl].clip(upper=4000)

        # Berechnung der Summe
        data_2017['Summe_2017'] = data_2017[spalten_auswahl].sum(axis=1)
        data_2019['Summe_2019'] = data_2019[spalten_auswahl].sum(axis=1)

        # Merge datasets anhand von GEO_ID und NAME
        merged_data = pd.merge(data_2017[['GEO_ID', 'NAME', 'Summe_2017']], data_2019[['GEO_ID', 'NAME', 'Summe_2019']], on=['GEO_ID', 'NAME'], how='outer')

        # Interpolate für 2018
        merged_data['Summe_2018'] = (
            merged_data['Summe_2017'] + 
            (merged_data['Summe_2019'] - merged_data['Summe_2017']) / 2
        )

        # Extrahieren von FIPS, County, und State information
        merged_data['FIPS'] = merged_data['GEO_ID'].str.replace('.*US', '', regex=True)
        merged_data['County'] = merged_data['NAME'].apply(lambda x: x.split(',')[0].replace(" County", "").strip())
        merged_data['State'] = merged_data['NAME'].apply(lambda x: x.split(',')[1].strip() if ',' in x else None)

        # Laden der salary data für 2018 aus Excel
        salary_df = pd.read_excel(f'{base_path}2018/Housing/Income_2018.xlsx', header=0, dtype={'fips2010': str})
        # Umbenennen zu "FIPS" and Behalten der ersten 5 Zeichen
        salary_df.rename(columns={'fips2010': 'FIPS'}, inplace=True)
        salary_df['FIPS'] = salary_df['FIPS'].str.slice(0, 5)

        # Gruppieren nach FIPS und Berechnen des Medians
        mean_median = salary_df.groupby('FIPS')['median'].median().reset_index()

        # Merge salary data mit housing data
        merged_data = pd.merge(merged_data, mean_median, on='FIPS', how='inner')

        # Berechnen der annual housing costs
        merged_data['Annual_Housing_Costs'] = merged_data['Summe_2018'] * 12

        # Berechnen des percentage of income devoted to monthly housing costs
        merged_data['Housing_to_Income_Percentage'] = (merged_data['Annual_Housing_Costs'] / merged_data['median']) * 100

        # Berechnen des Perzentils
        merged_data['Perzentil_HousingCostsBurden'] = merged_data.groupby('FIPS')['Housing_to_Income_Percentage'].transform(lambda x: np.percentile(x, 50))
        merged_data['Perzentil_HousingCostsBurden'] = merged_data['Housing_to_Income_Percentage'].rank(pct=True) * 100
        merged_data['Inverted_Perzentil_HousingCostsBurden'] = 100 - merged_data['Perzentil_HousingCostsBurden']

        median_value = merged_data['Housing_to_Income_Percentage'].median()
        print("Median:", median_value)

        # Speichern von interpolated data für 2018
        save_path = os.path.join(base_path, 'code generated interim files', 'Housing Costs', f'Housing_Costs_Summary_Neu_2018.csv')
        merged_data.to_csv(save_path, index=False)

        print(merged_data)

        return merged_data
    else:
        csv_pfad = os.path.join(base_path, f'{year}/Housing/Housing_{year}.csv')
        
        # Laden der ausgewählten Spalten
        columns_to_load = ['GEO_ID', 'NAME', 'DP04_0101E', 'DP04_0109E', 'DP04_0134E'] 
        
        # Nur die relevanten columns einlesen, skipping der ersten Zeile
        df = pd.read_csv(csv_pfad, dtype=str, usecols=columns_to_load, skiprows=[1])

        # Clean up 
        df.columns = df.columns.str.strip()

        # Konvertieren zu numerisch
        spalten_auswahl = ['DP04_0101E', 'DP04_0109E', 'DP04_0134E']
        df[spalten_auswahl] = df[spalten_auswahl].apply(pd.to_numeric, errors='coerce')

        # Kappen bei 4000
        df[spalten_auswahl] = df[spalten_auswahl].clip(upper=4000)

        # Berechnen der Summe
        df['Summe'] = df[spalten_auswahl].sum(axis=1)

        # Extrahieren von FIPS, County, und State information
        df['FIPS'] = df['GEO_ID'].str.replace('.*US', '', regex=True)
        df['County'] = df['NAME'].apply(lambda x: x.split(',')[0].replace(" County", "").strip())
        df['State'] = df['NAME'].apply(lambda x: x.split(',')[1].strip() if ',' in x else None)

        # Laden der average salary data für jedes county aus Excel
        salary_df = pd.read_excel(f'{base_path}/{year}/Housing/Income_{year}.xlsx', header=0, dtype={'fips2010': str})
        salary_df.rename(columns={'fips2010': 'FIPS'}, inplace=True)
        salary_df['FIPS'] = salary_df['FIPS'].str.slice(0, 5)

        # Gruppieren by FIPS und Berechnen des Medians
        mean_median = salary_df.groupby('FIPS')['median'].median().reset_index()

        # Merge salary data mit housing data
        df = pd.merge(df, mean_median, on='FIPS', how='inner')

        # Berechnen der annual housing costs
        df['Annual_Housing_Costs'] = df['Summe'] * 12

        # Berechnen dess percentage of income devoted to monthly housing costs
        df['Housing_to_Income_Percentage'] = (df['Annual_Housing_Costs'] / df['median']) * 100

        # Berechnen des Perzentils
        df['Perzentil_HousingCostsBurden'] = df.groupby('FIPS')['Housing_to_Income_Percentage'].transform(lambda x: np.percentile(x, 50))
        df['Perzentil_HousingCostsBurden'] = df['Housing_to_Income_Percentage'].rank(pct=True) * 100
        df['Inverted_Perzentil_HousingCostsBurden'] = 100 - df['Perzentil_HousingCostsBurden']

        median_value = df['Housing_to_Income_Percentage'].median()
        print("Median:", median_value)

        # Speichern des updated DataFrame zu einem CSV file
        save_path = os.path.join(base_path, 'code generated interim files', 'Housing Costs', f'Housing_Costs_Summary_Neu_{year}.csv')
        df.to_csv(save_path, index=False)

        print(df)

        return df

# Aufruf der Funkton
getHousingCostBurden(year)


def prepareSubsidizedHousingUnits(year): 

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    xlsx_pfad = os.path.join(base_dir, f'{year}/Housing/Subsidized.COUNTY_{year}.xlsx')
    
    df = pd.read_excel(xlsx_pfad)
    selected_columns = ['states', 'name', 'code', 'program_label', 'total_units']
    selected_data = df[selected_columns]

    # Filtern nach Zeilen mit 'program_label' gleich "Summary of All HUD Programs"
    filtered_data = selected_data[selected_data['program_label'] == 'Summary of All HUD Programs'].copy()
    
    if year == 2015:
        # Verarbeitung für 2015
        filtered_data['name'] = filtered_data['name'].str.replace('^\d{3} ', '', regex=True)
        filtered_data['name'] = filtered_data['name'].str.title()
        filtered_data['name'] = filtered_data['name'].str.replace(' County.*$', '', regex=True)
        filtered_data['name'] = filtered_data['name'].str.replace('Missing, ', '', regex=True)
        filtered_data['states'] = filtered_data['states'].str.title()
    else:
        # Verarbeitung für 2016 und später
        filtered_data['name'] = filtered_data['name'].str.replace(' County.*$', '', regex=True)
        filtered_data['name'] = filtered_data['name'].str.replace('Missing, ', '', regex=True)

    filtered_data.loc[:, 'states'] = filtered_data['states'].str[3:]

    # Umbenennen von 'code' zu 'FIPS' und Konvertierung zu String
    filtered_data['FIPS'] = filtered_data['code'].astype(str)

    # Filtern des DataFrames, um nur die Zeilen zu behalten, in denen 'FIPS' kein 'X' enthält
    filtered_data = filtered_data[~filtered_data['FIPS'].str.contains('X')]

    filtered_data.rename(columns={'states': 'State', 'name': 'County Name'}, inplace=True)

    # Ausgabe des Ergebnisses
    print(filtered_data)

    output_pfad = os.path.join(base_dir, f'{year}/Housing/Subsidized_Summary_{year}.xlsx')
    filtered_data.to_excel(output_pfad, index=False)

# Aufruf der Funktion
prepareSubsidizedHousingUnits(year)


def getSubsidizedHousingData(year):

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    xlsx_pfad = os.path.join(base_dir, f'{year}/Housing/Subsidized_Summary_{year}.xlsx')
    df_subsidized_units = pd.read_excel(xlsx_pfad)
    df_merged = merge_with_population(df_subsidized_units, year)
    
    # Berechnung des Anteils der subventionierten Einheiten zur Bevölkerung und weitere Verarbeitung...
    df_merged['Subsidized_to_Population'] = df_merged['total_units'] / df_merged[str(year)] * 10000
    # Berechnung der Rangprozente für den Anteil der subventionierten Einheiten zur Bevölkerung
    # df_merged['SubsidizedUnits_Rank_Percentage'] = rank_percentage(df_merged['Subsidized_to_Population'])

    df_merged['Perzentil_SubsidizedUnits'] = df_merged.groupby('FIPS')['Subsidized_to_Population'].transform(lambda x: np.percentile(x, 50))

    df_merged['Perzentil_SubsidizedUnits'] = df_merged['Subsidized_to_Population'].rank(pct=True) * 100

    median_value = df_merged['Subsidized_to_Population'].median()
    print("Median:", median_value)

    # Anzeigen der Spalten des DataFrames
    print("Spalten in df_merged:", df_merged.columns.tolist())

    # Dynamischer Speicherpfad für die CSV-Datei
    output_pfad = os.path.join(base_dir, 'code generated interim files', 'Subsidized Housing Units', f'Subsidized_Units_Index_{year}.csv')

    # Speichern des gemergten DataFrames als CSV-Datei
    df_merged.to_csv(output_pfad, index=False)

    return df_merged

getSubsidizedHousingData(year)


def merge_data_frame_by_location(df1, df2, criteria=['County Name', 'State']):

     # Erstellen einer Kopie von excel_df, um das Original unverändert zu lassen
    new_df = df1.copy()
    if criteria=='FIPS':
        df2['FIPS']= df2['FIPS'].astype(int)

    # Zuerst df_merged mit der Kopie von excel_df mergen, basierend auf gemeinsamen Spalten
    updated_df = pd.merge(new_df, df2, on=criteria, how='left',  suffixes=('', '_duplicate'))

    return updated_df

def merge_data_frames_by_location(df, criteria=['County Name', 'State']):

    df0= df[0]

    for i in range (1,len(df)):
        df0= merge_data_frame_by_location(df0, df[i], criteria)

    return df0

# merge_data_frames_by_location([excel_df, getAccesstoExerciseOpportunities(year), getPatientSatisfaction(year)])

def missing_values_average(df): 
    for i in range(0,len(df.columns)):
        column_name = df.columns[i]
        if df.dtypes[i] in [int, float]:
            df[column_name].fillna(df[column_name].mean(), inplace=True)
    return df 


# Laden der Excel-Datei in einen DataFrame
#df_base = pd.read_excel('/Users/jasmin/Desktop/Livability Score Data/Allgemein/US_FIPS_Codes.xls', header=1)
#df_final = df_base.copy()
#df_final = merge_data_frame_by_location(df_final, getMultiFamilyHousing(year),'FIPS')
#df_final = merge_data_frame_by_location(df_final, getHousingCosts(year),'FIPS')
#df_final = merge_data_frame_by_location(df_final, getHousingCostsBurden(year),'FIPS')
#df_final = merge_data_frame_by_location(df_final, getSubsidizedHousingData(year), 'FIPS')
#df_final = missing_values_average(df_final)
#print (df_final)
#df_final.to_csv(f'FinalHousingData{year}.csv', index=False)






















 


