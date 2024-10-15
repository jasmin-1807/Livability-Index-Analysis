import geopandas as gdp
import pandas as pd
import matplotlib.pyplot as plt



# Laden der geografischen Daten aus den Shapefiles
geo_data = gdp.read_file('/Users/jasmin/Desktop/Literatur Masterarbeit/Geo Data')

# Geo-Daten laden
geo_data = gdp.read_file(geo_data)

# Umwandlung der Koordinaten in geografisches System zur Überprüfung
geo_data = geo_data.to_crs(epsg=4326)

# Filtern der Daten auf realistische USA-Koordinaten
geo_data = geo_data.cx[-125:-66, 25:50]

# Plotten ohne Umprojektion, um Projektionsfehler zu vermeiden
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
geo_data.plot(ax=ax, linewidth=0.8, edgecolor='0.8')
ax.set_title('United States Counties (Geographic Projection)')
ax.set_axis_off()
plt.show()

# Erstellen des FIPS-Codes durch Kombinieren von STATEFP und COUNTYFP und als 5-stellige Strings formatieren
geo_data['FIPS'] = geo_data['STATEFP'].astype(str).str.zfill(2) + geo_data['COUNTYFP'].astype(str).str.zfill(3)

# Ändern des FIPS-Codes von 46113 zu 46102
geo_data['FIPS'] = geo_data['FIPS'].replace('46102', '46113')


# Pfad zur CSV-Datei mit den Quality of Life Daten
csv_path = '/Users/jasmin/Desktop/Livability Score Data/Categories With Parts of H & T/FinalCategoryScores_StateMean_WithPartofHousingandTransportation2015.csv'


# Laden der Quality of Life Daten (CSV)
quality_of_life_data = pd.read_csv(csv_path)

# Formatieren des county_id als 5-stellige Strings
quality_of_life_data['FIPS'] = quality_of_life_data['FIPS'].astype(str).str.zfill(5)

# Anzeigen der ersten Zeilen der Quality of Life Daten
print(quality_of_life_data.head())

# Überprüfen der Anzahl der einzigartigen Counties in beiden Datensätzen
unique_geo_counties = geo_data['FIPS'].nunique()
unique_quality_counties = quality_of_life_data['FIPS'].nunique()

print(f"Anzahl der einzigartigen Counties im geografischen Datensatz: {unique_geo_counties}")
print(f"Anzahl der einzigartigen Counties im Quality of Life Datensatz: {unique_quality_counties}")

# Überprüfen auf übereinstimmende FIPS-Codes
common_fips = pd.merge(geo_data[['FIPS']], quality_of_life_data[['FIPS']], left_on='FIPS', right_on='FIPS', how='inner')
print(f"Anzahl der übereinstimmenden FIPS-Codes: {common_fips.shape[0]}")

# Mergen der Daten basierend auf dem FIPS-Code und Hinzufügen von Suffixen für überlappende Spalten
merged_data = geo_data.set_index('FIPS').join(quality_of_life_data.set_index('FIPS'), lsuffix='_geo', rsuffix='_ql')

# Identify counties that are present in the geographic data but missing in the quality of life data
missing_in_quality_of_life = geo_data[~geo_data['FIPS'].isin(quality_of_life_data['FIPS'])]

# Display the missing counties
print("Counties in Quality of Life data but missing in Geographic data:")
print(missing_in_quality_of_life[['FIPS']])

# Überprüfen, ob das Merging korrekt war
print("Merged DataFrame:")
print(merged_data.head())
print(merged_data['Overall Score'].describe())

# Anzahl der erfolgreich gemergten Einträge
print("Number of successfully merged entries:", merged_data['Overall Score'].notnull().sum())

# Exportieren der gemergten Daten als CSV
export_path = '/Users/jasmin/Desktop/Literatur Masterarbeit/Geo Data/merged_dataNEW.csv'
merged_data.to_csv(export_path)

# Plotten der Choroplethenkarte, nur für erfolgreich gemergte Einträge
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged_data = merged_data.to_crs(epsg=3857)  # Umprojizieren auf Web Mercator
merged_data.dropna(subset=['Overall Score']).plot(column='Overall Score', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, legend_kwds={'shrink': 0.5})
ax.set_title('Livability Score by County 2015')
ax.set_axis_off()
plt.show()