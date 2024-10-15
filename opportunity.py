import pandas as pd
from os import path 
import numpy as np 
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr
import os

year = 2015 

def rank_percentage(series):
    return series.rank(method='min').apply(lambda x: (x-1) / (len(series)-1) * 100)


def getIncomeInequality(year):

    year_str = str(year)
    
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    csv_path = os.path.join(base_dir, f'{year_str}/Opportunity/Gini_{year_str}.csv')
    df = pd.read_csv(csv_path)

    df = df.filter(['GEO_ID', 'B19083_001E']) 

    # Entfernen der Zeile, in der GEO_ID 'Geography' ist
    df = df.loc[df['GEO_ID'] != 'Geography']

    df['Gini'] = pd.to_numeric(df['B19083_001E'], errors='coerce') * 100

    df['FIPS'] = df['GEO_ID'].str[-5:]

    # df['IncomeInequality_Rank_Percentage'] = rank_percentage(df['Gini'])  # Rangprozente für den Gini-Koeffizienten
    df['Perzentil_IncomeInequality'] = df.groupby(['FIPS'])['Gini'].transform(lambda x: np.percentile(x, 50))

    df['Perzentil_IncomeInequality'] = df['Gini'].rank(pct=True) * 100

    df['Inverted_Perzentil_IncomeInequality'] = 100 - df['Perzentil_IncomeInequality']

    median_value = df['Gini'].median()
    print("Median:", median_value)

    # Ergebnis anzeigen
    print(df[['GEO_ID', 'FIPS', 'Gini', 'Inverted_Perzentil_IncomeInequality']])

    return df 

getIncomeInequality(year)
    

def calculate_mean_from_range(rate):
    if 'GE' in str(rate):
        # Extrahieren des numerischen Teil nach 'GE' 
        return float(rate.replace('GE', ''))
    elif '-' in str(rate):
        # Zerlegen des Strings in Start- und Endwert des Bereichs und Berechnung des Mittelwerts
        start, end = map(int, rate.split('-'))
        return (start + end) / 2
    else:
        # Für normale numerische Werte, direkt zu float konvertieren
        try:
            return float(rate)
        except ValueError:
            # Behandlung von Fällen, in denen die Konversion fehlschlägt, z.B. durch Rückgabe eines NaN-Wertes oder eines spezifischen Platzhalters
            return float('nan')  # oder einen anderen Platzhalterwert, der für Ihre Analyse Sinn macht



def getHighschoolGraduationRate(year):

    year_str = str(year)
    
   # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    csv_path = os.path.join(base_dir, f'{year_str}/Opportunity/Graduation_{year_str}.csv')
    df = pd.read_csv(csv_path)

    # Bereinigen der Spaltennamen
    df.columns = df.columns.str.strip()

    # Anzeige der Spaltennamen
    print("Spaltennamen:", df.columns.tolist())

    print (df.head())

    if year == 2018 or year == 2019:
        rate_column = 'RATE'
    elif year == 2017:
        rate_column = 'ALL_RATE_1718'
    elif year == 2016:
        rate_column = 'ALL_RATE_1617'
    elif year == 2015:
        rate_column = 'ALL_RATE_1516'
    else:
        raise ValueError(f"Rate column for year {year} is not defined")
    
    # Überprüfen, ob die Spalte existiert
    if rate_column not in df.columns:
        raise KeyError(f"Spalte '{rate_column}' nicht gefunden in {year}.")

    # Umbenennen der Spalte in "RATE"
    df.rename(columns={rate_column: 'RATE'}, inplace=True)

    if year == 2018 or year == 2019:
        filtered_df = df[df['CATEGORY'] == 'ALL'].copy()
    else:
        filtered_df = df.copy()  # Für andere Jahre die Filterbedingung überspringen

     # Filtern nach den Zeilen, die "County" enthalten
    filtered_df = filtered_df[filtered_df['LEANM'].str.contains('County', na=False)].copy()

    # 'County' entfernen, um nur noch den County Namen zu erhalten
    filtered_df.loc[:, 'LEANM'] = filtered_df['LEANM'].str.replace('County.*', '', regex=True).str.strip()
    # Schreibweise von State Name ändern
    filtered_df.loc[:, 'STNAM'] = filtered_df['STNAM'].str.title()

    filtered_df.rename(columns={'LEANM': 'County Name', 'STNAM': 'State'}, inplace=True)

    # Werte vereinheitlichen in der RATE-Spalte
    filtered_df.loc[:, 'RATE'] = filtered_df['RATE'].apply(calculate_mean_from_range)

    # Berechnen des Mittelwerts nur für die 'RATE'-Spalte
    grouped_df = filtered_df.groupby(['County Name', 'State']).agg({'RATE': 'mean'}).reset_index()

    grouped_df['Perzentil_HighSchool'] = grouped_df['RATE'].rank(pct=True) * 100

    median_value = grouped_df['RATE'].median()
    print("Median:", median_value)

    # Dynamischer Pfad für die CSV-Datei
    output_path = os.path.join(base_dir, f'code generated interim files/Graduation Rate/HighSchoolData_{year}.csv')

    grouped_df.to_csv(output_path, index=False)

    
    print(grouped_df)

    return grouped_df

