import pandas as pd 
import os

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





    
# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Eine Ebene nach oben navigieren
parent_dir = os.path.dirname(base_dir)

# Dynamischer Pfad zur CSV-Datei
pfad_zum_datensatz = os.path.join(parent_dir, 'cross-year files', 'merged_salaries_all (1).csv')

# Laden des Datensatzes in ein DataFrame
df = pd.read_csv(pfad_zum_datensatz)

# Entfernen des Tausendertrennzeichens (Komma) und Konvertierung in numerischen Typ
df['salary'] = df['salary'].str.replace(',', '').astype(float)

# Extrahieren des Jahres aus der 'start_date'-Spalte
df['start_year'] = df['start_date'].str[-4:].astype(int)

# Filtern der Daten für die Jahre 2015 bis 2019
df = df[(df['start_year'] >= 2015) & (df['start_year'] <= 2019)]

# Gruppierung nach Unternehmen und Standort und Berechnung des Durchschnittslohns pro Standort
# grouped = df.groupby(['company', 'location'])['salary'].mean().reset_index(name='mean_salary')

# Gruppierung nach Unternehmen, Standort und Jahr sowie Berechnung des Durchschnittslohns und der Anzahl der Einträge pro Standort und Jahr
grouped = df.groupby(['company', 'location', 'start_year']).agg({'salary': 'mean', 'location': 'size'}).rename(columns={'location': 'count'}).reset_index()


# Dynamischer Pfad zur Ausgabe-CSV-Datei
output_path = os.path.join(parent_dir, 'research model interim files', 'mean-salary_all_locations_years.csv')
# Speichern des Ergebnisses als CSV-Datei
grouped.to_csv(output_path, index=False)

print(grouped)






# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Eine Ebene nach oben navigieren
parent_dir = os.path.dirname(base_dir)

# Dynamischer Pfad zur CSV-Datei
pfad_zum_datensatz1 = os.path.join(parent_dir, 'research model interim files', 'mean-salary_all_locations_years.csv')

# Laden des Datensatzes in ein DataFrame und Auswahl der Spalte "County"
df1 = pd.read_csv(pfad_zum_datensatz1)


pfad_zum_datensatz2 = os.path.join(parent_dir, 'cross-year files', 'All_Locations_Unique.xlsx')

# Laden des Datensatzes in ein DataFrame und Auswahl der Spalte "County"
df2 = pd.read_excel(pfad_zum_datensatz2)

# Merge der DataFrames basierend auf der Spalte "location"
merged_df = pd.merge(df1, df2, on='location')

# Umbenennen der Spalte "County" zu "County Name"
merged_df.rename(columns={'County': 'County Name'}, inplace=True)

# Umbenennen der Spalte "State" in "State Abbr."
merged_df.rename(columns={'State': 'State Abbr.'}, inplace=True)

# Sicherstellen, dass es keine NaN-Werte in der 'State Abbr.'-Spalte gibt
merged_df['State Abbr.'] = merged_df['State Abbr.'].fillna('')

# Entfernen von Leerzeichen und Kommas in der Spalte "State Abbr."
merged_df['State Abbr.'] = merged_df['State Abbr.'].str.replace(' ', '').str.replace(',', '')

# Anwenden der Funktion auf die Spalte "State" und Erstellen einer neuen Spalte "State"
merged_df['State'] = merged_df['State Abbr.'].apply(state_code_to_name)

output_path = os.path.join(parent_dir, 'research model interim files', 'Salaries_Counties_All_Locations_Years.csv')

# Speichern des Ergebnisses als CSV-Datei
merged_df.to_csv(output_path, index=False)

# Ausgabe des zusammengeführten DataFrames
print(merged_df)


# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Eine Ebene nach oben navigieren
parent_dir = os.path.dirname(base_dir)

# Dynamischer Pfad zur CSV-Datei
file_path = os.path.join(parent_dir, 'research model interim files', 'Salaries_Counties_All_Locations_Years.csv')

# Laden des Datensatzes mit den Gehaltsinformationen
salaries_df = pd.read_csv(file_path)

# Führende Leerzeichen aus der Spalte "County Name" entfernen
salaries_df['County Name'] = salaries_df['County Name'].str.strip()

# Umbenennen der Spalte 'start_year' in 'Year'
salaries_df.rename(columns={'start_year': 'Year'}, inplace=True)

