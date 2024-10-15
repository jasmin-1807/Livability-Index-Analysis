import pandas as pd
from os import path
import numpy as np
import os 


year = 2015 

def rank_percentage(series):
    return series.rank(method='min').apply(lambda x: (x-1) / (len(series)-1) * 100)


def state_code_to_name(state_code):
    state_codes = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }

    # Convert the input to uppercase to handle case-insensitive matching
    state_code = state_code.upper()

    # Check if the state code is in the dictionary
    if state_code in state_codes:
        return state_codes[state_code]
    else:
        return "State code not found"



def getSocialAssociations(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    basis_pfad = os.path.join(base_dir, f'{year}', 'Engagement')

    # Dateiformat und Spaltennamen basierend auf dem Jahr bestimmen
    if year in [2015, 2016]:
        datei_pfad = os.path.join(basis_pfad, f'SocialAssociations{year}.xls')
        spaltenname = 'Association Rate'
    elif year in [2017, 2018, 2019]:
        datei_pfad = os.path.join(basis_pfad, f'SocialAssociations{year}.xlsx')
        spaltenname = 'Social Association Rate'
    else:
        print("Ungültiges Jahr. Daten nur für 2015-2019 verfügbar.")
        return

    # Einlesen der Datei 
    df = pd.read_excel(datei_pfad, sheet_name=3, header=1)
    df = df.filter(['State', 'County', spaltenname])
    df.rename(columns={'County': 'County Name'}, inplace=True)

    # Anwendung der Rangprozente auf die Preventable Hospitalization Rate
    # df['SocialAssociations_Rate_Rank_Percentage'] = rank_percentage(df[spaltenname])

    # Berechnung des Perzentils für jede Zeile
    df['Perzentil_SocialAssociations'] = df.groupby(['County Name','State'])[spaltenname].transform(lambda x: np.percentile(x, 50))

    df['Perzentil_SocialAssociations'] = df[spaltenname].rank(pct=True) * 100

    median_value = df[spaltenname].median()
    print("Median:", median_value)

    print(df)
    return df

getSocialAssociations(year)



def getCulturalInstitutions(year): 

    # Anpassung des Jahres, wenn eines der Jahre 2015, 2016, 2017 oder 2018 angegeben wird, da nur 2019 vorhanden
    if year in [2015, 2016, 2017, 2018, 2019]:
        year = 2014

     # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zum CSV-Datensatz
    dataset_path = os.path.join(base_dir, f'{year}', 'culturalinstitutions.csv')
    
    df = pd.read_csv(dataset_path) 

    # Umwandeln der Staatskürzel in vollständige Namen 
    df['State (Administrative Location)'] = df['State (Administrative Location)'].apply(state_code_to_name)
    
    # Gruppierung nach dem 'County Code (FIPS)' und Anzahl der Einträge pro Gruppe
    culinstitution_count_by_state = df.groupby('State (Administrative Location)').size().reset_index(name='Anzahl CulInstitutionen')

    # Berechnung des Perzentils für jede Zeile
    culinstitution_count_by_state['Perzentil_CulturalInstitutions'] = culinstitution_count_by_state.groupby('State (Administrative Location)')['Anzahl CulInstitutionen'].transform(lambda x: np.percentile(x, 50))

    culinstitution_count_by_state['Perzentil_CulturalInstitutions'] = culinstitution_count_by_state['Anzahl CulInstitutionen'].rank(pct=True) * 100

    median_value = culinstitution_count_by_state['Anzahl CulInstitutionen'].median()
    print("Median:", median_value)

    # Umbenennung er Spalte 'State (Administrative Location)' zu 'State'
    culinstitution_count_by_state = culinstitution_count_by_state.rename(columns={'State (Administrative Location)': 'State'})

    
    print(culinstitution_count_by_state)

    return culinstitution_count_by_state

getCulturalInstitutions(year)



def getSocialInvolvementIndex(year):

    # Anpassung des Jahres, wenn eines der Jahre 2015, 2016, 2017 oder 2018 angegeben wird, da nur 2019 vorhanden
    if year in [2015, 2016, 2017, 2018]:
        year = 2019
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    dataset_path = os.path.join(base_dir, f'{year}', 'Engagement', 'Social_Involvement_Index.csv')


    df = pd.read_csv(dataset_path)

    # Löschen von ungültigen Antworten
    invalid_answers = [-9, -3, -2, -1]
    df = df[~df['PES1'].isin(invalid_answers)]
    df = df[~df['PES6'].isin(invalid_answers)]
    df = df[~df['PES7'].isin(invalid_answers)]
    df = df[~df['PES15'].isin(invalid_answers)]

    # Erstellen der Spalte "FIPS" aus 'GESTFIPS' und 'GTCO'
    df['FIPS'] = df['GESTFIPS'].astype(str).str.zfill(2) + df['GTCO'].astype(str).str.zfill(3)

    # Addition der relevanten Spalten
    df['All'] = df['PES1'] + df['PES6'] + df['PES7'] + df['PES15']

    # Gruppierung nach 'FIPS' und Berechnung des Durchschnitts der 'All'-Spalte
    df_grouped = df.groupby('FIPS')['All'].mean().reset_index()

    # Berechnung des Durchschnitts aller Werte in der Spalte 'All' nach 'FIPS'
    average_all = df_grouped['All'].mean()

    # Einfügen einer Spalte 'Index', die die 'All'-Spalte durchschnittlich abgleicht
    df_grouped['Index'] = df_grouped['All'] / average_all

    # Verhältnismäßige Anpassung des Index
    # df_grouped['Index'] = df_grouped['Index'] / df_grouped['Index'].mean()

    # Berechnung des Durchschnitts und des niedrigstens Wert der Index-Spalte
    median_index = df_grouped['Index'].median()
    min_index = df_grouped['Index'].min()
    # Berechnung des Durchschnitts aller Werte in der Spalte 'All'
    average_all_index = df_grouped['All'].mean()

    print("Durchschnitt des Index:", median_index)
    print("Niedrigster Wert des Index:", min_index)
    print("Durchschnitt Wert von All:", average_all_index)

    df_grouped['Perzentil_SocialIndex'] = df_grouped.groupby('FIPS')['Index'].transform(lambda x: np.percentile(x, 50))

    df_grouped['Perzentil_SocialIndex'] = df_grouped['Index'].rank(pct=True) * 100

    df_grouped['Inverted_Perzentil_SocialIndex'] = 100 - df_grouped['Perzentil_SocialIndex']

    median_value = df_grouped['Index'].median()
    print("Median:", median_value)

    print (df_grouped)

    return df_grouped

getSocialInvolvementIndex(year)

def getBroadbandCostandSpeed(year):

    # Anpassung des Jahres, wenn 2015 angegeben wird, da Datenverfügbarkeit erst ab 2016 beginnt
    if year == 2015:
        year = 2016
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamische Pfade zu den Excel-Dateien
    download_path = os.path.join(base_dir, f'{year}', 'Engagement', f'Downloadge_{year}.xlsx')
    providers_path = os.path.join(base_dir, f'{year}', 'Engagement', f'Providers_{year}.xlsx')
    
    # Laden der Daten
    df_download = pd.read_excel(download_path, header=[1, 2])  # Angenommen, die relevante Header-Zeile ist die dritte (indexiert mit 2)
    df_providers = pd.read_excel(providers_path, header=[1, 2])

    # Kombination der Header-Zeilen zu einem einzigen Spaltennamen
    df_download.columns = ['_'.join(col).strip() for col in df_download.columns.values]
    df_providers.columns = ['_'.join(col).strip() for col in df_providers.columns.values]

    print (df_download.columns)
    print (df_providers.columns)

    # Sicherstellen, dass 'Area' als Index verwendet wird, um die DataFrames zusammenzuführen
    df_download.set_index('Unnamed: 0_level_0_Area', inplace=True)
    df_providers.set_index('Unnamed: 0_level_0_Area', inplace=True)

    # Zusammenführen der DataFrames basierend auf dem Index 'Area'
    common_areas = df_download.join(df_providers, lsuffix='_download', rsuffix='_providers')

    # Überprüfung der Spaltennamen im zusammengeführten DataFrame
    print("Gemeinsame Areas DataFrame Spalten:", common_areas.columns)

    # Addition der gewünschten Spalten aus jedem DataFrame
    common_areas['Combined_Percentage'] = common_areas['2 or more providers_all_download'] + common_areas['3 or more providers_all_providers']

    # Berechnung der neuen Spalte "Broadband cost and speed"
    # common_areas['Broadband_Cost_and_Speed'] = common_areas[['3 or more providers_all_providers', '2 or more providers_all_download']].min(axis=1)

    # Berechnung des Rangprozentsatzes
    # common_areas['Broadband_Rank_Percentage'] = common_areas['Combined_Percentage'].rank(method='min').apply(lambda x: (x-1) / (len(common_areas)-1) * 100)

    # Zurücksetzn des Index in die Spalten, um 'Area' und 'State' zu extrahieren
    common_areas.reset_index(inplace=True)
    common_areas[['Area', 'State']] = common_areas['Unnamed: 0_level_0_Area'].str.split(',', expand=True)

    # Entfernen aller Zeilen, die "Municipio" im Feld "Unnamed: 0_level_0_Area" enthalten
    common_areas = common_areas[~common_areas['Unnamed: 0_level_0_Area'].str.contains("Municipio")]

    # Entfernen der letzten 7 Zeichen aus jeder Zeile in 'Area'
    common_areas['Area'] = common_areas['Area'].str[:-7]

    # Umbenennung der Spalte "Area" in "County Name" 
    common_areas.rename(columns={'Area': 'County Name'}, inplace=True)

    # Sortieren des DataFrames alphabetisch nach 'County Name'
    common_areas_sorted_by_county = common_areas.sort_values(by='County Name')

    # Entfernen von Leerzeichen hinter der State Abbr.
    common_areas_sorted_by_county['State'] = common_areas_sorted_by_county['State'].str.strip()

    # Anwendung der Funktion 'state_code_to_name' auf die Spalte 'State'
    common_areas_sorted_by_county['State'] = common_areas_sorted_by_county['State'].apply(state_code_to_name)

    # Berechnung des Perzentils für jede Zeile
    common_areas_sorted_by_county['Perzentil_Broadband'] = common_areas_sorted_by_county.groupby(['County Name', 'State'])['Combined_Percentage'].transform(lambda x: np.percentile(x, 50))

    common_areas_sorted_by_county['Perzentil_Broadband'] = common_areas_sorted_by_county['Combined_Percentage'].rank(pct=True) * 100

    median_value = common_areas_sorted_by_county['Combined_Percentage'].median()
    print("Median:", median_value)

    # Speichern des DataFrames in eine CSV-Datei
    #common_areas.to_csv('common_areas_with_broadband_cost_and_speed.csv', index=False)

    # Berechnung des Mittelwerts der Spalte "2 or more providers_all_download"
    mean_download = common_areas['2 or more providers_all_download'].mean()

# Berechnung des Mittelwerts der Spalte "3 or more providers_all_providers"
    mean_providers = common_areas['3 or more providers_all_providers'].mean()

    print("Mittelwert der Spalte '2 or more providers_all_download':", mean_download)
    print("Mittelwert der Spalte '3 or more providers_all_providers':", mean_providers)

    
    print(common_areas_sorted_by_county)

    return common_areas_sorted_by_county

getBroadbandCostandSpeed(year)




def prepareVotingRate(year):

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    # Einlesen der Wahldaten
    path_elections = os.path.join(base_dir, 'cross-year files', 'countypres_2000-2020.csv')
    df_elections = pd.read_csv(path_elections)
    df_elections['FIPS'] = df_elections['county_fips'].astype(str).str[:-2]
    df_elections['state'] = df_elections['state'].str.title()

    # Einlesen der Bevölkerungsdaten
    path_population = os.path.join(base_dir, 'cross-year files', 'PopulationOver18.csv')
    df_population = pd.read_csv(path_population)
    df_population['DP05_0021E'] = pd.to_numeric(df_population['DP05_0021E'], errors='coerce')
    df_population['FIPS'] = df_population['GEO_ID'].str.replace('.*US', '', regex=True).astype(str).str.zfill(5)
    
    results = []
    for y in [2012, 2016, 2020]:
        df_year = df_elections[df_elections['year'] == y].copy()
        df_year = df_year.groupby('FIPS').apply(lambda x: x.loc[x['totalvotes'].idxmax()]).reset_index(drop=True)
        df_year['FIPS'] = df_year['FIPS'].astype(str).str.zfill(5)
        df_final = pd.merge(df_year, df_population, on='FIPS', how='left')
        df_final['Voting_Rate'] = (df_final['totalvotes'] / df_final['DP05_0021E']) * 100
        df_final['Voting_Rate'] = df_final['Voting_Rate'].clip(lower=30, upper=85)
        df_final = df_final[~df_final['FIPS'].str.contains('n')]
        results.append(df_final[['FIPS', 'Voting_Rate']])
    
    df_voting_2012, df_voting_2016, df_voting_2020 = results
    
    df_voting_2015 = df_voting_2012.copy()
    df_voting_2015['Voting_Rate'] = (df_voting_2012['Voting_Rate'] + df_voting_2016['Voting_Rate']) / 2
    
    df_voting_2017 = df_voting_2016.copy()
    df_voting_2017['Voting_Rate'] = (df_voting_2016['Voting_Rate'] * 0.75 + df_voting_2020['Voting_Rate'] * 0.25)
    
    df_voting_2018 = df_voting_2016.copy()
    df_voting_2018['Voting_Rate'] = (df_voting_2016['Voting_Rate'] * 0.5 + df_voting_2020['Voting_Rate'] * 0.5)
    
    df_voting_2019 = df_voting_2016.copy()
    df_voting_2019['Voting_Rate'] = (df_voting_2016['Voting_Rate'] * 0.25 + df_voting_2020['Voting_Rate'] * 0.75)
    
    interpolated_data = {
        'FIPS': df_voting_2016['FIPS'],
        'Voting_Rate_2012': df_voting_2012['Voting_Rate'],
        'Voting_Rate_2015': df_voting_2015['Voting_Rate'],
        'Voting_Rate_2016': df_voting_2016['Voting_Rate'],
        'Voting_Rate_2017': df_voting_2017['Voting_Rate'],
        'Voting_Rate_2018': df_voting_2018['Voting_Rate'],
        'Voting_Rate_2019': df_voting_2019['Voting_Rate'],
        'Voting_Rate_2020': df_voting_2020['Voting_Rate']
    }
    
    df_interpolated = pd.DataFrame(interpolated_data)
    
    # Berechnung des Perzentils für jede Voting Rate und für 2016
    for year in [2015, 2016, 2017, 2018, 2019]:
        column_name = f'Voting_Rate_{year}'
        percentile_column_name = f'Perzentil_Voting_Rate_{year}'
        df_interpolated[percentile_column_name] = df_interpolated.groupby('FIPS')[column_name].transform(lambda x: np.percentile(x, 50))
        df_interpolated[percentile_column_name] = df_interpolated[column_name].rank(pct=True) * 100
    
    median_value = df_interpolated['Voting_Rate_2016'].median()
    print("Median Voting Rate 2016:", median_value)

    # Speichern des Ergebnisses als CSV
    output_path = os.path.join(base_dir, 'cross-year files', 'interpolated_voting_rates.csv')
    df_interpolated.to_csv(output_path, index=False)
    
    print(df_interpolated)
    
    return df_interpolated

# Aufrufen der Funktion 
final_results = prepareVotingRate(year)


def getVotingRate(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    input_path = os.path.join(base_dir, 'cross-year files', 'interpolated_voting_rates.csv')
    df_interpolated = pd.read_csv(input_path)
    
    column_name = f'Voting_Rate_{year}'
    percentile_column_name = f'Perzentil_Voting_Rate_{year}'

        
    # Auswahl der relevanten Spalten
    df_result = df_interpolated[['FIPS', column_name, percentile_column_name]]

    # Entfernen des Jahres aus den Spaltennamen
    df_result = df_result.rename(columns={column_name: 'Voting_Rate', percentile_column_name: 'Perzentil_Voting_Rate'})
        
    print(f"Ergebnisse für das Jahr {year}:")
    print(df_result)
        
    return df_result

# Aufrufen der Funktion für das gewünschte Jahr
final_results = getVotingRate(year)
