import pandas as pd 
import numpy as np
import os 

year = 2019 

def rank_percentage(series):
    return series.rank(method='min').apply(lambda x: (x-1) / (len(series)-1) * 100)


def getAirPollutionDays(year): 

    year_str = str(year)

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    csv_path = os.path.join(base_dir, f'{year_str}/Environment/annual_aqi_by_county_{year_str}.csv')
    df = pd.read_csv(csv_path)

    df = df.filter(['State', 'County', 'Unhealthy for Sensitive Groups Days', 'Median AQI']) 

    # Umbenennen der Spalte "County" in "County Name"
    df.rename(columns={'County': 'County Name'}, inplace=True)

    # Berechnung des Rangprozentsatzs für die Spalte "Unhealthy for Sensitive Groups Days"
    # df['UnhealthyDays_Inverted_Rank_Percentage'] = 100 - rank_percentage(df['Unhealthy for Sensitive Groups Days'])

    # Berechnung des Perzentils für jede Zeile
    df['Perzentil_AirPollution1'] = df.groupby(['County Name','State'])['Unhealthy for Sensitive Groups Days'].transform(lambda x: np.percentile(x, 50))

    df['Perzentil_AirPollution1'] = df['Unhealthy for Sensitive Groups Days'].rank(pct=True) * 100

    df['Inverted_Perzentil_AirPollution1'] = 100 - df['Perzentil_AirPollution1']


    median_value = df['Unhealthy for Sensitive Groups Days'].median()
    print("Median:", median_value)

    # Berechnung des Rangprozentsatzes für die Spalte "Unhealthy for Sensitive Groups Days"
    # df['MedianAQI_Inverted_Rank_Percentage'] = 100 - rank_percentage(df['Median AQI'])

    # Berechnung des Perzentils für jede Zeile
    df['Perzentil_AirPollution'] = df.groupby(['County Name','State'])['Median AQI'].transform(lambda x: np.percentile(x, 50))

    df['Perzentil_AirPollution'] = df['Median AQI'].rank(pct=True) * 100

    df['Inverted_Perzentil_AirPollution'] = 100 - df['Perzentil_AirPollution']


    median_value = df['Median AQI'].median()
    print("Median:", median_value)


    print(df)

    return df

getAirPollutionDays(year)


def getDrinkingWater(year): 

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    excel_path = os.path.join(base_dir, f'{year}/Environment/DrinkingWater{year}.xlsx')
    df = pd.read_excel(excel_path, header = 4)

    # Umbenennung der Spalte 'Primacy Agency' in 'State' 
    df = df.rename(columns={'Primacy Agency': 'State'})

    # Berechnung der Anzahl der Verstöße für jeden Staat
    violations_per_state = df.groupby('State').size().reset_index(name='Violations')

    # Berechnung des Median der Verstöße
    median_value = violations_per_state['Violations'].median()
    print("Median:", median_value)

    # Berechnung des Inversen Perzentils
    violations_per_state['Perzentil_DrinkingWater'] = violations_per_state['Violations'].rank(pct=True) * 100
    violations_per_state['Inverted_DrinkingWater'] = 100 - violations_per_state['Perzentil_DrinkingWater']

    # Erstellung eines DataFrames für die Ergebnisse
    violations_ranking = violations_per_state.sort_values(by='Inverted_DrinkingWater', ascending=False)

    # Anzeigen des Rankings
    print(violations_ranking)

    return violations_ranking

getDrinkingWater(year)


def getLocalIndustrialPollution(year): 

    # Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
    excel_path = os.path.join(base_dir, 'cross-year files/RSEI-score_2015-2019.xlsx')
    df = pd.read_excel(excel_path, header = 0)


    # Überprüfen, ob die Spalte für das Einreichungsjahr vorhanden ist
    if 'Submission Year' in df.columns:
        # Filtern des DataFrames auf das gewünschte Jahr
        df_filtered = df[df['Submission Year'] == year]
        
        # Entfernen von Zeilen mit "not modeled" im RSEI Score
        df_filtered = df_filtered[df_filtered['RSEI Score'] != 'Not modeled']

        # Sicherstellen, dass die FIPS-Codes als Strings vorliegen
        df_filtered['FIPS'] = df_filtered['FIPS'].astype(str)

        # Entfernen aller fünfstelligen FIPS-Codes, die mit '7' beginnen
        df_filtered = df_filtered[~(df_filtered['FIPS'].str.startswith('7') & df_filtered['FIPS'].str.len() == 5)]
        
        # Gruppieren nach 'FIPS' und Berechnen des Mittelwerts des 'RSEI Score' für jede Gruppe
        df_grouped = df_filtered.groupby('FIPS')['RSEI Score'].mean().reset_index()
        
        # Anwenden des Rangprozentsatzes auf den gruppierten 'RSEI Score'
        # df_grouped['RSEI Score Inverted Rank Percentage'] = 100 - rank_percentage(df_grouped['RSEI Score'])

        # Berechnung des Perzentils für jede Zeile
        df_grouped['Perzentil_IndustrialPollution'] = df_grouped.groupby('FIPS')['RSEI Score'].transform(lambda x: np.percentile(x, 50))

        df_grouped['Perzentil_IndustrialPollution'] = df_grouped['RSEI Score'].rank(pct=True) * 100

        df_grouped['Inverted_Perzentil_IndustrialPollution'] = 100 - df_grouped['Perzentil_IndustrialPollution']

         # Berechnung des Median der Verstöße
        median_value = df_grouped['RSEI Score'].median()
        print("Median:", median_value)

        # Exportieren der Ergebnisse in eine CSV-Datei
        output_path = os.path.join(base_dir, 'code generated interim files', 'Local Pollution', f'Local_Pollution{year}.csv')
        df_grouped.to_csv(output_path, index=False)
        
        # Rückgabe des gruppierten DataFrames
        return df_grouped
    else:
        # Fehlermeldung, falls die Spalte 'Submission Year' nicht existiert
        return "Die Spalte 'Submission Year' wurde nicht gefunden."

# Beispielaufruf der Funktion 
result = getLocalIndustrialPollution(year)

# Ergebnis anzeigen
print(result)





