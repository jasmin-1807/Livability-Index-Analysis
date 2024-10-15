import csv
from fuzzywuzzy import fuzz
import pandas as pd
import os

# Funktion zum Einlesen der Daten aus einer CSV-Datei und Erfassen aller Spaltennamen
def read_csv_with_all_columns(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        column_names = reader.fieldnames  # Erfassen der Spaltennamen
        for row in reader:
            data.append(row)
    return data, column_names

# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Eine Ebene nach oben navigieren
parent_dir = os.path.dirname(base_dir)

# Dynamische Pfade für die CSV-Dateien
merged_data_path = os.path.join(parent_dir, 'Merged Salary & CoL Data', 'Salaries_Counties_All_Locations_Years_StateMean_With_Scores_andIndex_Parts_of_T_H.csv')
companies2_path = os.path.join(parent_dir, 'cross-year files', 'mobygames_20231028.csv')
company_size_path = os.path.join(parent_dir, 'cross-year files', 'company-size.csv')


# Lese die Daten aus den CSV-Dateien ein
merged_data, merged_data_columns = read_csv_with_all_columns(merged_data_path)
companies2, _ = read_csv_with_all_columns(companies2_path)
company_size, _ = read_csv_with_all_columns(company_size_path)

# Entfernen von Zeilen, bei denen 'experience_company' das Wort 'power' enthält
company_size = [row for row in company_size if 'power' not in row['experience_company'].lower()]

# Liste der Begriffe, die in company1 enthalten sein sollen, um die Zeile zu löschen
delete_terms_company1 = [
    "UTILITY DATA CONTRACTORS INC", "SKILLZDEPOT INC", "KNIGHTSBRIDGE PROPERTIES CORP",
    "MODUS ASSOCIATES LLC", "MODUS OPERATIONS LLC", "MODUS OPS LLC", "SEGAL NYC LLC",
    "SEGANTII CAPITAL MANAGEMENT (USA) LLC", "STEAMBOAT CAPITAL PARTNERS LLC",
    "UTILITY PROGRAMS & METERING II", "EXTREME VENTURES INC", "SEGANTEK ENGINEERING",
    "UTILITY GLOBAL INC", "UTILITY CONNECTIONS INCORPORATED", "UTILITY SOLUTIONS PARTNERS",
    "LATITUDE36 INC", "MODUS HEALTH GROUP INC", "UTILITY SYSTEMS SCIENCE & SOFTWARE INC",
    "UTILITY SYSTEMS SCIENCE AND SOFTWARE", "UTILITY SYSTEMS SCIENCE AND SOFTWARE INC",
    "MODUS GROUP LLC", "MODUS ACUPUNCTURE", "EXTREME EROSION CONTROL LLC", "SEGAL DRUG TRIALS INC",
    "UTILITY SYSTEMS CONSTRUCTION & ENGINEERING LLC", "SEGAMI CORPORATION",
    "UTILITY PARTNERS OF AMERICA LLC", "STEAM LOGISTICS LLC", "LATITUDE BUILDERS", "LATITUDE LLC",
    "SEGAL INSTITUTE FOR CLINICAL RESEARCH INC", "MODUSLINK COPORATION", "UTILITY SOLUTIONS PARTNERS LLC",
    "LATITUDE GEOGRAPHICS USA INC", "THE METAL SURGEON", "EXENTUS CORPORATION", "STEAMATIC LLC",
    "OCULUS HEALTH", "MODUSBOX INC", "EXTREME SCALE SOLUTIONS LLC", "EXTREME WAVES INC",
    "LATITUDE PHARMACEUTICALS INC", "LATITUDE WINES INC", "CYANCO INTERNATIONAL LLC",
    "UTILITY CONSUMER ANALYTICS INC", "EXTREME AUTOMATION INC", "UTILITY TREE SERVICE LLC",
    "COLONY CABINETS INC", "COLONY DISPLAY LLC", "EXTREME I INC", "DIVERSIFIED MATERIAL SPECIALISTS INC",
    "EXTREME EXTERIORS", "EXTREME GETAWAY", "EXTREME MACHINE AND FABRICATING INC",
    "EXTREME STEEL INCORPORATED", "LATITUDE SOFT TECHNOLOGIES LLC", "LATITUDE 36 FOODS LLC",
    "LATITUDE 36 INC", "LATITUDE 38 VACATION RENTALS", "LATITUDE CONSULTING GROUP INC",
    "LATITUDE MANAGEMENT INC", "MODUS STUDIO PLLC", "MODUSLINK CORPORATION",
    "STEAMBOAT SPRINGS WINTER SPORTS CLUB INC", "THE MIRROR THEATER LTD", "THE MIRROR THEATHER LTD",
    "THERE DOES NOT EXIST LLC", "UTILITY CONCRETE PRODUCTS LLC", "UTILITY MAPPING SERVICES INC",
    "UTILITY TRUCKS & EQUIPMENT INC", "DIVERSIFIED HOME CARE INC", "PIPELINE SUCCESS INC"
]

# Funktion zum Löschen der Zeilen basierend auf den Bedingungen und Einfügen der dynamischen Spalten
def delete_rows_dynamic(merged_data, companies2, company_size, delete_terms_company1):
    cleaned_merged_data = []
    for entry in merged_data:
        company1 = entry['company'].lower()
        if any(term.lower() in company1 for term in delete_terms_company1):
            continue  # Überspringen der Zeile, wenn einer der Begriffe in company1 enthalten ist

             # Bestimmeen des Jahrs für die dynamischen Spalten
        year = entry.get('Year', '2019')  # Fallback auf 2019, falls Jahr nicht vorhanden

        company2 = next((row for row in companies2 if fuzz.partial_ratio(company1, row['company'].lower()) == 100), None)
        if company2 is not None and "advanced" in company2['company'].lower():
            continue  # Überspringen der Zeile, wenn "advanced" in company2 enthalten ist

         # Fuzzy-Suche in company_size
        size_entry = next((row for row in company_size if fuzz.partial_ratio(company1, row['experience_company'].lower()) == 100 and row['year'] == year), None)
    
    
        # Hinzufügen der zusätzlichen Spalten, falls vorhanden
        count_col = f'Count_{year}'
        avg_moby_col = f'AvgMobyScore_{year}'
        incompany_col = 'total_incompany'
        
        if company2:
            entry[count_col] = company2.get(count_col, '')
            entry[avg_moby_col] = company2.get(avg_moby_col, '')
        else:
            entry[count_col] = ''
            entry[avg_moby_col] = ''

        if size_entry:
            entry[incompany_col] = size_entry.get('total_incompany', '')
        else:
            entry[incompany_col] = ''

            # Füge experience_company hinzu
        entry['experience_company'] = company2.get('experience_company', '') if company2 else ''
        
        cleaned_merged_data.append(entry)
    return cleaned_merged_data

# Löschen der Zeilen und hinzufügen der neuen Spalten 
cleaned_merged_data = delete_rows_dynamic(merged_data, companies2, company_size, delete_terms_company1)

# Konvertieren der bereinigten Daten in ein pandas DataFrame
df_cleaned = pd.DataFrame(cleaned_merged_data)

# Dynamische Perzentile und kombinierter Index basierend auf den Jahren
years = df_cleaned['Year'].unique()

for year in years:
    count_col = f'Count_{year}'
    avg_moby_col = f'AvgMobyScore_{year}'
    
    if count_col in df_cleaned.columns and avg_moby_col in df_cleaned.columns:
        df_cleaned[f'{count_col}_Percentile'] = df_cleaned[count_col].rank(pct=True) * 100
        df_cleaned[f'{avg_moby_col}_Percentile'] = df_cleaned[avg_moby_col].rank(pct=True) * 100

        df_cleaned[f'Combined_Index_{year}'] = (df_cleaned[f'{count_col}_Percentile'] + df_cleaned[f'{avg_moby_col}_Percentile']) / 2

# Speichern als CSV-Datei
# Dynamischer Pfad zur CSV-Datei, die gespeichert werden soll
output_file_dynamic = os.path.join(parent_dir, 'All Variables merged', 'not used', 'cleaned_merged_salaries_all_locations_years_with_index_dynamic_PartsofHandT.csv')
df_cleaned.to_csv(output_file_dynamic, index=False, encoding='utf-8')

output_file_dynamic



# Dateipfad für den bereinigten Datensatz
#output_file = 'cleaned_merged_salaries.csv'

# Exportiere den bereinigten Datensatz als CSV-Datei
#with open(output_file, 'w', newline='', encoding='utf-8') as file:
    #writer = csv.DictWriter(file, fieldnames=merged_data_columns + ['Count_2019', 'AvgMobyScore_2019', 'total_incompany_2019'])
    #writer.writeheader()
    #writer.writerows(cleaned_merged_data)

#print(f"Bereinigter Datensatz wurde erfolgreich als '{output_file}' exportiert.")
