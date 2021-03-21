import json
from fastapi import FastAPI
from typing import Optional

with open('data.json', 'r') as f:
    data = json.load(f)

app = FastAPI()


@app.get('/mps')
def get_mps(skip: int = 0, limit: Optional[int] = len(data)):
    return data[skip : skip + limit]


@app.get('/mps/club/{club}')
def get_mps_by_club(club: str):
    return {'mp': list(filter(lambda x: x['club'].lower() == club.lower(), data))}


@app.get('/mp/id/{id}')
def get_mp_by_id(id: int):
    return {'mp': list(filter(lambda x: x['id'] == id, data))}


@app.get('/mp/name/{first_name} {last_name}')
def get_mp_by_name(first_name: str, last_name: str):
    return {'mp': list(filter(lambda x: x['first_name'].lower() == first_name.lower() and x['last_name'].lower() == last_name.lower(), data))}
