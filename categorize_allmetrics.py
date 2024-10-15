import pandas as pd 
import os


year = 2015 

# Dynamisch den Basis-Pfad basierend auf dem aktuellen Skript-Verzeichnis erstellen
base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts

file_path = os.path.join(base_dir, 'Livability Files with all Metrics', f'FinalOverallData_StateMean{year}.csv')

df_final = pd.read_csv(file_path, low_memory=False)


class Group:
    def __init__(self,destinationname, sourcenames):
        self.destinationname = destinationname
        self.sourcenames = sourcenames
groups = [Group('Health Score',['Perzentil_Satisfaction', 'Inverted_Perzentil_Smoking', 'Inverted_Perzentil_Obesity', 'Inverted_Hospitalization_Perzentil', 'Perzentil', 'Inverted_HealthcareShortage_Perzentil']), 
          Group ('Housing Score', ['Perzentil_MultiFamily', 'Inverted_Perzentil_HousingCosts', 'Inverted_Perzentil_HousingCostsBurden', 'Perzentil_SubsidizedUnits']),
          Group ('Neighborhood Score', [ 'Perzentil_Vacancy', 'Perzentil_Libraries', 'Perzentil_Park', 'Inverted_Perzentil_Crime', 'Inverted_Perzentil_Grocery', 'Perzentil_Markets']), 
          Group('Opportunity Score', ['Inverted_Perzentil_IncomeInequality', 'Perzentil_HighSchool', 'Perzentil_AgeDiversity', 'Perzentil_JobsperWorker']),
          Group('Transportation Score',['Inverted_Perzentil_CrashRate', 'Inverted_Perzentil_TransportationCosts', 'Perzentil_ADA', 'Inverted_Perzentil_SpeedLimits']), 
          Group('Environment Score', ['Inverted_Perzentil_AirPollution', 'Inverted_Perzentil_IndustrialPollution', 'Inverted_DrinkingWater']), 
          Group('Engagement Score', ['Perzentil_SocialAssociations', 'Perzentil_CulturalInstitutions', 'Perzentil_Broadband', 'Perzentil_Voting_Rate', 'Inverted_Perzentil_SocialIndex'])] 

for group in groups: 
    group.destinationname
    group.sourcenames
    n = len(group.sourcenames)
    df_final[group.destinationname] = 0 
    for column in group.sourcenames:
        df_final[group.destinationname]+= df_final [column]
    df_final[group.destinationname]/=n
    df_final[group.destinationname] = df_final[group.destinationname].round(0).astype(int)  # Runde auf ganze Zahlen


    # Berechne den "Overall Score" als Mittelwert aller Gruppen-Scores
score_columns = [group.destinationname for group in groups]
df_final['Overall Score'] = df_final[score_columns].mean(axis=1).round(0).astype(int)  # Runde auf ganze Zahlen


# Behalte nur die gewünschten Spalten
desired_columns = ['County Name', 'State', 'FIPS'] + score_columns + ['Overall Score']
df_final = df_final[desired_columns]

output_path = os.path.join(base_dir, 'Category Scores All Metrics', f'FinalCategoryScores_StateMean{year}.csv')
# Speichere das Ergebnis in einer CSV-Datei
df_final.to_csv(output_path, index=False)