getHighschoolGraduationRate(year)

def prepareAgeDiversity(year): 
    
    year_str = str(year)
    
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    dataset_path = os.path.join(base_dir, f'{year_str}/Opportunity/Age_{year_str}.csv')

    # Relevante Spalten laden
    columns_to_load = ['GEO_ID', 'NAME', 'S0101_C02_002E', 'S0101_C02_003E', 'S0101_C02_004E', 'S0101_C02_005E', 'S0101_C02_006E', 'S0101_C02_007E', 'S0101_C02_008E', 'S0101_C02_009E', 'S0101_C02_010E', 'S0101_C02_011E', 'S0101_C02_012E', 'S0101_C02_013E', 'S0101_C02_014E', 'S0101_C02_015E', 'S0101_C02_016E', 'S0101_C02_017E', 'S0101_C02_018E', 'S0101_C02_019E']

    # Skip Metadata
    df = pd.read_csv(dataset_path, dtype=str, usecols=columns_to_load, skiprows=[1])
    df['FIPS'] = df['GEO_ID'].str[-5:]

    # Bereinigen by stripping leading and trailing whitespaces
    df.columns = df.columns.str.strip()

    # Anzeigen der unique column names um sicherzugehen dass richtig
    print("Unique Column Names:", df.columns)

     # Spezifizieren der Gruppen
    columns_group1 = ['S0101_C02_002E', 'S0101_C02_003E', 'S0101_C02_004E']
    columns_group2 = ['S0101_C02_005E', 'S0101_C02_006E', 'S0101_C02_007E', 'S0101_C02_008E', 'S0101_C02_009E', 'S0101_C02_010E','S0101_C02_011E', 'S0101_C02_012E']
    columns_group3 = ['S0101_C02_013E', 'S0101_C02_014E', 'S0101_C02_015E', 'S0101_C02_016E', 'S0101_C02_017E', 'S0101_C02_018E', 'S0101_C02_019E']

    # Neue Gruppen mit der Summe der Gruppe für jede Spalte
    df['Summe_Group1'] = df[columns_group1].astype(float).sum(axis=1)
    df['Summe_Group2'] = df[columns_group2].astype(float).sum(axis=1)
    df['Summe_Group3'] = df[columns_group3].astype(float).sum(axis=1)


    
    print(df)

    return df 

# Aufruf der Funktion
prepareAgeDiversity(year)


def getNationalAge(year): 

    year_str = str(year)
    
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    dataset_path = os.path.join(base_dir, f'{year_str}/Opportunity/NationalAge_{year}.csv')

    # Lesen der CSV-Datei
    df = pd.read_csv(dataset_path)

    # Überprüfen des Spaltennamens basierend auf dem Jahr und Auswählen der richtigen Spalte
    if year >= 2017:
        estimate_column = 'United States!!Percent!!Estimate'
    else:
        estimate_column = 'United States!!Total!!Estimate'

    # Konvertierung der 'Estimate'-Spalte in ein numerisches Format, entfernen von Nicht-Zahlen Zeichen
    df[estimate_column] = df[estimate_column].replace('[\%,]', '', regex=True)
    df[estimate_column] = pd.to_numeric(df[estimate_column], errors='coerce')  # Verwenden von 'coerce', um Konvertierungsfehler zu behandeln

    # Definieren der Altersgruppen gemäß den Anforderungen
    age_groups = {
        'children': ['Under 5 years', '5 to 9 years', '10 to 14 years'],
        'working_age': [
            '15 to 19 years', '20 to 24 years', '25 to 29 years', '30 to 34 years',
            '35 to 39 years', '40 to 44 years', '45 to 49 years', '50 to 54 years'],
        'experienced_retired': [
            '55 to 59 years', '60 to 64 years', '65 to 69 years', '70 to 74 years',
            '75 to 79 years', '80 to 84 years', '85 years and over']
    }

    # Summieren der Prozente für jede Altersgruppe
    sums = {group_name: 0 for group_name in age_groups}  # Initialisieren der Summen mit 0
    for group_name, age_labels in age_groups.items():
        # Filtern der Daten für die aktuelle Altersgruppe
        for label in age_labels:
            # Filtern basierend auf dem 'Label (Grouping)'
            group_data = df[df['Label (Grouping)'].str.strip() == label.strip()]
            # Überprüfen und Summieren der Prozente für die aktuelle Altersgruppe
            if not group_data.empty:
                sums[group_name] += group_data[estimate_column].sum()

    return sums

    # Beispielaufruf 
