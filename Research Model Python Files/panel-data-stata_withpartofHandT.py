import pandas as pd
import re
import os



# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Eine Ebene nach oben navigieren
parent_dir = os.path.dirname(base_dir)

# Dynamischer Pfad zur CSV-Datei
file_path = os.path.join(parent_dir, 'All Variables merged', 'Gefilterte_Daten_2015_2019_Standorte_dynamicPartsofHandT.csv')
# Zuerst die Daten laden und relevante Spalten auswählen
data = pd.read_csv(file_path)

# Entferne alle Spalten, die 'Percentile' im Namen haben
data = data.loc[:, ~data.columns.str.contains('Percentile')]

# Melt the dataframe to combine all the Count columns into one
melted_count_data = pd.melt(data, 
                      id_vars=[col for col in data.columns if not col.startswith('Count_')],
                      value_vars=[col for col in data.columns if col.startswith('Count_')],
                      var_name='Year_Var',
                      value_name='Count')

# Extrahiere das Jahr aus der 'Year_Var' Spalte
melted_count_data['Year_Var'] = melted_count_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen
final_count_data = melted_count_data[melted_count_data['Year'] == melted_count_data['Year_Var']]

# Entferne die 'Year_Var' Spalte
final_count_data = final_count_data.drop(columns=['Year_Var'])

# ---- Alter Code: Verarbeitung der Count-Spalten ----
# Identifiziere die Count-Spalten (Spalten, die mit 'Count_' beginnen)
count_columns = [col for col in data.columns if col.startswith('Count_')]

# Schmelze den DataFrame, um die Count-Spalten zu einer Spalte zusammenzufassen
melted_count_data = pd.melt(data, 
                            id_vars=[col for col in data.columns if col not in count_columns],
                            value_vars=count_columns,
                            var_name='Year_Var',
                            value_name='Count')

# Extrahiere das Jahr aus der 'Year_Var' Spalte für Count-Daten
melted_count_data['Year_Var'] = melted_count_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen für Count-Daten
final_count_data = melted_count_data[melted_count_data['Year'] == melted_count_data['Year_Var']]

# Entferne die 'Year_Var' Spalte aus den Count-Daten
final_count_data = final_count_data.drop(columns=['Year_Var'])

# ---- Neuer Code: Verarbeitung der AvgMobyScore-Spalten ----
# Identifiziere die AvgMobyScore-Spalten (Spalten, die mit 'AvgMobyScore_' beginnen)
avgmoby_columns = [col for col in data.columns if col.startswith('AvgMobyScore_')]

# Schmelze den DataFrame, um die AvgMobyScore-Spalten zu einer Spalte zusammenzufassen
melted_avgmoby_data = pd.melt(data, 
                              id_vars=[col for col in data.columns if col not in avgmoby_columns],
                              value_vars=avgmoby_columns,
                              var_name='Year_Var',
                              value_name='AvgMobyScore')

# Extrahiere das Jahr aus der 'Year_Var' Spalte für AvgMobyScore-Daten
melted_avgmoby_data['Year_Var'] = melted_avgmoby_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen für AvgMobyScore-Daten
final_avgmoby_data = melted_avgmoby_data[melted_avgmoby_data['Year'] == melted_avgmoby_data['Year_Var']]

# Entferne die 'Year_Var' Spalte aus den AvgMobyScore-Daten
final_avgmoby_data = final_avgmoby_data.drop(columns=['Year_Var'])

# Merge der beiden finalen DataFrames auf gemeinsamen Spalten
common_columns = [col for col in final_count_data.columns if col in final_avgmoby_data.columns and col not in ['Count', 'AvgMobyScore']]
final_data = pd.merge(final_count_data, final_avgmoby_data, on=common_columns, how='outer')

# Entferne die angegebenen Spalten am Ende
columns_to_remove = [
    'AvgMobyScore_2019', 'AvgMobyScore_2015', 'total_incompany_2015', 
    'AvgMobyScore_2016', 'total_incompany_2016', 'AvgMobyScore_2018', 
    'total_incompany_2018', 'AvgMobyScore_2017', 'total_incompany_2017', 
    'Combined_Index_2019', 'Combined_Index_2015', 'Combined_Index_2016', 
    'Combined_Index_2018', 'Combined_Index_2017', 'Count_2019', 'Count_2015', 
    'Count_2016', 'Count_2018', 'Count_2017'
]

final_data = final_data.drop(columns=columns_to_remove, errors='ignore')

# Dynamischer Pfad zur Ausgabe-CSV-Datei
output_file_path = os.path.join(parent_dir, 'Stata', 'Gefilterte_Daten_2015_2019_Standorte_dynamic_StataPartsofHandT.csv')

