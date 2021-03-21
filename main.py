import requests
import os
from sejm import MP
from declaration import Declaration
import json

mps = requests.get('http://api.sejm.gov.pl/sejm/term9/MP').json()

api = []


def get_city(location):
    key = 'AIzaSyBEu_cX_5ViUUlYQP6oAVKQB59--9OjuN0'

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={key}'
    r = requests.get(url).json()

    if r['status'] == 'ZERO_RESULTS' or r['status'] == 'INVALID_REQUEST':
        pob = location
    else:
        pob = r['results'][0]['address_components'][0]['long_name']

    return pob


for ind, mp in enumerate(mps):
    id = mp['id']
    first_name = mp['firstName']
    last_name = mp['lastName']
    club = mp['club']

    representative = MP(id=id,
                        first_name=first_name,
                        last_name=last_name,
                        club=club)

    print(id)
    pdf_file = f'declarations/{id:03d}.pdf'

    if pdf_file.split('/')[1] in os.listdir('declarations'):
        try:
            #declaration_date = representative.get_declaration()
            declaration = Declaration(pdf_file=pdf_file)
            #declaration.get_name()
            dob = declaration.get_dob()
            pob = get_city(declaration.get_pob())
            position = declaration.get_position()
            pln_money = declaration.get_pln_money()
            foreign_money = declaration.get_foreign_money()

            api.append({'id': id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'dob': dob,
                        'pob': pob,
                        'club': club,
                        'position': position,
                        'pln_money': pln_money,
                        'foreign_money': foreign_money,
                        'declaration_date': 'null'})
        except:
            print('problem')
            continue

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(api, f, ensure_ascii=False, indent=4)












