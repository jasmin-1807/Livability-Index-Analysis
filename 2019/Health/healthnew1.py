import pandas as pd
from os import path 


def getPatientSatisfaction(year):
    csv_pfad = f'/Users/jasmin/Desktop/Livability Score Data/{year}/Health/{year}_Hospital.csv'
    
    try:
        df = pd.read_csv(csv_pfad, low_memory=False)

    # Schreibweise von 'County Name' anpassen
        df['County Name'] = df['County Name'].str.capitalize()

    # Filterung nach spezifischer Antwortbeschreibung
        filtered_df = df[df['HCAHPS Answer Description'] == 'Patients who gave a rating of "9" or "10" (high)']

    # Konvertierung der 'HCAHPS Answer Percent' Spalte zu numerischen Werten
        filtered_df.loc[:, 'HCAHPS Answer Percent'] = pd.to_numeric(filtered_df['HCAHPS Answer Percent'], errors='coerce')
    # Berechnen des Mittelwerts für 'HCAHPS Answer Percent'
        mean_percent = filtered_df['HCAHPS Answer Percent'].mean()
    # Füllen aller leeren (NaN) Zeilen in 'HCAHPS Answer Percent' mit dem Mittelwert
        filtered_df.loc[:, 'HCAHPS Answer Percent'] = filtered_df['HCAHPS Answer Percent'].fillna(mean_percent)

        columns_of_interest = ['County Name', 'State', 'HCAHPS Answer Description', 'HCAHPS Answer Percent']
        filtered_df = filtered_df[columns_of_interest]

        grouped_df = filtered_df.groupby(['County Name', 'State'])['HCAHPS Answer Percent'].mean().reset_index()

    # Anpassung des Ausgabepfades für das gefilterte CSV
        output_csv_pfad = f'/Users/jasmin/Desktop/Livability Score Data/{year}/Health/Patient_Satisfaction_Filtered.csv'
        grouped_df.to_csv(output_csv_pfad, index=False)
        print(grouped_df)
        return grouped_df
    except FileNotFoundError:
        print(f"Datei für das Jahr {year} nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

# Beispielaufruf der Funktion für das Jahr 2018
getPatientSatisfaction(2018)
   


def getSmokingPrevalence(year):
    # Dynamische Anpassung des Pfades basierend auf dem Jahr
    csv_pfad = f'/Users/jasmin/Desktop/Livability Score Data/{year}/Health/SmokingObesity{year}.csv'
    
    try:
        df = pd.read_csv(csv_pfad)
        # Da niedrige Werte gut sind, wird die Smoking Prevalence invertiert
        df['Inverse_Smoking_Prevalence'] = 100 - df['CSMOKING_CrudePrev'] 
        # Die ersten 4 Stellen der TractFIPS geben die FIPS von State + County an, eine 0 wird
        # hinzugefügt, um die Spalte mit dem "County/State" Dokument mergen zu können
        df['FIPS'] = '0' + df['TractFIPS'].astype(str).str[:4]
        df = df.filter(['TractFIPS', 'CSMOKING_CrudePrev', 'FIPS']) 
        
        return df
    except FileNotFoundError:
        print(f"Datei für das Jahr {year} nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

# Beispielaufruf für das Jahr 2018
df_result = getSmokingPrevalence(2019)
print(df_result)


# def getSmokingPrevalence():
    
    # csv_pfad = '/Users/jasmin/Desktop/Livability Score Data/2019/Health/SmokingObesity2019.csv'
    
    # df = pd.read_csv(csv_pfad)
    # Da niedrige Werte gut sind wird die Smoking Prevalence inverted
    # df['Inverse_Smoking_Prevalence'] = 100 - df['CSMOKING_CrudePrev'] 
    # Die ersten 4 Stellen der TractFIPS geben die FIPS von State + County an, eine 0 wird
    # hinzugefügt um die Spalte mit dem "County/State" Dokument mergen zu können
    # df['FIPS'] = '0' + df['TractFIPS'].astype(str).str[:4]
    # df = df.filter(['TractFIPS', 'CSMOKING_CrudePrev', 'FIPS']) 
    
    # return df

# df_result = getSmokingPrevalence()
# print(df_result)



def getObesityPrevalence(year):
    
    csv_pfad = f'/Users/jasmin/Desktop/Livability Score Data/{year}/Health/SmokingObesity{year}.csv'
    
    try:
        df = pd.read_csv(csv_pfad)
    # Da niedrige Werte gut sind wird die Smoking Prevalence inverted
        df['Inverse_Obesity_Prevalence'] = 100 - df['OBESITY_CrudePrev'] 
    # Die ersten 4 Stellen der TractFIPS geben die FIPS von State + County an, eine 0 wird
    # hinzugefügt um die Spalte mit dem "County/State" Dokument mergen zu können
        df['FIPS'] = '0' + df['TractFIPS'].astype(str).str[:4]
        df = df.filter(['TractFIPS', 'OBESITY_CrudePrev', 'FIPS']) 

        return df
    except FileNotFoundError:
        print(f"Datei für das Jahr {year} nicht gefunden.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None
    
# Beispielaufruf für das Jahr 2018
df_result = getObesityPrevalence(2019)
print(df_result)


import pandas as pd

def getPreventableHospitalizationRate(year):
    # Basispfad anpassen entsprechend Ihrer Struktur
    basis_pfad = f'/Users/jasmin/Desktop/Livability Score Data/{year}/Health/'
    
    # Dateiformat und Spaltennamen basierend auf dem Jahr bestimmen
    if year in [2015, 2016]:
        datei_pfad = f'{basis_pfad}PreventableHosp{year}.xls'
        spaltenname = 'Preventable Hosp. Rate'
    elif year in [2017, 2018, 2019]:
        datei_pfad = f'{basis_pfad}PreventableHosp{year}.xlsx'
        spaltenname = 'Preventable Hospitalization Rate'
    else:
        print("Ungültiges Jahr. Daten nur für 2015-2019 verfügbar.")
        return

    # Lese die Datei ein
    df = pd.read_excel(datei_pfad, sheet_name=3, header=1)
    df = df.filter(['State', 'County', spaltenname])

    # Normalisierung und Inversion
    max_raw_value = df[spaltenname].max()
    df['Normalized_Rate'] = ((df[spaltenname] - df[spaltenname].min()) / (max_raw_value - df[spaltenname].min())) * 100
    df['Inverted_Normalized_Rate'] = 100 - df['Normalized_Rate']

    # Ausgabe der Ergebnisse
    max_normalized_index = df['Normalized_Rate'].idxmax()
    max_inverted_normalized_index = df['Inverted_Normalized_Rate'].idxmax()

    print(f'Der höchste normalisierte Wert für {year} ist: {df["Normalized_Rate"].max():.2f}%')
    print(f'Dieser Wert wurde im Index {max_normalized_index} für das County {df.at[max_normalized_index, "County"]} gefunden.')

    print(f'Der höchste invers normalisierte Wert für {year} ist: {df["Inverted_Normalized_Rate"].max():.2f}%')
    print(f'Dieser Wert wurde im Index {max_inverted_normalized_index} für das County {df.at[max_inverted_normalized_index, "County"]} gefunden.')

    print(df)
    return df

# Beispielaufruf für das Jahr 2019
df_2019 = getPreventableHospitalizationRate(2019)




def load_data(year):
    """Lädt die Daten für ein bestimmtes Jahr, wobei das Dateiformat und unterschiedliche Spaltennamen berücksichtigt werden."""
    base_path = '/Users/jasmin/Desktop/Livability Score Data/{}/Health/AccessExercise{}'
    
    # Dateiendung basierend auf dem Jahr festlegen
    file_extension = '.xls' if year in [2016, 2018] else '.xlsx'
    
    # Vollständigen Dateipfad zusammenstellen
    xlsx_path = f"{base_path.format(year, year)}{file_extension}"
    
    try:
        df = pd.read_excel(xlsx_path, sheet_name=3, header=1)
        
        # Spaltenname basierend auf dem Jahr anpassen
        if year in [2016, 2018]:
            access_column = '% With Access'
        else:
            access_column = '% With Access to Exercise Opportunities'
        
        # Überprüfen, ob die gewünschte Spalte existiert
        if access_column not in df.columns:
            raise ValueError(f"Spalte '{access_column}' nicht gefunden in {year}.")
        
        df = df[['State', 'County', access_column]]
        df.rename(columns={access_column: '% With Access to Exercise Opportunities'}, inplace=True)
        
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
    df_earlier = df_earlier.sort_values(by=['State', 'County']).reset_index(drop=True)
    df_later = df_later.sort_values(by=['State', 'County']).reset_index(drop=True)
    
    # Berechnung des Mittelwerts für die Spalte '% With Access to Exercise Opportunities'
    interpolated_values = (df_earlier['% With Access to Exercise Opportunities'] + df_later['% With Access to Exercise Opportunities']) / 2
    df_interpolated = df_earlier.copy()
    df_interpolated['% With Access to Exercise Opportunities'] = interpolated_values
    
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

# Beispiel: Daten für das Jahr 2017 abrufen
df_2018 = getAccesstoExerciseOpportunities(2018)
print(df_2018)
