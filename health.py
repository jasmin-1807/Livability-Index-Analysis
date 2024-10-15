import pandas as pd
from os import path 
import numpy as np
import os 

year = 2017

def calculate_percentage(x, max_value = None):
    if max_value==None:
        max_value=x.max()
    return (x / max_value) * 100 if max_value != 0 else 0

def calculate_inverted_percentage(x, max_value=None):
    return 100 - calculate_percentage(x, max_value)


def rank_percentage(series):
    return series.rank(method='min').apply(lambda x: (x-1) / (len(series)-1) * 100)


def calculate_statistics(df, value_column, group_column=None):
    """Berechnet das Perzentil und den Median für einen DataFrame."""
    # Berechnung des Perzentils für jede Zeile
    if group_column is not None:
        grouped = df.groupby(group_column)[value_column]
        df['Perzentil'] = grouped.transform(lambda x: np.percentile(x, 50))
    else:
        df['Perzentil'] = df[value_column].rank(pct=True) * 100

    # Berechnung des Medians
    median_value = df[value_column].median()
    
    return df, median_value


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


    state_code = state_code.upper()

    
    if state_code in state_codes:
        return state_codes[state_code]
    else:
        return "State code not found"
    


def getPatientSatisfaction(year):
    # Dynamisch den Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    csv_pfad = os.path.join(base_dir, f'{year}/Health/{year}_Hospital.csv')
    
    df = pd.read_csv(csv_pfad, encoding='ISO-8859-1', low_memory=False)
    

    # Schreibweise von 'County Name' anpassen
    df['County Name'] = df['County Name'].str.capitalize()

    # Filterung nach spezifischer Antwortbeschreibung
    filtered_df = df[df['HCAHPS Answer Description'] == 'Patients who gave a rating of "9" or "10" (high)']

    # Konvertierung der 'HCAHPS Answer Percent' Spalte zu numerischen Werten
    filtered_df.loc[:, 'HCAHPS Answer Percent'] = pd.to_numeric(filtered_df['HCAHPS Answer Percent'], errors='coerce')
    # Berechnen des Mittelwerts für 'HCAHPS Answer Percent'
        # mean_percent = filtered_df['HCAHPS Answer Percent'].mean()
    # Füllen aller leeren (NaN) Zeilen in 'HCAHPS Answer Percent' mit dem Mittelwert
        # filtered_df.loc[:, 'HCAHPS Answer Percent'] = filtered_df['HCAHPS Answer Percent'].fillna(mean_percent)

    columns_of_interest = ['County Name', 'State', 'HCAHPS Answer Description', 'HCAHPS Answer Percent']
    filtered_df = filtered_df[columns_of_interest]
    
    # Berechnung des Mittelwertes pro County
    grouped_df = filtered_df.groupby(['County Name', 'State'])['HCAHPS Answer Percent'].mean().reset_index()

    
    # Berechnung der Rangprozente für 'HCAHPS Answer Percent'
        #grouped_df['Satisfaction_Rank_Percentage'] = rank_percentage(grouped_df['HCAHPS Answer Percent'])

        # Aktualisieren des State-Spaltenwerts mit dem ausgeschriebenen Staatsnamen
    grouped_df['State'] = grouped_df['State'].map(state_code_to_name)

        # Berechnung des Perzentils für jede Zeile
    grouped_df['Perzentil_Satisfaction'] = grouped_df.groupby(['County Name', 'State'])['HCAHPS Answer Percent'].transform(lambda x: np.percentile(x, 50))

    grouped_df['Perzentil_Satisfaction'] = grouped_df['HCAHPS Answer Percent'].rank(pct=True) * 100

    median_value = grouped_df['HCAHPS Answer Percent'].median()
    print("Median:", median_value)


    # Anpassung des Ausgabepfades für das gefilterte CSV
    output_csv_pfad = os.path.join(base_dir, f'{year}/Health/Patient_Satisfaction_Filtered.csv')
    grouped_df.to_csv(output_csv_pfad, index=False)
    print(grouped_df)
    return grouped_df