sums = getNationalAge(year)



def calculate_age_diversity_pearson(df_local, national_percents):
    # Konvertieren der nationalen Prozentsätze in eine Liste im selben Format wie die lokalen Prozentsätze
    national_percents_list = [national_percents['children'], national_percents['working_age'], national_percents['experienced_retired']]
    
    # Berechnen des Pearson-Korrelationskoeffizienten für jede Gemeinde
    df_local['Pearson_Correlation_Coeff'] = df_local.apply(lambda row: pearsonr(
        [row['Summe_Group1'], row['Summe_Group2'], row['Summe_Group3']], national_percents_list)[0], axis=1)

    print (df_local)

    return df_local


def getAgeDiversity(year):
    # Aufrufen der nationalen Prozentsätze 
    national_percents = getNationalAge(year)
    
    # Annahme: getAgeDiversity gibt ein DataFrame zurück, das die lokalen Prozentsätze enthält
    local_percents_df = prepareAgeDiversity(year)
    
    # Berechnen des Age Diversity Scores für jede Gemeinde
    local_percents_df = calculate_age_diversity_pearson(local_percents_df, national_percents)

    local_percents_df['Perzentil_AgeDiversity'] = local_percents_df.groupby(['FIPS'])['Pearson_Correlation_Coeff'].transform(lambda x: np.percentile(x, 50))

    local_percents_df['Perzentil_AgeDiversity'] = local_percents_df['Pearson_Correlation_Coeff'].rank(pct=True) * 100


    median_value = local_percents_df['Pearson_Correlation_Coeff'].median()
    print("Median:", median_value)

    # Beispielaufruf
    print(local_percents_df[['FIPS', 'NAME', 'Pearson_Correlation_Coeff', 'Perzentil_AgeDiversity']])
    
    # Speichern oder weiterverarbeiten der Ergebnisse
    return local_percents_df

# Beispielaufruf
age_diversity_scores = getAgeDiversity(year)

# Maximum und Minimum der Pearson-Korrelationskoeffizienten
max_corr = age_diversity_scores['Pearson_Correlation_Coeff'].max()
min_corr = age_diversity_scores['Pearson_Correlation_Coeff'].min()

print("Maximum Pearson-Korrelationskoeffizient:", max_corr)
print("Minimum Pearson-Korrelationskoeffizient:", min_corr)


# def calculate_similarity(local_percents, national_percents):
   
    # Berechne die euklidische Distanz zwischen den lokalen und nationalen Prozenten
    #distance = np.sqrt(np.sum((np.array(local_percents) - np.array(national_percents))**2))
    # Konvertiere die Distanz in einen Ähnlichkeitswert (dieser Teil kann angepasst werden)
    # Nehmen wir an, eine maximale Distanz von 100% als den ungünstigsten Fall
    #similarity = 1 - (distance / np.sqrt(3*100**2))
    # Stelle sicher, dass der Wert zwischen 0 und 1 liegt
   # return max(0, min(1, similarity))*100



#def calculate_similarity(local_percents, national_percents)

    # Berechne die Kosinus-Ähnlichkeit zwischen den lokalen und nationalen Prozenten
    #similarity = 1 - cosine(local_percents, national_percents)
    
    # Stelle sicher, dass der Ähnlichkeitswert zwischen 0 und 1 liegt
    #similarity = max(0, min(1, similarity))
    
    # Konvertiere den Ähnlichkeitswert in Prozent
    #similarity_percent = similarity * 100
    
    #return similarity_percent

