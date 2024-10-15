def state_code_to_name(state_code):
    state_codes = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }

    # Convert the input to uppercase to handle case-insensitive matching
    state_code = state_code.upper()

    # Check if the state code is in the dictionary
    if state_code in state_codes:
        return state_codes[state_code]
    else:
        return "State code not found"

import pandas as pd
import os

# def read_code_mappings(file_path, key_column, value_column):
    #df = pd.read_excel(file_path, header=1)
    #print("DataFrame from Excel:")
    #print(df)

    #code_mappings = dict(zip(df[key_column], df[value_column]))
    #print(f"Code Mappings: {code_mappings}")

    #return code_mappings

##def get_state_name(state_code):
    #state_codes = read_code_mappings('US_FIPS_Codes.xls', 'FIPS State', 'State')
    #return state_codes.get(int(state_code), 'Unknown')

#def get_county_name(county_code):
    ##county_codes = read_code_mappings('US_FIPS_Codes.xls', 'FIPS County', 'County Name')
    #return county_codes.get(int(county_code), 'Unknown')


#state_code = '01'
#county_code = '001'
#print(f'State Code: {state_code}, County Code: {county_code}')

#state_name = get_state_name(state_code)
#county_name = get_county_name(county_code)

#print(f'State: {state_name}, County: {county_name}')

base_dir = os.path.dirname(os.path.realpath(__file__))  # Verzeichnis des Skripts
excel_path = os.path.join(base_dir, "Allgemein", "US_FIPS_Codes.xls")

# Lese die Excel-Datei
df = pd.read_excel(excel_path, header=1)



# Füge eine neue Spalte 'FIPS Sum' hinzu, die die Summe von 'FIPS State' und 'FIPS County' ist
df['FIPS Sum'] = (df['FIPS State'].astype(str).str.zfill(2) + df['FIPS County'].astype(str).str.zfill(3)).astype(int)

# Funktion, um den County- und Staatsnamen basierend auf 'FIPS Sum' zu erhalten
def get_county_state(fips_sum):
    row = df[df['FIPS Sum'] == fips_sum]
    if not row.empty:
        return row['County Name'].values[0], row['State'].values[0]
    else:
        return None, None


def get_state_code(fips_sum):
    row = df[df['FIPS Sum'] == fips_sum]
    if not row.empty:
        return row['FIPS State'].values[0]
    else:
        return None
    
# Beispielaufruf
fips_sum = 1001  # Hier die gewünschte Summe von 'FIPS State' und 'FIPS County' eintragen
county, state = get_county_state(fips_sum)

if county and state:
    print(f"State: {state}, County: {county}")
else:
    print("FIPS Sum nicht gefunden.")


state_code_example = get_state_code(fips_sum)

if state_code_example:
    print(f"State Code: {state_code_example}")
else:
    print("FIPS Sum nicht gefunden.")