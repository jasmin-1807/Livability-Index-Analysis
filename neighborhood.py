import pandas as pd
import numpy as np
import os

verbose = True

year = 2019

# def calculate_percentage(x, max_value=None):
    # if max_value is None:
        # max_value = x.max()
    # return (x / max_value) * 100 if max_value != 0 else 0

# def standardize_series(series):
    # return (series - series.mean()) / series.std()

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



def getCrimeRate(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamische Pfade für 2014 und 2016
    base_path_2014 = os.path.join(base_dir, '2014')
    base_path_2016 = os.path.join(base_dir, 'cross-year files')


    def loadCrimeData(year, base_path):
        stata_pfad_neighborhood = os.path.join(base_path, f'Crimes-{year}.dta')
        try:
            # Laden der Stata-Datei als pandas DataFrame
            dataframe = pd.read_stata(stata_pfad_neighborhood)

            # Berechnung der Verbrechensrate pro 10.000 Einwohner für alle Verbrechen
            dataframe['total_crimes'] = dataframe['VIOL'] + dataframe['PROPERTY']
            dataframe['population'] = dataframe['CPOPARST']
            dataframe['crime_rate'] = (dataframe['total_crimes'] / dataframe['population']) * 10000

            # Zusammenfügen des FIPS des Staates und des Countys, um den Gesamtfips zu erhalten
            dataframe['FIPS'] = dataframe['FIPS_ST'].astype(str).str.zfill(2) + dataframe['FIPS_CTY'].astype(str).str.zfill(3)

            # Entfernen der NaN-Werte
            clean_data = dataframe.dropna(subset=['crime_rate'])
            clean_data = clean_data.replace([np.inf, -np.inf], np.nan).dropna(subset=['crime_rate'])

            return clean_data[['FIPS', 'crime_rate']].copy()

        except Exception as e:
            print(f"Fehler beim Laden der Daten für {year}: {e}")
            return pd.DataFrame()

    if year == 2015:
        # Ladenn der Daten für 2014 und 2016
        data_2014 = loadCrimeData(2014, base_path_2014)
        data_2016 = loadCrimeData(2016, base_path_2016)

        if data_2014.empty or data_2016.empty:
            print("Fehler: Daten für eines der Jahre konnten nicht geladen werden.")
            return pd.DataFrame()

        # Verwenden von data_2014 als Basis und Ergänzen der Daten aus data_2016, wo verfügbar
        merged_data = pd.merge(data_2014, data_2016, on='FIPS', how='left', suffixes=('_2014', '_2016'))

        # Berechnen der linearen Interpolation für 2015
        merged_data['crime_rate_2015'] = merged_data['crime_rate_2014'] + (merged_data['crime_rate_2016'] - merged_data['crime_rate_2014']) / 2

        # Vorbereitung des finalen DataFrames 
        interpolated_data = merged_data[['FIPS', 'crime_rate_2015']].copy()
        
        # Berechnung des Perzentils für jede Zeile
        interpolated_data['Perzentil_Crime'] = interpolated_data.groupby('FIPS')['crime_rate_2015'].transform(lambda x: np.percentile(x, 50))
        interpolated_data['Perzentil_Crime'] = interpolated_data['crime_rate_2015'].rank(pct=True) * 100
        interpolated_data['Inverted_Perzentil_Crime'] = 100 - interpolated_data['Perzentil_Crime']
        
        print("Interpolierte Kriminalitätsrate für 2015:")
        print(interpolated_data)
        
        return interpolated_data

    else:
        # Für alle anderen Jahre die Daten von 2016 verwenden
        data_2016 = loadCrimeData(2016, base_path_2016)
        if data_2016.empty:
            print("Fehler: Daten für das Jahr 2016 konnten nicht geladen werden.")
            return pd.DataFrame()
        

        # Berechnung des Perzentils für jede Zeile
        data_2016['Perzentil_Crime'] = data_2016.groupby('FIPS')['crime_rate'].transform(lambda x: np.percentile(x, 50))
        data_2016['Perzentil_Crime'] = data_2016['crime_rate'].rank(pct=True) * 100
        data_2016['Inverted_Perzentil_Crime'] = 100 - data_2016['Perzentil_Crime']
        
        print(f"Kriminalitätsrate für {year} (basierend auf 2016):")
        print(data_2016)
        
        return data_2016

getCrimeRate(year)


def getVacancyRate(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    if year == 2018:
        # Pfade für 2017 und 2019
        path_2017 = os.path.join(base_dir, '2017', 'Housing', 'Housing_2017.csv')
        path_2019 = os.path.join(base_dir, '2019', 'Housing', 'Housing_2019.csv')

        data_2017 = pd.read_csv(path_2017, skiprows=lambda x: x in [1], dtype={'DP04_0003E': 'float', 'DP04_0001E': 'float'})
        data_2019 = pd.read_csv(path_2019, skiprows=lambda x: x in [1], dtype={'DP04_0003E': 'float', 'DP04_0001E': 'float'})

        data_2017['FIPS'] = data_2017['GEO_ID'].str.replace('.*US', '', regex=True)
        data_2019['FIPS'] = data_2019['GEO_ID'].str.replace('.*US', '', regex=True)

        vacancy_rate_2018 = (data_2017['DP04_0003E'] + data_2019['DP04_0003E']) / (data_2017['DP04_0001E'] + data_2019['DP04_0001E']) * 100
        data_2018 = data_2017.copy()
        data_2018['Vacancy_Rate'] = vacancy_rate_2018
        data_2018['Perzentil_Vacancy'] = data_2018.groupby('FIPS')['Vacancy_Rate'].transform(lambda x: np.percentile(x, 50))
        data_2018['Perzentil_Vacancy'] = data_2018['Vacancy_Rate'].rank(pct=True) * 100
        return data_2018[['GEO_ID', 'NAME', 'FIPS', 'Vacancy_Rate', 'Perzentil_Vacancy']]
    else:
        # Für 2015, 2016, 2017, 2019 und andere Jahre
        path = os.path.join(base_dir, str(year), 'Housing', f'Housing_{year}.csv')
        
        # Einlesen der Daten für das Jahr
        data = pd.read_csv(path, skiprows=lambda x: x in [1], dtype={'DP04_0003E': 'float', 'DP04_0001E': 'float'})
        data['FIPS'] = data['GEO_ID'].str.replace('.*US', '', regex=True)
        data['Vacancy_Rate'] = (data['DP04_0003E'] / data['DP04_0001E']) * 100

    # Anwendung der Rangprozente-Funktion auf die Leerstandsrate
    # data['Vacancy_Rate_Rank_Percentage'] = rank_percentage(data['Vacancy_Rate'])
        
    # Berechnung des Perzentils für jede Zeile
        data['Perzentil_Vacancy'] = data.groupby('FIPS')['Vacancy_Rate'].transform(lambda x: np.percentile(x, 50))

        data['Perzentil_Vacancy'] = data['Vacancy_Rate'].rank(pct=True) * 100

        median_value = data['Vacancy_Rate'].median()
        print("Median:", median_value)
    # Skaliere die Leerstandsquote auf eine Skala von 0 bis 100 relativ zum maximalen Wert im Datensatz
    # if 'Vacancy_Rate' in data.columns:
        # data['Vacancy_Rate_Scaled'] = calculate_percentage(data['Vacancy_Rate'])
        # return data[['GEO_ID', 'NAME', 'FIPS', 'Vacancy_Rate', 'Vacancy_Rate_Scaled']]
    # else:
        # return None
    
    # Auswahl der gewünschten Spalten für die Ausgabe
    output_columns = ['GEO_ID', 'NAME', 'FIPS', 'Vacancy_Rate', 'Perzentil_Vacancy']
    return data[output_columns]

# Beispielaufruf
try:
   vacancy_data_2019 = getVacancyRate(year)
   print(vacancy_data_2019)
except Exception as e:
   print(f"Ein Fehler ist aufgetreten: {e}")




def getParkScore(year): 
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    base_path = os.path.join(base_dir)

    if year == 2018:
    # Laden der Daten für 2017 und 2019
        # Laden der Daten für 2017 und 2019
        data_2017_path = f'{base_path}/2017/Neighborhood/ParkScore_2017.xlsx'
        data_2019_path = f'{base_path}/2019/Neighborhood/ParkScore_2019.xlsx'

        # Lesen der Excel-Dateien für 2017 und 2019
        data_2017 = pd.read_excel(data_2017_path, sheet_name=9, header=1)
        data_2019 = pd.read_excel(data_2019_path, sheet_name=7, header=1)

        # Skalieren der Prozentsätze 
        data_2017['Percent of Residents within Half-Mile Walk of Park'] = pd.to_numeric(data_2017['Percent of Residents within Half-Mile Walk of Park'], errors='coerce') * 100
        data_2019['Percent of Residents within Half-Mile Walk of Park'] = pd.to_numeric(data_2019['Percent of Residents within Half-Mile Walk of Park'], errors='coerce') * 100

        # Filtern der beiden Datensätze auf die relevanten Spalten
        data_2017_filtered = data_2017[['City', 'Percent of Residents within Half-Mile Walk of Park']].dropna()
        data_2019_filtered = data_2019[['City', 'Percent of Residents within Half-Mile Walk of Park']].dropna()

        # Verwende data_2017_filtered als Basis und ergänze Daten aus data_2019_filtered, wo verfügbar
    # Dies führt zu einem DataFrame, der alle Städte aus 2017 mit ihren ursprünglichen Werten und den ergänzten Werten aus 2019 enthält
        merged_data = pd.merge(data_2017_filtered, data_2019_filtered, on='City', how='left', suffixes=('_2017', '_2019'))

    # Ausfüllen fehlender Werte in den Daten von 2019 mit den Werten von 2017, falls keine Daten für 2019 vorliegen
        merged_data['Percent of Residents within Half-Mile Walk of Park_2019'].fillna(merged_data['Percent of Residents within Half-Mile Walk of Park_2017'], inplace=True)

    # Berechnen der linearen Interpolation für 2018
        merged_data['Percent of Residents within Half-Mile Walk of Park_2018'] = (
            merged_data['Percent of Residents within Half-Mile Walk of Park_2017'] + 
            (merged_data['Percent of Residents within Half-Mile Walk of Park_2019'] - merged_data['Percent of Residents within Half-Mile Walk of Park_2017']) / 2
        )

    # Vorberetung des finalen DataFrames
        filtered_df = merged_data[['City', 'Percent of Residents within Half-Mile Walk of Park_2018']]
        filtered_df['Perzentil_Park'] = filtered_df.groupby('City')['Percent of Residents within Half-Mile Walk of Park_2018'].transform(lambda x: np.percentile(x, 50))
        filtered_df['Perzentil_Park'] = filtered_df['Percent of Residents within Half-Mile Walk of Park_2018'].rank(pct=True) * 100
        filtered_df.rename(columns={'Percent of Residents within Half-Mile Walk of Park_2018': 'Percent of Residents within Half-Mile Walk of Park'}, inplace=True)
    else:   

    # Bestimmen der spezifischen Details basierend auf dem Jahr
        if year == 2019:
            sheet_name = 7  # 8. Tabellenblatt für 2019
            file_extension = 'xlsx'
        # elif year == 2018:
            # sheet_name = 0  # 1. Tabellenblatt für 2018
            # file_extension = 'xlsx'
        elif year in [2017, 2016]:
            sheet_name = 9  # 10. Tabellenblatt für 2017 und 2016
            file_extension = 'xlsx' if year == 2017 else 'xls'
        elif year == 2015:
            sheet_name = 14 # 15. Tabellenblatt für 2015
            file_extension = 'xlsx'
        else:
            raise ValueError("Daten für das angegebene Jahr sind nicht verfügbar.")
    
    # Vollständiger Pfad zur Datei
        filepath = f'{base_path}/{year}/Neighborhood/ParkScore_{year}.{file_extension}'
    
    # Lesen der spezifizierte Excel-Datei und des Tabellenblatts
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=1)  # Header ist in Zeile 2

       # Konvertieren der Prozentsätze zu numerischen Werten und handlen nicht-numerischer als NaN
        df['Percent of Residents within Half-Mile Walk of Park'] = pd.to_numeric(df['Percent of Residents within Half-Mile Walk of Park'], errors='coerce') * 100
    
    # Filtern der Daten nach den gewünschten Spalten
        filtered_df = df[['City', 'Percent of Residents within Half-Mile Walk of Park']].copy()

    # Anwendung der Rangprozente-Funktion auf die Spalte "Percent of Residents within Half-Mile Walk of Park"
        # filtered_df['Park_Access_Rank_Percentage'] = rank_percentage(filtered_df['Percent of Residents within Half-Mile Walk of Park'])

        # Berechnung des Perzentils für jede Zeile
        filtered_df['Perzentil_Park'] = filtered_df.groupby('City')['Percent of Residents within Half-Mile Walk of Park'].transform(lambda x: np.percentile(x, 50))

        filtered_df['Perzentil_Park'] = filtered_df['Percent of Residents within Half-Mile Walk of Park'].rank(pct=True) * 100

        median_value = filtered_df['Percent of Residents within Half-Mile Walk of Park'].median()
        print("Median:", median_value)
    
    print (filtered_df)

    return filtered_df

getParkScore(year)


def loadCityStateMappings(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur Excel-Datei
    filepath = os.path.join(base_dir, 'cross-year files', 'UsCities_States.xlsx')
    # Laden des entsprechenden Blattes für das gegebene Jahr
    city_state_df = pd.read_excel(filepath, sheet_name=str(year))
    return city_state_df


def getParkScoreWithState(year):
    # Laden der Park Score-Daten für das gegebene Jahr
    park_score_df = getParkScore(year)
    
    # Laden der Stadt-Staat-Zuordnungen für das gegebene Jahr
    city_state_df = loadCityStateMappings(year)
    
    # Verknüpfen der Park Score-Daten mit den Stadt-Staat-Zuordnungen
    # Angenommen, sowohl park_score_df als auch city_state_df haben eine Spalte namens 'City'
    merged_df = pd.merge(park_score_df, city_state_df, on='City', how='left')

    final_df = merged_df.drop(columns=['City'])

    # Gruppieren nach "State" und Berechnen des Mittelwerts für numerische Spalten
    final_df = merged_df.groupby('State').mean(numeric_only=True).reset_index()

    print (final_df)

    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    # Dynamischer Pfad für die CSV-Datei
    output_path = os.path.join(base_dir, 'code generated interim files', 'Park Scores with States', f'FinalParkScoreState{year}.csv')

    # Speichern des DataFrames als CSV-Datei
    final_df.to_csv(output_path, index=False)
    
    return final_df

getParkScoreWithState(year)



def getAccesstoLibraries(year): 
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    csv_pfad = os.path.join(base_dir, f'{year}', 'Neighborhood', f'Libraries_{year}.csv')

    df = pd.read_csv(csv_pfad, encoding='latin1')

    df['Population_Mode'] = df.groupby('CNTY')['CNTYPOP'].transform(lambda x: x.mode()[0])
    
    libraries_per_county = df.groupby(['CNTY', 'STABR']).agg(
        Number_of_Libraries=('LIBNAME', 'nunique'),
        Population=('CNTYPOP', 'max')  # Verwende 'max', da alle Werte gleich sein sollten
    ).reset_index()

    # Berechnen der Bibliotheken im Verhältnis zu den Einwohnern
    libraries_per_county['Libraries_per_Population'] = (libraries_per_county['Number_of_Libraries'] / libraries_per_county['Population'])

    # Anwenden der Rangprozente-Funktion auf die Libraries_per_Population-Spalte
    # libraries_per_county['Library_Rate_Rank_Percentage'] = rank_percentage(libraries_per_county['Libraries_per_Population'])

    # Berechnung des Perzentils für jede Zeile
    libraries_per_county['Perzentil_Libraries'] = libraries_per_county.groupby(['CNTY', 'STABR'])['Libraries_per_Population'].transform(lambda x: np.percentile(x, 50))

    libraries_per_county['Perzentil_Libraries'] = libraries_per_county['Libraries_per_Population'].rank(pct=True) * 100

    median_value = libraries_per_county['Libraries_per_Population'].median()
    print("Median:", median_value)

    # Umbenennen
    libraries_per_county = libraries_per_county.rename(columns={'CNTY': 'County Name'})

    # Ändern der Groß-/Kleinschreibung der 'County'-Spalte, sodass nur der erste Buchstabe großgeschrieben ist
    libraries_per_county['County Name'] = libraries_per_county['County Name'].str.capitalize()

    # Anwenden der Funktion `state_code_to_name` auf die 'STABR'-Spalte
    libraries_per_county['State'] = libraries_per_county['STABR'].apply(state_code_to_name)

    # Umbenennung
    libraries_per_county.columns = ['County Name', 'STABR', 'Number of Libraries', 'CNTYPOP', 'Libraries_per_Population', 'Perzentil_Libraries', 'State']

    
    print(libraries_per_county)

    
    return libraries_per_county

    # print(libraries_per_county[['Number of Libraries', 'Libraries_per_Population', 'Library Rate Rank Percentage']].sort_values('Library Rate Rank Percentage', ignore_index=True))
    # libraries_per_county[['Number of Libraries', 'Libraries_per_Population', 'Library Rate Rank Percentage']].sort_values('Library Rate Rank Percentage', ignore_index=True).plot()
    # plt.show()

getAccesstoLibraries(year)

#def prepareGroceryStores():
    # Laden der Daten für 2015
    #excel_pfad_2015 = '/Users/jasmin/Desktop/Livability Score Data/2015/Neighborhood/GroceryStores_2015.xlsx'
    #df_2015 = pd.read_excel(excel_pfad_2015, sheet_name=2)
    
    # Laden der Daten für 2019
    #excel_pfad_2019 = '/Users/jasmin/Desktop/Livability Score Data/2019/Neighborhood/GroceryStores_2019.xlsx'
    #df_2019 = pd.read_excel(excel_pfad_2019, sheet_name=2)

    # Daten aufbereiten
    #def prepare_data(df, year):
       # df = df.filter(['State', 'County', 'lapophalfshare'])
        #df['County'] = df['County'].str.replace('County', '').str.strip()
        #df = df.rename(columns={'County': 'County Name'})
        #if year == 2015:
            #df['lapophalfshare'] = df['lapophalfshare'] * 100
        #df['Year'] = year
        #return df.groupby(['State', 'County Name', 'Year'])['lapophalfshare'].mean().reset_index()

    #df_2015_prepared = prepare_data(df_2015, 2015)
    #df_2019_prepared = prepare_data(df_2019, 2019)

    # Kombinieren der Daten
    #combined_df = pd.concat([df_2015_prepared, df_2019_prepared], ignore_index=True)

    # Liste der Staaten und Countys
    #states_counties = combined_df[['State', 'County Name']].drop_duplicates()

    #interpolated_data = []

    #for _, row in states_counties.iterrows():
        #state = row['State']
        #county = row['County Name']

        # Extrahieren der Werte für 2015 und 2019 für diesen State und County
        #value_2015 = combined_df[(combined_df['State'] == state) & (combined_df['County Name'] == county) & (combined_df['Year'] == 2015)]['lapophalfshare'].values
        #value_2019 = combined_df[(combined_df['State'] == state) & (combined_df['County Name'] == county) & (combined_df['Year'] == 2019)]['lapophalfshare'].values

        #if len(value_2015) > 0 and len(value_2019) > 0:
            # Werte für 2015 und 2019 vorhanden
            #known_years = [2015, 2019]
            #known_values = [value_2015[0], value_2019[0]]

            # Lineare Interpolation
            #for year in [2016, 2017, 2018]:
                #nterpolated_value = value_2015[0] + (value_2019[0] - value_2015[0]) * (year - 2015) / (2019 - 2015)
                #interpolated_data.append({'State': state, 'County Name': county, 'Year': year, 'lapophalfshare': interpolated_value})

    #interpolated_df = pd.DataFrame(interpolated_data)

    # Zusammenführen der interpolierten Daten mit den ursprünglichen Daten
    #df_combined = pd.concat([combined_df, interpolated_df], ignore_index=True)

    #df_combined['Perzentil_Grocery'] = df_combined.groupby(['State', 'County Name'])['lapophalfshare'].rank(pct=True) * 100
    #df_combined['Inverted_Perzentil_Grocery'] = 100 - df_combined['Perzentil_Grocery']

    #median_value = df_combined['lapophalfshare'].median()
    #print("Median:", median_value)

    #print(df_combined)

    # Exportieren als CSV
    #output_path = '/Users/jasmin/Desktop/Livability Score Data/Combined_GroceryStores_2015-2019.csv'
    #df_combined.to_csv(output_path, index=False)

    #return df_combined

#prepareGroceryStores()


def getGroceryStores(year):

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    csv_pfad = os.path.join(base_dir, 'cross-year files', 'Combined_GroceryStores_2015-2019.csv')

    df = pd.read_csv(csv_pfad)

    # Filtern des Jahres
    filtered_data = df[df['Year'] == year]
    
    # Benötigte Spalten
    result = filtered_data[['County Name', 'State', 'lapophalfshare', 'Inverted_Perzentil_Grocery']]
    
    return result

filtered_data = getGroceryStores(year)
print(filtered_data)



def getFarmersMarkets(year): 
    
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur Excel-Datei
    excel_pfad = os.path.join(base_dir, 'cross-year files', 'Farmers_Markets.xlsx')

    # Dynamischer Pfad zur CSV-Datei
    zip_fips_pfad = os.path.join(base_dir, 'cross-year files', 'ZIP-COUNTY-FIPS_2017-06.csv')

    df = pd.read_excel(excel_pfad) 

    # Daten aus CSV-Datei mit den ZIP-FIPS-Zuordnungen lesen
    zip_fips_mapping = pd.read_csv(zip_fips_pfad,  usecols=['ZIP', 'STCOUNTYFP'], dtype={'ZIP': str})

    # Extrahieren der letzten 5 Zeichen aus der Spalte "location_address" und nur die Zeilen behalten, bei denen sie numerisch sind
    df['ZIP'] = df['location_address'].str[-5:]
    df = df[df['ZIP'].str.isdigit()]

    # Überprüfen auf Duplikate in der Spalte 'last_5_digits'
    duplicates = df.duplicated(subset=['ZIP'], keep=False)

    # Anzahl der Duplikate
    num_duplicates = duplicates.sum()
    print("Anzahl der Duplikate:", num_duplicates)

    # Anzeigen der Duplikate
    duplicate_rows = df[duplicates]
    print("Duplikate:")
    print(duplicate_rows)

    # FIPS-Codes basierend auf den ZIP-Codes hinzufügen
    df = df.merge(zip_fips_mapping, how='left', on='ZIP')

    # Konvertierung von STCOUNTYFP in String ohne .0 und umbenennen zu FIPS
    df['FIPS'] = df['STCOUNTYFP'].astype(str).str[:-2]

    # Entfernen aller Zeilen, wo 'FIPS' nichtnumerische Werte enthält
    df = df[df['FIPS'].apply(lambda x: x.isdigit())]

    # Zählen der Anzahl der Märkte pro Ort
    market_counts = df.groupby(['FIPS']).size().reset_index(name='market_count')

    print(type(market_counts['market_count']))

    # Anwenden der rank_percentage-Funktion auf die 'market_count'-Spalte
    # market_counts['market_count_rank_percentage'] = rank_percentage(market_counts['market_count'])

    # Berechnung des Perzentils für jede Zeile
    market_counts['Perzentil_Markets'] = market_counts.groupby('FIPS')['market_count'].transform(lambda x: np.percentile(x, 50))

    market_counts['Perzentil_Markets'] = market_counts['market_count'].rank(pct=True) * 100

    median_value = market_counts['market_count'].median()
    print("Median:", median_value)

    export_pfad = os.path.join(base_dir, 'code generated interim files', 'Farmers Markets', 'market_counts.xlsx')
    
    market_counts.to_excel(export_pfad, index=False)

    
    print(market_counts)

    return market_counts

getFarmersMarkets(year)





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

#def missing_values_average(df): 
    #for i in range(0,len(df.columns)):
        #column_name = df.columns[i]
        #if df.dtypes[i] in [int, float]:
            #df[column_name].fillna(df[column_name].mean(), inplace=True)
    #return df 


# Laden der Excel-Datei in einen DataFrame
#df_base = pd.read_excel('/Users/jasmin/Desktop/Livability Score Data/Allgemein/US_FIPS_Codes.xls', header=1)
#df_final = df_base.copy()
#df_final = merge_data_frame_by_location(df_final, getCrimeRate(year),'State')
#df_final = merge_data_frame_by_location(df_final, getVacancyRate(year),'FIPS')
#df_final = merge_data_frame_by_location(df_final, getParkScoreWithState(year), 'State')
#df_final = merge_data_frame_by_location(df_final, getAccesstoLibraries(year))
#df_final = missing_values_average(df_final)
#print (df_final)
#df_final.to_csv(f'FinalNeighborhoodData{year}.csv', index=False)