# Save the transformed data to a new CSV file
final_data.to_csv(output_file_path, index=False)






# Dynamischer Pfad zur CSV-Datei
path = os.path.join(parent_dir, 'All Variables merged', 'Gefilterte_Daten_2015_2019_dynamicPartsofHandT.csv')

# Zuerst die Daten laden und relevante Spalten auswählen
data = pd.read_csv(path)

# Entferne alle Spalten, die 'Percentile' im Namen haben
data = data.loc[:, ~data.columns.str.contains('Percentile')]

# Melt the dataframe to combine all the Count columns into one
melted_count_data = pd.melt(data, 
                      id_vars=[col for col in data.columns if not col.startswith('Count_')],
                      value_vars=[col for col in data.columns if col.startswith('Count_')],
                      var_name='Year_Var',
                      value_name='Count')

# Extrahiere das Jahr aus der 'Year_Var' Spalte
melted_count_data['Year_Var'] = melted_count_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen
final_count_data = melted_count_data[melted_count_data['Year'] == melted_count_data['Year_Var']]

# Entferne die 'Year_Var' Spalte
final_count_data = final_count_data.drop(columns=['Year_Var'])

# ---- Alter Code: Verarbeitung der Count-Spalten ----
# Identifiziere die Count-Spalten (Spalten, die mit 'Count_' beginnen)
count_columns = [col for col in data.columns if col.startswith('Count_')]

# Schmelze den DataFrame, um die Count-Spalten zu einer Spalte zusammenzufassen
melted_count_data = pd.melt(data, 
                            id_vars=[col for col in data.columns if col not in count_columns],
                            value_vars=count_columns,
                            var_name='Year_Var',
                            value_name='Count')

# Extrahiere das Jahr aus der 'Year_Var' Spalte für Count-Daten
melted_count_data['Year_Var'] = melted_count_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen für Count-Daten
final_count_data = melted_count_data[melted_count_data['Year'] == melted_count_data['Year_Var']]

# Entferne die 'Year_Var' Spalte aus den Count-Daten
final_count_data = final_count_data.drop(columns=['Year_Var'])

# ---- Neuer Code: Verarbeitung der AvgMobyScore-Spalten ----
# Identifiziere die AvgMobyScore-Spalten (Spalten, die mit 'AvgMobyScore_' beginnen)
avgmoby_columns = [col for col in data.columns if col.startswith('AvgMobyScore_')]

# Schmelze den DataFrame, um die AvgMobyScore-Spalten zu einer Spalte zusammenzufassen
melted_avgmoby_data = pd.melt(data, 
                              id_vars=[col for col in data.columns if col not in avgmoby_columns],
                              value_vars=avgmoby_columns,
                              var_name='Year_Var',
                              value_name='AvgMobyScore')

# Extrahiere das Jahr aus der 'Year_Var' Spalte für AvgMobyScore-Daten
melted_avgmoby_data['Year_Var'] = melted_avgmoby_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen für AvgMobyScore-Daten
final_avgmoby_data = melted_avgmoby_data[melted_avgmoby_data['Year'] == melted_avgmoby_data['Year_Var']]

# Entferne die 'Year_Var' Spalte aus den AvgMobyScore-Daten
final_avgmoby_data = final_avgmoby_data.drop(columns=['Year_Var'])

# Merge der beiden finalen DataFrames auf gemeinsamen Spalten
common_columns = [col for col in final_count_data.columns if col in final_avgmoby_data.columns and col not in ['Count', 'AvgMobyScore']]
final_data = pd.merge(final_count_data, final_avgmoby_data, on=common_columns, how='outer')

# Entferne die angegebenen Spalten am Ende
columns_to_remove = [
    'AvgMobyScore_2019', 'AvgMobyScore_2015', 'total_incompany_2015', 
    'AvgMobyScore_2016', 'total_incompany_2016', 'AvgMobyScore_2018', 
    'total_incompany_2018', 'AvgMobyScore_2017', 'total_incompany_2017', 
    'Combined_Index_2019', 'Combined_Index_2015', 'Combined_Index_2016', 
    'Combined_Index_2018', 'Combined_Index_2017', 'Count_2019', 'Count_2015', 
    'Count_2016', 'Count_2018', 'Count_2017'
]

final_data = final_data.drop(columns=columns_to_remove, errors='ignore')


output_path = os.path.join(parent_dir, 'All Variables merged', 'not used', 'Gefilterte_Daten_2015_2019_dynamic_StataPartsofHandT.csv')
# Save the transformed data to a new CSV file
final_data.to_csv(output_path, index=False)



