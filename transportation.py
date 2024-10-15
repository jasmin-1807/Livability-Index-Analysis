import pandas as pd
import numpy as np
import os 

year = 2015 


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

   # Überprüfen, ob state_code ein String ist und nicht null
    if pd.notnull(state_code) and isinstance(state_code, str):
        state_code = state_code.upper()
        return state_codes.get(state_code, "State code not found")
    else:
        return "State code not found"


def calculate_percentage(x, max_value = None):
    if max_value==None:
        max_value=x.max()
    return (x / max_value) * 100 if max_value != 0 else 0

def calculate_inverted_percentage(x, max_value=None):
    return 100 - calculate_percentage(x, max_value)


def merge_with_population(crash_data, year):
    
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    excel_path = os.path.join(base_dir, "cross-year files", "CleanedPop2015-2019_CrashRate.xlsx")

    # Pfad der Bevölkerungsdaten anpassen
    df_population_cleaned = pd.read_excel(excel_path)

    # Spalte "County" in "County Name" umbenennen
    df_population_cleaned.rename(columns={'County': 'County Name'}, inplace=True)
    crash_data.rename(columns={'County': 'County Name'}, inplace=True)

    # "Parish" entfernen und "city" zu "City" korrigieren in der Spalte "County Name"
    df_population_cleaned['County Name'] = df_population_cleaned['County Name'].str.replace(' Parish', '', regex=False)
    df_population_cleaned['County Name'] = df_population_cleaned['County Name'].str.replace('city', 'City', regex=False)
    
    # Merge der DataFrames basierend auf den Spalten "State" und "County"
    df_merged = pd.merge(crash_data, df_population_cleaned, on=['State', 'County Name'], how='left', indicator=True)
    
    return df_merged

def rank_percentage(series):
    return series.rank(method='min').apply(lambda x: (x-1) / (len(series)-1) * 100)


