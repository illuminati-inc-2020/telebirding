import json
import requests

def find_species_code(name):
    url = "https://api.ebird.org/v2/ref/taxon/find"
    params = {
        "cat": "species",
        "key": "jfekjedvescr",
        "locale": "en",
        "q": name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and len(response.json()) == 1:
        return response.json()[0]['code']
    else:
        print(f"\tError fetching species code for {name}")
        return ''

def get_latin_name(sp_code):
    url = "https://api.ebird.org/v2/ref/taxonomy/ebird"
    params = {
        "cat": "species",
        "fmt": "json",
        "species": "sibsto1",
        "locale": "en"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and len(response.json()) == 1:
        return response.json()[0]['sciName'].lower()
    else:
        print(f"\tError fetching latin name for {sp_code}")
        return ''

with open("../data/bird-species.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for key, sp in [sp for sp in data['species'].items()]:
    sp_code = ''
    latin_name = ''
    if not 'ebird_code' in sp or not sp['ebird_code']:
        print(f"Fetching {sp['name']}...")
        for name in [sp['name']] + sorted(sp['tags'], key=len, reverse=True):
            sp_code = find_species_code(name)
            if sp_code:
                if name != sp['name']:
                    print(f"\tNew name: {name}")
                    sp['tags'].remove(name)
                    data['species']['tags'] = sp['tags'] = sp['tags'] + [sp['name']]
                    data['species']['name'] = sp['name'] = name
                break
    else:
        sp_code = sp['ebird_code']
    if sp_code:
        print(f"\tSpecies code: {sp_code}")
        data['species']['ebird_code'] = sp['ebird_code'] = sp_code
        if not 'latin_name' in sp or not sp['latin_name']:
            latin_name = get_latin_name(sp_code)
    if latin_name:
        print(f"\tLatin name: {latin_name}")
        data['species']['latin_name'] = sp['latin_name'] = latin_name

with open("../data/bird-species-new.json", "w", encoding="utf-8") as file:
        json.dump(data, file, separators=(",", ":"))