# Beispielaufruf der Funktion für das Jahr 2018
getPatientSatisfaction(year)


def adjust_fips(tract_fips):
    # Konvertieren von TractFIPS in einen String, um mit den Zeichen zu arbeiten
    tract_fips_str = str(tract_fips)
    # Extrahieren der ersten 5 Zeichen, da diese den FIPS-Code enthalten

    
    # Überprüfen der Gesamtlänge von TractFIPS, um zu bestimmen, ob eine Anpassung nötig ist
    if len(tract_fips_str) == 10:  # Impliziert, dass eine führende 0 fehlt (einstellige Staats-ID)
        adjusted_fips = '0' + tract_fips_str[:4]
    else:  # Keine Anpassung nötig, Nutzen der ersten 5 Ziffern direkt
        adjusted_fips = tract_fips_str[:5]
    
    return adjusted_fips

def getSmokingPrevalence(year):

    if year == 2018 or year == 2019:
        year = 2017
    # Dynamische Anpassung des Pfades basierend auf dem Jahr
    # Dynamisch den Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    csv_pfad = os.path.join(base_dir, f'{year}/Health/SmokingObesity{year}.csv')
    
    try:
        df = pd.read_csv(csv_pfad)
        # Die ersten 4 Stellen der TractFIPS geben die FIPS von State + County an, eine 0 wird
        # hinzugefügt, um die Spalte mit dem "County/State" Dokument mergen zu können
        # df['FIPS'] = '0' + df['TractFIPS'].astype(str).str[:4]
        df['FIPS'] = df['TractFIPS'].apply(adjust_fips)

          # Gruppierung nach FIPS und Berechnung des Mittelwerts
        df = df.groupby('FIPS').agg({
            'CSMOKING_CrudePrev': 'mean'
        }).reset_index()

        # Berechnung des Perzentils für jede Zeile
        df['Perzentil_Smoking'] = df.groupby('FIPS')['CSMOKING_CrudePrev'].transform(lambda x: np.percentile(x, 50))

        df['Perzentil_Smoking'] = df['CSMOKING_CrudePrev'].rank(pct=True) * 100

        df['Inverted_Perzentil_Smoking'] = 100 - df['Perzentil_Smoking']


        median_value = df['CSMOKING_CrudePrev'].median()
        print("Median:", median_value)

        # Anwendung der rank_percentage Formel auf CSMOKING_CrudePrev
        # df['Smoking_Rank_Percentage'] = rank_percentage(df['CSMOKING_CrudePrev'])
        
        # Invertierung der Smoking Rank Percentage, sodass niedrige Raucherprävalenz hohe Werte ergibt
        # df['Inverse_Smoking_Rank_Percentage'] = 100 - df['Smoking_Rank_Percentage']

        print (df)
        return df
    except FileNotFoundError:
        print(f"Datei für das Jahr {year} nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None
         
# Beispielaufruf für das Jahr 2018
getSmokingPrevalence(year)



def getObesityPrevalence(year):

    if year == 2018 or year == 2019:
        year = 2017
    
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    csv_pfad = os.path.join(base_dir, f'{year}/Health/SmokingObesity{year}.csv')
    
    try:
        df = pd.read_csv(csv_pfad)

        # Die ersten 4 Stellen der TractFIPS geben die FIPS von State + County an, eine 0 wird
    # hinzugefügt um die Spalte mit dem "County/State" Dokument mergen zu können
        df['FIPS'] = df['TractFIPS'].apply(adjust_fips)
        
        # Gruppierung nach FIPS und Berechnung des Mittelwerts
        df = df.groupby('FIPS').agg({
            'OBESITY_CrudePrev': 'mean'
        }).reset_index()

    # Anwendung der rank_percentage Formel auf CSMOKING_CrudePrev
        #df['Obesity_Rank_Percentage'] = rank_percentage(df['OBESITY_CrudePrev'])
        
        # Invertierung der Smoking Rank Percentage, sodass niedrige Raucherprävalenz hohe Werte ergibt
        #df['Inverse_Obesity_Rank_Percentage'] = 100 - df['Obesity_Rank_Percentage']

        # Berechnung des Perzentils für jede Zeile
        df['Perzentil_Obesity'] = df.groupby('FIPS')['OBESITY_CrudePrev'].transform(lambda x: np.percentile(x, 50))

        df['Perzentil_Obesity'] = df['OBESITY_CrudePrev'].rank(pct=True) * 100

        df['Inverted_Perzentil_Obesity'] = 100 - df['Perzentil_Obesity']

        median_value = df['OBESITY_CrudePrev'].median()
        print("Median:", median_value)
    
        return df
    except FileNotFoundError:
        print(f"Datei für das Jahr {year} nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None
    
# Beispielaufruf für das Jahr 2018
df_obesity = getObesityPrevalence(year)
print(df_obesity)


def getPreventableHospitalizationRate(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    basis_pfad = os.path.join(base_dir, f'{year}/Health/')
    
    # Dateiformat und Spaltennamen basierend auf dem Jahr bestimmen
    if year in [2015, 2016]:
        datei_pfad = os.path.join(basis_pfad, f'PreventableHosp{year}.xls')
        spaltenname = 'Preventable Hosp. Rate'
    elif year in [2017, 2018, 2019]:
        datei_pfad = os.path.join(basis_pfad, f'PreventableHosp{year}.xlsx')
        spaltenname = 'Preventable Hospitalization Rate'
    else:
        print("Ungültiges Jahr. Daten nur für 2015-2019 verfügbar.")
        return

    # Lese die Datei ein
    df = pd.read_excel(datei_pfad, sheet_name=3, header=1)
    df = df.filter(['State', 'County', 'FIPS', spaltenname])
    df.rename(columns={'County': 'County Name'}, inplace=True)

    # Lösche alle Zeilen, in denen 'County Name' leer ist
    df.dropna(subset=['County Name'], inplace=True)

    # Berechnung des Perzentils für jede Zeile
    df['Perzentil_Hospitalization'] = df.groupby('FIPS')[spaltenname].transform(lambda x: np.percentile(x, 50))

    df['Perzentil_Hospitalization'] = df[spaltenname].rank(pct=True) * 100

    df['Inverted_Hospitalization_Perzentil'] = 100 - df['Perzentil_Hospitalization']

    median_value = df[spaltenname].median()
    print("Median:", median_value)
    
    # Anwendung der Rangprozente auf die Preventable Hospitalization Rate
    #df['Hospitalization_Rate_Rank_Percentage'] = rank_percentage(df[spaltenname])

    # Inversion der Rangprozente
    #df['Inverted_Hospitalization_Rate_Rank_Percentage'] = 100 - df['Hospitalization_Rate_Rank_Percentage']

    print(df)
    return df

getPreventableHospitalizationRate(year)




def load_data(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    base_path = os.path.join(base_dir, f'{year}/Health/AccessExercise{year}')
    
    # Dateiendung basierend auf dem Jahr festlegen
    file_extension = '.xls' if year in [2014, 2016, 2018] else '.xlsx'
    
    # Vollständigen Dateipfad zusammenstellen
    xlsx_path = f"{base_path.format(year, year)}{file_extension}"
    
    try:
        df = pd.read_excel(xlsx_path, sheet_name=3, header=1)
        
        # Spaltenname basierend auf dem Jahr anpassen
        if year in [2014, 2016, 2018]:
            access_column = '% With Access'
        else:
            access_column = '% With Access to Exercise Opportunities'
        
        # Überprüfen, ob die gewünschte Spalte existiert
        if access_column not in df.columns:
            raise ValueError(f"Spalte '{access_column}' nicht gefunden in {year}.")
        
        df = df[['State', 'County', 'FIPS', access_column]]
        df.rename(columns={access_column: '% With Access to Exercise Opportunities'}, inplace=True)

        # Anwendung der Rangprozente
        # df['Access_Exercise_Rank_Percentage'] = rank_percentage(df['% With Access to Exercise Opportunities'])

        # Berechnung des Perzentils für jede Zeile
        df['Perzentil'] = df.groupby('FIPS')['% With Access to Exercise Opportunities'].transform(lambda x: np.percentile(x, 50))

        df['Perzentil'] = df['% With Access to Exercise Opportunities'].rank(pct=True) * 100

        median_value = df['% With Access to Exercise Opportunities'].median()
        print("Median:", median_value)

        # Umbenennen der "County" Spalte in "County Name" direkt nach dem Laden
        df = df.rename(columns={'County': 'County Name'})

        # Lösche alle Zeilen, in denen 'County Name' leer ist
        df.dropna(subset=['County Name'], inplace=True)
        
        return df
    except FileNotFoundError:
        print(f"Datei für das Jahr {year} nicht gefunden.")
        return None
    except ValueError as e:
        print(e)
        return None
    
def interpolate_data(df_earlier, df_later):
    """Interpoliert Daten zwischen zwei DataFrames."""
    # Sicherstellen, dass die DataFrames sortiert sind, um korrekt zu interpolieren
    df_earlier = df_earlier.sort_values(by=['State', 'County Name']).reset_index(drop=True)
    df_later = df_later.sort_values(by=['State', 'County Name']).reset_index(drop=True)
    
    # Berechnung des Mittelwerts für die Spalte '% With Access to Exercise Opportunities'
    interpolated_values = df_earlier['% With Access to Exercise Opportunities'] + (df_later['% With Access to Exercise Opportunities'] - df_earlier['% With Access to Exercise Opportunities']) / 2
    df_interpolated = df_earlier.copy()
    df_interpolated['% With Access to Exercise Opportunities'] = interpolated_values

    # Anwendung der Rangprozente auf die interpolierte Spalte
    # df_interpolated['Access_Exercise_Rank_Percentage'] = rank_percentage(df_interpolated['% With Access to Exercise Opportunities'])

    # Berechnung des Perzentils für jede Zeile
    df_interpolated['Perzentil_Exercise'] = df_interpolated.groupby('FIPS')['% With Access to Exercise Opportunities'].transform(lambda x: np.percentile(x, 50))

    df_interpolated['Perzentil_Exercise'] = df_interpolated['% With Access to Exercise Opportunities'].rank(pct=True) * 100

    median_value = df_interpolated['% With Access to Exercise Opportunities'].median()
    print("Median:", median_value)
    
    
    return df_interpolated

def getAccesstoExerciseOpportunities(year):
    if year in [2019, 2018, 2016, 2014]:
        return load_data(year)
    elif year == 2017:
        df_2016 = load_data(2016)
        df_2018 = load_data(2018)
        return interpolate_data(df_2016, df_2018)
    elif year == 2015:
        df_2014 = load_data(2014)
        df_2016 = load_data(2016)
        return interpolate_data(df_2014, df_2016)
    else:
        print(f"Keine Daten verfügbar für das Jahr {year}.")
        return None
    
df_opportunities = getAccesstoExerciseOpportunities(year)
print(df_opportunities)


def getHealthcareShortage(year): 

     # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Aktuelles Verzeichnis des Skripts
    excel_file = os.path.join(base_dir, 'cross-year files/HPSA_Score_2023.xlsx')
    df = pd.read_excel(excel_file, header=0)  # Header in der ersten Zeile

    # Benötigte Spalten auswählen
    df_selected = df[['Common State County FIPS Code', 'HPSA Score']]
    df_selected = df_selected.rename(columns={'Common State County FIPS Code': 'FIPS'})

    # Nach FIPS gruppieren und Mittelwert berechnen
    grouped_mean = df_selected.groupby('FIPS').mean()
    
    # Berechnung des Perzentils für jede Zeile
    grouped_mean['Perzentil_HealthcareShortage'] = grouped_mean.groupby('FIPS')['HPSA Score'].transform(lambda x: np.percentile(x, 50))

    grouped_mean['Perzentil_HealthcareShortage'] = grouped_mean['HPSA Score'].rank(pct=True) * 100

    grouped_mean['Inverted_HealthcareShortage_Perzentil'] = 100 - grouped_mean['HPSA Score']

    median_value = grouped_mean['HPSA Score'].median()
    print("Median:", median_value)

    # Index in eine Spalte zurücksetzen
    grouped_mean.reset_index(inplace=True)

    # Zeilen löschen, in denen 'XXXXX' in der Spalte 'FIPS' steht
    grouped_mean = grouped_mean[grouped_mean['FIPS'] != 'XXXXX']

    print(grouped_mean)

    return grouped_mean

getHealthcareShortage(2023)


# Datensatz für alle Städte laden
# funktionen = []
# for funktion in funktionen : 
    # df=funktion(2019)
#   gesamtdatensatz

# def remove_existing_suffixes(df, suffixes=('_left', '_right')):
    # Umbenennen von Spalten, die bereits die Suffixe enthalten, um Konflikte zu vermeiden
    #new_column_names = {}
    #for column in df.columns:
        #for suffix in suffixes:
            #if column.endswith(suffix):
                # Suffix entfernen und erneut anhängen, um eindeutige Namen zu gewährleisten
                #new_column_name = column[:-len(suffix)] + suffix
                #new_column_names[column] = new_column_name
    #df.rename(columns=new_column_names, inplace=True)
    #return df


# def merge_data_frame_by_location(df1, df2, criteria=['County Name', 'State']):

     # Erstellen einer Kopie von excel_df, um das Original unverändert zu lassen
    #new_df = df1.copy()
    #if criteria=='FIPS':
        #df2['FIPS']= df2['FIPS'].astype(int)

     # Existierende Suffixe entfernen, falls vorhanden
    #remove_existing_suffixes(new_df)
    #remove_existing_suffixes(df2)

    # Zuerst df_merged mit der Kopie von excel_df mergen, basierend auf gemeinsamen Spalten
    #updated_df = pd.merge(new_df, df2, on=criteria, how='left', suffixes=('_left', '_right'))

    #return updated_df

# def merge_data_frames_by_location(df, criteria=['County Name', 'State']):

    #df0= df[0]

    #for i in range (1,len(df)):
        #df0= merge_data_frame_by_location(df0, df[i], criteria)

    #return df0

# merge_data_frames_by_location([excel_df, getAccesstoExerciseOpportunities(year), getPatientSatisfaction(year)])

# def missing_values_average(df): 
    #for i in range(0,len(df.columns)):
        #column_name = df.columns[i]
        #if df.dtypes[i] in [int, float]:
            #df[column_name].fillna(df[column_name].mean(), inplace=True)
    #return df 

# Laden der Excel-Datei in einen DataFrame
# df_base = pd.read_excel('/Users/jasmin/Desktop/Livability Score Data/Allgemein/US_FIPS_Codes.xls', header=1)
# df_final = df_base.copy()
# df_final = merge_data_frame_by_location(df_final, getAccesstoExerciseOpportunities(year))
# # df_final = merge_data_frame_by_location(df_final, getPatientSatisfaction(year))
# df_final = merge_data_frame_by_location(df_final, getPreventableHospitalizationRate(year))
# df_final = merge_data_frame_by_location(df_final, getSmokingPrevalence(year), 'FIPS')
# df_final = merge_data_frame_by_location(df_final, getObesityPrevalence(year), 'FIPS')
# df_final = missing_values_average(df_final)
# print (df_final)
# df_final.to_csv(f'FinalHealthData{year}.csv', index=False)


# class Group:
    # def __init__(self,destinationname, sourcenames):
        # self.destinationname = destinationname
        # self.sourcenames = sourcenames
# groups = [Group('Health Score',['Satisfaction_Rank_Percentage', 'Inverse_Smoking_Prevalence', 'Inverse_Obesity_Prevalence', 'Inverted_Hospitalization_Rate_Rank_Percentage', 'Access_Exercise_Rank_Percentage']), 
#           ]