# Dynamischer Pfad zur CSV-Datei
datapath = os.path.join(parent_dir, 'All Variables merged', 'cleaned-merged_salaries_all_locations_years_with_index_dynamic_PartsofHandT.csv')

# Zuerst die Daten laden und relevante Spalten auswählen
data = pd.read_csv(datapath)

# Entferne alle Spalten, die 'Percentile' im Namen haben
data = data.loc[:, ~data.columns.str.contains('Percentile')]

# Melt the dataframe to combine all the Count columns into one
melted_count_data = pd.melt(data, 
                      id_vars=[col for col in data.columns if not col.startswith('Count_')],
                      value_vars=[col for col in data.columns if col.startswith('Count_')],
                      var_name='Year_Var',
                      value_name='Count')

# Extrahiere das Jahr aus der 'Year_Var' Spalte
melted_count_data['Year_Var'] = melted_count_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen
final_count_data = melted_count_data[melted_count_data['Year'] == melted_count_data['Year_Var']]

# Entferne die 'Year_Var' Spalte
final_count_data = final_count_data.drop(columns=['Year_Var'])

# ---- Alter Code: Verarbeitung der Count-Spalten ----
# Identifiziere die Count-Spalten (Spalten, die mit 'Count_' beginnen)
count_columns = [col for col in data.columns if col.startswith('Count_')]

# Schmelze den DataFrame, um die Count-Spalten zu einer Spalte zusammenzufassen
melted_count_data = pd.melt(data, 
                            id_vars=[col for col in data.columns if col not in count_columns],
                            value_vars=count_columns,
                            var_name='Year_Var',
                            value_name='Count')

# Extrahiere das Jahr aus der 'Year_Var' Spalte für Count-Daten
melted_count_data['Year_Var'] = melted_count_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen für Count-Daten
final_count_data = melted_count_data[melted_count_data['Year'] == melted_count_data['Year_Var']]

# Entferne die 'Year_Var' Spalte aus den Count-Daten
final_count_data = final_count_data.drop(columns=['Year_Var'])

# ---- Neuer Code: Verarbeitung der AvgMobyScore-Spalten ----
# Identifiziere die AvgMobyScore-Spalten (Spalten, die mit 'AvgMobyScore_' beginnen)
avgmoby_columns = [col for col in data.columns if col.startswith('AvgMobyScore_')]

# Schmelze den DataFrame, um die AvgMobyScore-Spalten zu einer Spalte zusammenzufassen
melted_avgmoby_data = pd.melt(data, 
                              id_vars=[col for col in data.columns if col not in avgmoby_columns],
                              value_vars=avgmoby_columns,
                              var_name='Year_Var',
                              value_name='AvgMobyScore')

# Extrahiere das Jahr aus der 'Year_Var' Spalte für AvgMobyScore-Daten
melted_avgmoby_data['Year_Var'] = melted_avgmoby_data['Year_Var'].str.extract(r'(\d{4})').astype(int)

# Filtere die Zeilen, die das Jahr in der 'Year' Spalte entsprechen für AvgMobyScore-Daten
final_avgmoby_data = melted_avgmoby_data[melted_avgmoby_data['Year'] == melted_avgmoby_data['Year_Var']]

# Entferne die 'Year_Var' Spalte aus den AvgMobyScore-Daten
final_avgmoby_data = final_avgmoby_data.drop(columns=['Year_Var'])

# Merge der beiden finalen DataFrames auf gemeinsamen Spalten
common_columns = [col for col in final_count_data.columns if col in final_avgmoby_data.columns and col not in ['Count', 'AvgMobyScore']]
final_data = pd.merge(final_count_data, final_avgmoby_data, on=common_columns, how='outer')

# Entferne die angegebenen Spalten am Ende
columns_to_remove = [
    'AvgMobyScore_2019', 'AvgMobyScore_2015', 'total_incompany_2015', 
    'AvgMobyScore_2016', 'total_incompany_2016', 'AvgMobyScore_2018', 
    'total_incompany_2018', 'AvgMobyScore_2017', 'total_incompany_2017', 
    'Combined_Index_2019', 'Combined_Index_2015', 'Combined_Index_2016', 
    'Combined_Index_2018', 'Combined_Index_2017', 'Count_2019', 'Count_2015', 
    'Count_2016', 'Count_2018', 'Count_2017'
]

final_data = final_data.drop(columns=columns_to_remove, errors='ignore')


output_data = os.path.join(parent_dir, 'All Variables merged', 'not used', 'cleaned-merged_salaries_all_locations_years_with_index_dynamicPartsofHandT_Stata.csv')
# Save the transformed data to a new CSV file
final_data.to_csv(output_data, index=False)
