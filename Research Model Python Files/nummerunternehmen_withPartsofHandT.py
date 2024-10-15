import pandas as pd
import os

# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Eine Ebene nach oben navigieren
parent_dir = os.path.dirname(base_dir)

# Dynamischer Pfad zur CSV-Datei
file_path = os.path.join(parent_dir, 'All Variables merged', 'not used', 'cleaned_merged_salaries_all_locations_years_with_index_dynamic_PartsofHandT.csv')

df = pd.read_csv(file_path)

# Entfernen der Firma "RUST-OLEUM CORPORATION" aus der Spalte "company"
df = df[df['company'] != 'RUST-OLEUM CORPORATION']

# Dynamischer Pfad zur CSV-Datei
output_path = os.path.join(parent_dir, 'All Variables merged', 'cleaned-merged_salaries_all_locations_years_with_index_dynamic_PartsofHandT.csv')
# Speichern des aktualisierten Datensatzes ohne "RUST-OLEUM CORPORATION"
df.to_csv(output_path, index=False)

# Filtern der Daten für den Zeitraum 2015-2019

# Zählen der Anzahl der eindeutigen Unternehmen
num_companies = df['company'].nunique()
print(f"Anzahl der Unternehmen: {num_companies}")
# Anzahl der eindeutigen Unternehmen für jedes Jahr zählen
unique_companies_per_year = df.groupby('Year')['company'].nunique().reset_index()

# Umbenennen der Spalten für bessere Lesbarkeit
unique_companies_per_year.columns = ['Year', 'Number of Companies']

# Ausgabe der Anzahl der Unternehmen pro Jahr
print(unique_companies_per_year)

# Funktion zur Zählung der eindeutigen Unternehmen, die in jedem Jahr eines bestimmten Zeitraums einen Eintrag haben
def count_unique_companies_all_years(start_year, end_year):
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    year_range = end_year - start_year + 1
    companies_with_all_years = filtered_df.groupby('company')['Year'].nunique()
    return companies_with_all_years[companies_with_all_years == year_range].count()

# Anzahl der Unternehmen für verschiedene Zeiträume
count_2015_2019 = count_unique_companies_all_years(2015, 2019)
count_2016_2019 = count_unique_companies_all_years(2016, 2019)
count_2017_2019 = count_unique_companies_all_years(2017, 2019)
count_2018_2019 = count_unique_companies_all_years(2018, 2019)

# Ausgabe der Ergebnisse
print(f"Anzahl der Unternehmen von 2015 bis 2019: {count_2015_2019}")
print(f"Anzahl der Unternehmen von 2016 bis 2019: {count_2016_2019}")
print(f"Anzahl der Unternehmen von 2017 bis 2019: {count_2017_2019}")
print(f"Anzahl der Unternehmen von 2018 bis 2019: {count_2018_2019}")


# Filtern der Daten für den Zeitraum 2015-2019
filtered_df = df[(df['Year'] >= 2015) & (df['Year'] <= 2019)]

# Gruppieren nach Unternehmen und Zählen der Einträge pro Unternehmen für die Jahre 2015-2019
company_year_counts = filtered_df.groupby('company')['Year'].nunique()

# Beibehalten der Unternehmen, die in jedem Jahr von 2015 bis 2019 Einträge haben (also 5 Jahre)
valid_companies = company_year_counts[company_year_counts == 5].index


# Filtern des ursprünglichen DataFrames, um nur die validen Unternehmen zu behalten
final_filtered_df = filtered_df[filtered_df['company'].isin(valid_companies)]

# Anzahl der eindeutigen Unternehmen zählen
num_valid_companies = final_filtered_df['company'].nunique()

print(f"Anzahl der Unternehmen von 2015 bis 2019: {num_valid_companies}")

# Dynamischer Pfad zur CSV-Datei
output = os.path.join(parent_dir, 'All Variables merged', 'Gefilterte_Daten_2015_2019_dynamicPartsofHandT.csv')
# Exportieren der gefilterten Daten in eine neue CSV-Datei
final_filtered_df.to_csv(output, index=False)

# Optional: Anzeigen der ersten Zeilen des gefilterten DataFrames
print(final_filtered_df.head())

# Zusätzlicher Schritt: Filtern der Daten für Unternehmen, die in jedem Standort in jedem Jahr von 2015 bis 2019 Einträge haben
# Gruppieren nach Unternehmen und Standort und Zählen der Einträge pro Unternehmen-Standort-Kombination für die Jahre 2015-2019
company_location_year_counts = filtered_df.groupby(['company', 'location'])['Year'].nunique()

# Beibehalten der Unternehmen-Standort-Kombinationen, die in jedem Jahr von 2015 bis 2019 Einträge haben (also 5 Jahre)
valid_company_locations = company_location_year_counts[company_location_year_counts == 5].reset_index()[['company', 'location']]

# Zusammenführen mit dem ursprünglichen DataFrame, um nur die validen Unternehmen-Standort-Kombinationen zu behalten
final_location_filtered_df = filtered_df.merge(valid_company_locations, on=['company', 'location'], how='inner')

# Anzahl der eindeutigen Unternehmen zählen, die für jeden Standort in jedem Jahr von 2015 bis 2019 Einträge haben
num_valid_location_companies = final_location_filtered_df['company'].nunique()

print(f"Anzahl der Unternehmen, die in jedem Standort von 2015 bis 2019 Einträge haben: {num_valid_location_companies}")

# Dynamischer Pfad zur CSV-Datei
outputpath = os.path.join(parent_dir, 'All Variables merged', 'Gefilterte_Daten_2015_2019_Standorte_dynamicPartsofHandT.csv')
# Exportieren der gefilterten Daten in eine neue CSV-Datei
final_location_filtered_df.to_csv(outputpath, index=False)


# Laden des Datensatzes
file_path2 = os.path.join(parent_dir, 'cross-year files', 'Filtered_Companies_2015_2019.csv')
df2 = pd.read_csv(file_path2)

# Entfernen der Firma "RUST-OLEUM CORPORATION" aus der Spalte "company"
df_filtered = df2[df2['company'] != 'RUST-OLEUM CORPORATION']

output_ = os.path.join(parent_dir, 'cross-year files', 'Filtered-Cleaned_Companies_2015_2019_dynamic.csv')
# Optional: Speichern des gefilterten DataFrames in eine neue CSV-Datei
df_filtered.to_csv(output_, index=False)

# Zählen der Anzahl der eindeutigen Unternehmen
num_companies = df_filtered['company'].nunique()
print(f"Anzahl der Unternehmen: {num_companies}")

# Anzeige der ersten Zeilen des gefilterten DataFrames
print(df_filtered.head())









