import health
import housing
import opportunity
import transportation
import environment
import engagement
import neighborhood
import pandas as pd 
from os import path 
import os

year = 2019 


def merge_data_frame_by_location(df1, df2, criteria=['County Name', 'State']):

     # Erstellen einer Kopie von excel_df, um das Original unverändert zu lassen
    new_df = df1.copy()
    if criteria=='FIPS':
        df2['FIPS']= df2['FIPS'].astype(int)

    # Zuerst df_merged mit der Kopie von excel_df mergen, basierend auf gemeinsamen Spalten
    updated_df = pd.merge(new_df, df2, on=criteria, how='left', suffixes=('', '_duplicate'))

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

def missing_values_state_average(df):

    # Berechne den nationalen Durchschnitt für jede numerische Spalte
    national_means = df.select_dtypes(include=[int, float]).mean()
    # Ersetze fehlende numerische Werte mit dem Mittelwert pro Staat
    for column_name in df.select_dtypes(include=[int, float]):
        # Berechne den Mittelwert pro Staat für die Spalte
        state_means = df.groupby('State')[column_name].transform('mean')
        # Fülle fehlende Werte in der Spalte mit dem berechneten Mittelwert pro Staat
        df[column_name] = df[column_name].fillna(state_means)

        # Fülle verbleibende fehlende Werte mit dem nationalen Durchschnitt
        df[column_name] = df[column_name].fillna(national_means[column_name])
        
    return df

# Laden der Excel-Datei in einen DataFrame
# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

# Dynamischer Pfad zur Excel-Datei
file_path = os.path.join(base_dir, 'cross-year files', 'US_FIPS_Codes.xls')
df_base = pd.read_excel(file_path, header=1)
df_final = df_base.copy()
df_final = merge_data_frame_by_location(df_final, health.getAccesstoExerciseOpportunities(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, health.getPatientSatisfaction(year))
df_final = merge_data_frame_by_location(df_final, health.getPreventableHospitalizationRate(year))
df_final = merge_data_frame_by_location(df_final, health.getSmokingPrevalence(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, health.getObesityPrevalence(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, health.getHealthcareShortage(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, housing.getMultiFamilyHousing(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, housing.getHousingCosts(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, housing.getHousingCostBurden(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, housing.getSubsidizedHousingData(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, opportunity.getIncomeInequality(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, opportunity.getHighschoolGraduationRate(year))
df_final = merge_data_frame_by_location(df_final, opportunity.getAgeDiversity(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, opportunity.getJobsperWorker(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, transportation.getCrashRate(year))
df_final = merge_data_frame_by_location(df_final, transportation.getSpeedLimits(year), 'State')
df_final = merge_data_frame_by_location(df_final, transportation.getADAStationsAndVehicles(year), 'State')
df_final = merge_data_frame_by_location(df_final, transportation.getHouseholdTransportationCosts(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, environment.getAirPollutionDays(year))
df_final = merge_data_frame_by_location(df_final, environment.getDrinkingWater(year), 'State')
df_final = merge_data_frame_by_location(df_final, environment.getLocalIndustrialPollution(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, engagement.getSocialAssociations(year))
df_final = merge_data_frame_by_location(df_final, engagement.getCulturalInstitutions(year), 'State')
df_final = merge_data_frame_by_location(df_final, engagement.getBroadbandCostandSpeed(year))
df_final = merge_data_frame_by_location(df_final, engagement.getVotingRate(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, engagement.getSocialInvolvementIndex(year), 'FIPS')
df_final = merge_data_frame_by_location(df_final, neighborhood.getCrimeRate(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, neighborhood.getVacancyRate(year),'FIPS')
df_final = merge_data_frame_by_location(df_final, neighborhood.getParkScoreWithState(year), 'State')
df_final = merge_data_frame_by_location(df_final, neighborhood.getAccesstoLibraries(year))
df_final = merge_data_frame_by_location(df_final, neighborhood.getGroceryStores(year))
df_final = merge_data_frame_by_location(df_final, neighborhood.getFarmersMarkets(year), 'FIPS')
df_final = missing_values_state_average(df_final)
print (df_final)
output_path = os.path.join(base_dir, 'Livability Files with all Metrics', f'FinalOverallData_StateMean{year}.csv')
# Speichere das Ergebnis in einer CSV-Datei
df_final.to_csv(output_path, index=False)