def prepareCrashRate(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    base_path = os.path.join(base_dir, f'{year}/Transportation')
    filename = f'CrashRate_{year}.xlsx'
    full_path = os.path.join(base_path, filename)
    
    # Lesen des ersten Tabellenblatts
    df_sheet1 = pd.read_excel(full_path, sheet_name=0, header=5)
    # Entfernen der letzten Zeile (Summe aller Werte)
    df_sheet1 = df_sheet1.iloc[:-1]

    # Lesen des zweiten Tabellenblatt
    df_sheet2 = pd.read_excel(full_path, sheet_name=1, header=5)
    # Extrahieren der gewünschten Zeile aus dem zweiten Tabellenblatt
    row_to_add = df_sheet2.iloc[0]

    # Hinzufügen der Zeile zu dem ersten DataFrame
    df_combined = pd.concat([df_sheet1, row_to_add.to_frame().T], ignore_index=True)

    # Überprüfen, ob die gewünschten Spalten im DataFrame vorhanden sind
    desired_columns = ['State', 'County', 'Crash Date (Year)']
    if set(desired_columns).issubset(df_combined.columns):
        selected_data = df_combined[desired_columns]
        selected_data = selected_data.iloc[:-1]
    else:
        print("Einer oder mehrere der gewünschten Spaltennamen sind im DataFrame nicht vorhanden.")
        return None
    selected_data['State'] = selected_data['State'].astype(str)
    selected_data['County'] = selected_data['County'].astype(str)

    # Anzeigen der ersten paar Zeilen des resultierenden DataFrames 
    # print(selected_data.head())
    return selected_data

# Beispielaufruf der Funktion für ein spezifisches Jahr
#prepareCrashRate(year)


def getCrashRate(year):

    # Basisverzeichnis dynamisch ermitteln (Verzeichnis des Skripts)
    base_dir = os.path.dirname(os.path.realpath(__file__))

    crash_data = prepareCrashRate(year)
    
    crash_data['State'] = crash_data['State'].str.strip()
    crash_data['County'] = crash_data['County'].str.strip()

    df_merged = merge_with_population(crash_data, year)

    # Berechnung des Verhältnisses von Crash Total zur Bevölkerung für das angegebene Jahr
    population_column = str(year)
    
    # Annahme: "Crash Date (Year)" repräsentiert hier die Gesamtzahl der Unfälle, korrigiere dies entsprechend deinen Daten
    df_merged['Crash_to_Population_Rate'] = df_merged.apply(lambda row: (row['Crash Date (Year)'] / row[population_column] * 100000)
                                                   if population_column in df_merged.columns and row[population_column] > 0 
                                                   else None, axis=1)

    # Berechnung der invertierten Rangprozente für die Crash Rate
    # df_merged['Crash Rate Inverted Ranked Percentage'] = 100 - rank_percentage(df_merged['Crash_to_Population_Rate'])

    df_merged['Perzentil_CrashRate'] = df_merged.groupby(['County Name', 'State'])['Crash_to_Population_Rate'].transform(lambda x: np.percentile(x, 50))

    df_merged['Perzentil_CrashRate'] = df_merged['Crash_to_Population_Rate'].rank(pct=True) * 100

    df_merged['Inverted_Perzentil_CrashRate'] = 100 - df_merged['Perzentil_CrashRate']

    median_value = df_merged['Crash_to_Population_Rate'].median()
    print("Median:", median_value)


    # Anzeigen der ersten paar Zeilen des DataFrames, um das Ergebnis zu überprüfen
    print(df_merged[['State', 'County Name', 'Crash_to_Population_Rate', 'Inverted_Perzentil_CrashRate']])

    # Hier speichern des DataFrames als CSV
    output_path = os.path.join(base_dir, 'code generated interim files', 'Crash Rate & Population', f'CrashRatePopulation_{year}.csv')
    df_merged.to_csv(output_path, index=False)  # Speichern ohne Index

    # Rückgabe des kombinierten DataFrames
    return df_merged

print (getCrashRate(year))


def getSpeedLimits(year):

   # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur Excel-Datei im Ordner 'Allgemein'
    excel_pfad = os.path.join(base_dir,'cross-year files', 'SpeedLimitsIIhs.xlsx')

    df = pd.read_excel(excel_pfad)

    df.set_index('State', inplace=True)

# Leere Werte mit NaN ersetzen
    df.replace('', pd.NA, inplace=True)

# Spaltenwerte in numerische Werte konvertieren (falls noch nicht geschehen)
    df = df.apply(pd.to_numeric, errors='coerce')

# Spaltenwerte summieren (NaN-Werte werden ignoriert)
    summed_values = df.sum(axis=1, skipna=True)

# Anzahl der nicht leeren Werte in jeder Zeile zählen
    non_empty_counts = df.count(axis=1)

# Durchschnittswert berechnen
    average_values = summed_values / non_empty_counts

# Ergebnisse in ein DataFrame umwandeln
    result_df = pd.DataFrame({'Durchschnittsgeschwindigkeit': average_values})

    result_df = result_df.dropna()

    # Rangprozentsatz für die Durchschnittsgeschwindigkeit berechnen
    # result_df['Inverted_RankPercentage_SpeedLimits'] = 100 - rank_percentage(result_df['Durchschnittsgeschwindigkeit'])

    result_df['Perzentil_SpeedLimits'] = result_df.groupby('State')['Durchschnittsgeschwindigkeit'].transform(lambda x: np.percentile(x, 50))

    result_df['Perzentil_SpeedLimits'] = result_df['Durchschnittsgeschwindigkeit'].rank(pct=True) * 100

    result_df['Inverted_Perzentil_SpeedLimits'] = 100 - result_df['Perzentil_SpeedLimits']

    median_value = result_df['Durchschnittsgeschwindigkeit'].median()
    print("Median:", median_value)

    print(result_df)

# Ergebnisse ausgeben
    
    return result_df


getSpeedLimits(year)


def getADAStationsAndVehicles(year):
    
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    base_path = os.path.join(base_dir, f'{year}/Transportation')

    # Dynamische Pfade für die beiden Excel-Dateien
    transit_stations_path = os.path.join(base_path, f'{year} Transit Stations.xlsx')
    revenue_vehicle_inventory_path = os.path.join(base_path, f'{year} Revenue Vehicle Inventory.xlsx')

    # Einlesen der ersten Excel-Datei
    df1 = pd.read_excel(transit_stations_path, sheet_name=0, header=0)

    # Einlesen der zweiten Excel-Datei
    df2 = pd.read_excel(revenue_vehicle_inventory_path, sheet_name=0, header=0)

    # Auswahl der gewünschten Spalten aus der ersten Datei
    desired_columns_df1 = ['NTD ID', 'Total Stations', 'ADA Accessible Stations']
    selected_data_df1 = df1[desired_columns_df1]

    # Summieren der Werte von ADA Vehicles und Total Vehicles nach NTD ID
    station_totals = selected_data_df1.groupby('NTD ID').sum().reset_index()

    # Auswahl der gewünschten Spalten aus der zweiten Datei
    desired_columns_df2 = ['NTD ID', 'Total Fleet Vehicles', 'ADA Fleet Vehicles']  
    selected_data_df2 = df2[desired_columns_df2]

    # Summieren der Werte von ADA Vehicles und Total Vehicles nach NTD ID
    vehicle_totals = selected_data_df2.groupby('NTD ID').sum().reset_index()

    # Zusammenführen der DataFrames anhand der "NTD ID"
    merged_data = pd.merge(station_totals, vehicle_totals, on='NTD ID', how='inner')

    # Gruppieren nach 'NTD ID' und Berechnen des Mittelwerts für Duplikate
    grouped_data = merged_data.groupby('NTD ID', as_index=False).mean()

    # Berechnen des kombinierten ADA-Werts für jede NTD ID
    # grouped_data['Combined ADA Value'] = grouped_data['ADA Accessible Stations'] + grouped_data['ADA Fleet Vehicles']

    # Berechnen des Prozentsatzes der ADA-zugänglichen Transitstationen und -fahrzeuge
    grouped_data['ADA Stations Percentage'] = np.where(grouped_data['Total Stations'] > 0, 
                                                  (grouped_data['ADA Accessible Stations'] / grouped_data['Total Stations']) * 100, 
                                                  0)
    grouped_data['ADA Vehicles Percentage'] = np.where(grouped_data['Total Fleet Vehicles'] > 0, 
                                                   (grouped_data['ADA Fleet Vehicles'] / grouped_data['Total Fleet Vehicles']) * 100, 
                                                   0)

    grouped_data['Combined ADA Percentage'] = np.mean([grouped_data['ADA Stations Percentage'], grouped_data['ADA Vehicles Percentage']], axis=0)

        # Rang-Prozentsatz für den kombinierten ADA-Wert berechnen
    # grouped_data['ADA Rank Percentage'] = rank_percentage(grouped_data['Combined ADA Value'])

    # Einlesen des NTD_ID_States.csv Datensatzes, um die Staaten zu ergänzen
    # Dynamischer Pfad für die CSV-Datei
    csv_path = os.path.join(base_dir, 'cross-year files', 'NTD_ID_States.csv')
    # Einlesen der CSV-Datei
    ntd_id_states_df = pd.read_csv(csv_path)
    # Auswahl der relevanten Spalten
    ntd_id_states = ntd_id_states_df[['NTD ID', 'State']].drop_duplicates()

    # Zusammenführen mit dem grouped_data DataFrame, um die Staaten hinzuzufügen
    final_data = pd.merge(grouped_data, ntd_id_states, on='NTD ID', how='left')

    # Umwandlung der Staatskürzel in vollständige Namen
    final_data['State Name'] = final_data['State'].apply(state_code_to_name)

    print(final_data.columns)

    # Gruppierung nach 'State Name' und Berechnen des Mittelwerts für jeden Staat
    # Nutze .agg() um sowohl Mittelwerte als auch erste Einträge für nicht-numerische Daten zu erhalten
    state_summary = final_data.groupby('State Name').agg({
        'Combined ADA Percentage': 'mean',
        'State': 'first'  # Gehe davon aus, dass 'State' das Staatskürzel enthält, das als 'StateAbr' ausgegeben werden soll
    }).rename(columns={'State': 'StateAbr'})

    # Umbenennen des Index 'State Name' zu 'State' und Rücksetzen des Index
    state_summary.reset_index(inplace=True)
    state_summary.rename(columns={'State Name': 'State'}, inplace=True)

    state_summary['Perzentil_ADA'] = state_summary.groupby('State')['Combined ADA Percentage'].transform(lambda x: np.percentile(x, 50))

    state_summary['Perzentil_ADA'] = state_summary['Combined ADA Percentage'].rank(pct=True) * 100

    median_value = state_summary['Combined ADA Percentage'].median()
    print("Median:", median_value)


    # Ausgabe des DataFrames mit den korrekten Spaltennamen
    print(state_summary[['Combined ADA Percentage','Perzentil_ADA', 'StateAbr', 'State']])

    # Optional: Anzeigen der ersten paar Zeilen des resultierenden DataFrames, um die Struktur zu überprüfen
    print(state_summary)

    return state_summary

getADAStationsAndVehicles(year)



def getHouseholdTransportationCosts(year):

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad für die CSV-Datei
    csv_path = os.path.join(base_dir, 'cross-year files', 'Location_Affordability_Index.csv')

    # Einlesen der CSV-Datei
    df = pd.read_csv(csv_path, low_memory=False)

    # Anzeigen der Spalte CNTY_FIPS
    print(df['CNTY_FIPS'])
    
    # Summieren der Spalten hh1_t_cost bis hh8_t_cost für jede Zeile und Speichern in einer neuen Spalte "Transportation Costs"
    transportation_columns = [f'hh{i}_t_cost' for i in range(1, 9)]  # Generiert Spaltennamen dynamisch
    df['Transportation Costs'] = df[transportation_columns].mean(axis=1)

    # Konvertieren von STCOUNTYFP in String ohne .0 und Umbenennen zu FIPS
    df['FIPS'] = df['CNTY_FIPS'].astype(str).str[:-2]

    # Entfernen von Zeilen mit FIPS-Codes, die nichtnumerische Werte enthalten
    df = df[df['FIPS'].apply(lambda x: x.isdigit())]

    # Entfernen von Zeilen mit FIPS-Codes, die mit '720' beginnen
    df = df[~df['FIPS'].str.startswith(('720', '721'))]

    # Gruppierung der Daten nach FIPS und Berechnung des Mittelwerts der "Transportation Costs" für jede Gruppe
    df_grouped = df.groupby('FIPS')['Transportation Costs'].mean().reset_index()

    # Anwendung der rank_percentage Funktion auf die "Transportation Costs" und Speicherung in einer neuen Spalte "Rank Percentage"
    # df_grouped['Transportation_Costs_Rank_Percentage'] = rank_percentage(df['Transportation Costs'])
    df_grouped['Perzentil_TransportationCosts'] = df_grouped.groupby('FIPS')['Transportation Costs'].transform(lambda x: np.percentile(x, 50))

    df_grouped['Perzentil_TransportationCosts'] = df_grouped['Transportation Costs'].rank(pct=True) * 100

    df_grouped['Inverted_Perzentil_TransportationCosts'] = 100 - df_grouped['Perzentil_TransportationCosts']

    median_value = df_grouped['Transportation Costs'].median()
    print("Median:", median_value)
    
    # Anzeigen der Ergebnisse
    print(df_grouped)

    return df_grouped

getHouseholdTransportationCosts(year)

