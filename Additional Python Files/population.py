import pandas as pd

def prepare_and_save_population_data(input_excel_path, output_excel_path):
    # Einlesen der Excel-Datei, Überspringen der ersten zwei Zeilen und Benutze der dritten und vierten Zeile nicht als Kopfzeile
    df_population = pd.read_excel(input_excel_path, header=None, skiprows=2)
    
    # Manuelle Festlegung der Spaltennamen
    column_names = ['Geographic Area', 'Census', 'Estimates Base', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    df_population.columns = column_names
    print(df_population['Geographic Area'].dtype)
    # Funktion zur Extraktion von County Namen
    def extract_county(area):
        if pd.notnull(area) and isinstance(area, str):
            # Entfernen dens Punkts, falls vorhanden
            if area.startswith('.'):
                area = area[1:]
            # Teilen des Strings beim Wort "County", nur den ersten Teil behalten
            # Entfernen zusätzlicher Leerzeichen
            area = area.split(' County')[0].strip()
        return area

    
    # Funktion zur Extraktion von State Namen
    def extract_state(area):
        if pd.notnull(area) and ',' in area:
            return area.split(',')[1].strip()
        return None

    # Anwenden der Extraktionsfunktionen und Erstellung der neuen Spalten
    df_population['County'] = df_population['Geographic Area'].apply(extract_county)
    df_population['State'] = df_population['Geographic Area'].apply(extract_state)
    
    # Auswahl der notwendigen Spalten: County, State und die Bevölkerungsschätzungen für die Jahre 2015 bis 2019
    df_population_cleaned = df_population[['County', 'State', '2015', '2016', '2017', '2018', '2019']]

    df_population_cleaned[['2015', '2016', '2017', '2018', '2019']] = df_population_cleaned[['2015', '2016', '2017', '2018', '2019']].apply(pd.to_numeric, errors='coerce')
    # Speichern der bereinigten Daten in einer neuen Excel-Datei
    df_population_cleaned.to_excel(output_excel_path, index=False)
    
    print(f"Bereinigte Daten wurden gespeichert: {output_excel_path}")

# Pfad zur Eingabe-Excel-Datei und Ausgabe-Excel-Datei anpassen
input_excel_path = '/Users/jasmin/Desktop/Livability Score Data/Allgemein/CountyPopulation2010-2019.xlsx'
output_excel_path = '/Users/jasmin/Desktop/Livability Score Data/Allgemein/CleanedPop2015-2019.xlsx'

# Aufruf der Funktion mit den angegebenen Pfaden
prepare_and_save_population_data(input_excel_path, output_excel_path)



import pandas as pd
import re

def prepare_and_save_population_dataNEU(input_excel_path, output_excel_path):
    # Einleeses der Excel-Datei, überspringen der ersten zwei Zeilen und benutzen der dritten und vierten Zeile nicht als Kopfzeile
    df_population = pd.read_excel(input_excel_path, header=None, skiprows=2)
    
    # Manuelle Festlegung der Spaltennamen
    column_names = ['Geographic Area', 'Census', 'Estimates Base', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    df_population.columns = column_names
    
    # Funktion zur Extraktion von County Namen
    def extract_county(area):
        if pd.notnull(area) and isinstance(area, str):
            # Versuch, den County-Namen zu extrahieren
            try:
                # Teilen des Strings beim letzten Komma und nur den ersten Teil
                area = area.rsplit(',', 1)[0].strip()
                # Überprüfen, ob "County" im Namen enthalten ist
                if "County" in area:
                    # Extrahieren des Teils des Namens vor "County" und entfernen zusätzliche Leerzeichen
                    area = area.split(' County')[0].strip()
                # Entfernen des "." vor dem "County", falls vorhanden
                area = area.replace('.', '')
            # Ersetzen von "St" am Anfang eines Wortes durch "St."
                area = area.replace('St ', 'St. ')
                return area
            except:
                # Falls ein Fehler auftritt, gib None zurück
                return None
        else:
            return None

    # Funktion zur Extraktion von State Namen
    def extract_state(area):
        if pd.notnull(area) and ',' in area:
            return area.split(',')[1].strip()
        return None

    # Anwenden der Extraktionsfunktionen und Erstellung der neuen Spalten
    df_population['County'] = df_population['Geographic Area'].apply(extract_county)
    df_population['State'] = df_population['Geographic Area'].apply(extract_state)
    
    # Auswahl der notwendigen Spalten: County, State und die Bevölkerungsschätzungen für die Jahre 2015 bis 2019
    df_population_cleaned = df_population[['County', 'State', '2015', '2016', '2017', '2018', '2019']]

    # Konvertieren der Bevölkerungsschätzungen in numerische Werte
    df_population_cleaned[['2015', '2016', '2017', '2018', '2019']] = df_population_cleaned[['2015', '2016', '2017', '2018', '2019']].apply(pd.to_numeric, errors='coerce')
    
    # Speichern der bereinigten Daten in einer neuen Excel-Datei
    df_population_cleaned.to_excel(output_excel_path, index=False)
    
    print(f"Bereinigte Daten wurden gespeichert: {output_excel_path}")

# Pfad zur Eingabe-Excel-Datei und Ausgabe-Excel-Datei anpassen
input_excel_path = '/Users/jasmin/Desktop/Livability Score Data/Allgemein/CountyPopulation2010-2019.xlsx'
output_excel_path = '/Users/jasmin/Desktop/Livability Score Data/Allgemein/CleanedPop2015-2019NEU.xlsx'

# Aufruf der Funktion mit den angegebenen Pfaden
prepare_and_save_population_dataNEU(input_excel_path, output_excel_path)