# Filtern der Zeile mit County Name Los Angeles und State California
los_angeles_row1 = salaries_df[(salaries_df['County Name'] == 'Los Angeles') & (salaries_df['State'] == 'California')]
print(len(los_angeles_row1))
# Ausgabe der gefilterten Zeile
print(los_angeles_row1)

# Dynamischer Pfad zum Unterordner "Final Category Scores With Parts of H & T"
scores_folder = os.path.join(parent_dir, 'Category Scores With Parts of Housing & Transp')

# Laden der Score-Daten für jedes Jahr aus dem Unterordner
scores_2015 = pd.read_csv(os.path.join(scores_folder,'FinalCategoryScores_StateMean_WithPartofHousingandTransportation2015.csv'))
scores_2016 = pd.read_csv(os.path.join(scores_folder,'FinalCategoryScores_StateMean_WithPartofHousingandTransportation2016.csv'))
scores_2017 = pd.read_csv(os.path.join(scores_folder,'FinalCategoryScores_StateMean_WithPartofHousingandTransportation2017.csv'))
scores_2018 = pd.read_csv(os.path.join(scores_folder,'FinalCategoryScores_StateMean_WithPartofHousingandTransportation2018.csv'))
scores_2019 = pd.read_csv(os.path.join(scores_folder,'FinalCategoryScores_StateMean_WithPartofHousingandTransportation2019.csv'))

# Hinzufügen einer Jahr-Spalte zu jedem Score-Datensatz
scores_2015['Year'] = 2015
scores_2016['Year'] = 2016
scores_2017['Year'] = 2017
scores_2018['Year'] = 2018
scores_2019['Year'] = 2019


# Kombinieren aller Score-Datensätze zu einem einzigen DataFrame
all_scores_df = pd.concat([scores_2015, scores_2016, scores_2017, scores_2018, scores_2019])

# Merge der DataFrames basierend auf "County Name" und "State"
merged_df = pd.merge(salaries_df, all_scores_df, on=['County Name', 'State', 'Year'], how='inner')


 # Dynamischer Pfad zum Unterordner 
output_path = os.path.join(parent_dir, 'research model interim files','Salaries_Counties_All_Locations_Years_With_Scores_StateMean_Parts_of_T_H.csv')
# Speichern des Ergebnisses als CSV-Datei
merged_df.to_csv(output_path, index=False)


# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Eine Ebene nach oben navigieren
parent_dir = os.path.dirname(base_dir)

# Dynamischer Pfad zur CSV-Datei
csv_file_path = os.path.join(parent_dir, 'research model interim files', 'Salaries_Counties_All_Locations_Years_With_Scores_StateMean_Parts_of_T_H.csv')

# Lade die CSV-Datei
df_csv = pd.read_csv(csv_file_path)

# Lade die Excel-Datei, speziell Tabellenblatt 2
excel_file = os.path.join(parent_dir, 'cross-year files', 'Numbeo_CostofLiving_Counties_.xlsx')
df_excel = pd.read_excel(excel_file, sheet_name=0)  # sheet_name=1, da Python bei 0 zu zählen beginnt

# Sicherstellen, dass beide DataFrames eine Spalte 'FIPS' haben
print(df_csv.columns)
print(df_excel.columns)

# Berechnen des Mittelwerts des Cost of Living Index für jedes FIPS und Jahr
df_excel_mean = df_excel.groupby(['FIPS', 'Year']).agg({'Cost of Living Index': 'mean'}).reset_index()

# Überprüfen auf Duplikate in df_excel
df_excel_duplicates = df_excel_mean[df_excel.duplicated(subset=['FIPS', 'Year'], keep=False)]
print(f"Duplikate in df_excel:\n{df_excel_duplicates}")


merged_df = pd.merge(df_csv, df_excel_mean[['FIPS', 'Year', 'Cost of Living Index']], on=['FIPS', 'Year'], how='left')


merged_df.head()


# Dynamischer Pfad zum Unterordner (du kannst den Pfad anpassen, falls nötig)
output = os.path.join(parent_dir, 'Merged Salary & CoL Data','Salaries_Counties_All_Locations_Years_StateMean_With_Scores_andIndex_Parts_of_T_H.csv')
# Speichern des Ergebnisses als CSV-Datei
merged_df.to_csv(output, index=False)