#def getAgeDiversity(year):
    # Rufen Sie die nationalen Prozentsätze ab
    #national_percents = getNationalAge(year)
    
    # Annahme: getAgeDiversity gibt ein DataFrame zurück, das die lokalen Prozentsätze enthält
    #local_percents_df = prepareAgeDiversity(year)
    
    # Konvertieren der nationalen Prozentsätze in eine Liste im selben Format wie die lokalen Prozentsätze
    #national_percents_list = [national_percents['children'], national_percents['working_age'], national_percents['experienced_retired']]
    
    # Berechnen Sie die Age Diversity Scores für jede Gemeinde
    #local_percents_df['Age_Diversity_Score'] = local_percents_df.apply(
        #lambda row: calculate_similarity([row['Summe_Group1'], row['Summe_Group2'], row['Summe_Group3']], national_percents_list),
        #axis=1
    #)

    # Berechnen Sie den Rangprozentsatz für die Age Diversity Scores
    # local_percents_df['AgeDiversity_Rank_Percentage'] = rank_percentage(local_percents_df['Age_Diversity_Score'])

    #local_percents_df['Perzentil_AgeDiversity'] = local_percents_df.groupby(['FIPS'])['Age_Diversity_Score'].transform(lambda x: np.percentile(x, 50))

    #local_percents_df['Perzentil_AgeDiversity'] = local_percents_df['Age_Diversity_Score'].rank(pct=True) * 100


    #median_value = local_percents_df['Age_Diversity_Score'].median()
    #print("Median:", median_value)
    
    # Speichern oder weiterverarbeiten der Ergebnisse
    #return local_percents_df

# Beispielaufruf
#age_diversity_scores = getAgeDiversity(year)
#print(age_diversity_scores[['FIPS', 'NAME', 'Perzentil_AgeDiversity']])




def getJobsperWorker(year):
    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

    # Dynamischer Pfad zur CSV-Datei
    filepath = os.path.join(base_dir, 'cross-year files', 'JobsperWorker.csv')

    # Einlesen der CSV-Datei
    df = pd.read_csv(filepath)

    # Entfernen von Zeilen, wo "geo_level" ein "S" enthält
    df = df[~df['geo_level'].str.contains('S')]
    
    # Filtern des DataFrames nach dem angegebenen Jahr
    df_filtered = df[df['year'] == year]
    
    # Berechnung des Durchschnitts von "Emp" und "EmpEnd"
    df_filtered['JobsPerWorker'] = (df_filtered['Emp'] + df_filtered['EmpEnd']) / 2 / df_filtered['EmpTotal']
    
    # Gruppierung nach 'geography' und Berechnung des Durchschnitts für jedes County
    result = df_filtered.groupby('geography')['JobsPerWorker'].mean().reset_index()

    # Anwenden der rank_percentage Funktion auf die 'JobsPerWorker' Spalte
    # result['JobsPerWorker_RankPercentage'] = rank_percentage(result['JobsPerWorker'])

    # Umbenennen der "geography" Spalte in "FIPS"
    result.rename(columns={'geography': 'FIPS'}, inplace=True)

    result['Perzentil_JobsperWorker'] = result.groupby(['FIPS'])['JobsPerWorker'].transform(lambda x: np.percentile(x, 50))

    result['Perzentil_JobsperWorker'] = result['JobsPerWorker'].rank(pct=True) * 100


    median_value = result['JobsPerWorker'].median()
    print("Median:", median_value)

    print (result)
    # Ausgabe der Ergebnisse
    return result

# Beispiel, wie die Funktion aufgerufen wird:
getJobsperWorker(year)







def merge_data_frame_by_location(df1, df2, criteria=['County Name', 'State']):

     # Erstellen einer Kopie von excel_df, um das Original unverändert zu lassen
    new_df = df1.copy()
    if criteria=='FIPS':
        df2['FIPS']= df2['FIPS'].astype(int)

    # Zuerst df_merged mit der Kopie von excel_df mergen, basierend auf gemeinsamen Spalten
    updated_df = pd.merge(new_df, df2, on=criteria, how='left')

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
#df_final = merge_data_frame_by_location(df_final, getIncomeInequality(year),'FIPS')
#df_final = merge_data_frame_by_location(df_final, getHighschoolGraduationRate(year))
#df_final = merge_data_frame_by_location(df_final, getAgeDiversity(year), 'FIPS')
#df_final = missing_values_average(df_final)
#print (df_final)
#df_final.to_csv(f'FinalOpportunityData{year}.csv', index=False)
