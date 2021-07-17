"""Script to seed database."""

import os

import crud
import model
import server

os.system('dropdb tones')
os.system('createdb tones')

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    username = f'iamuser{n}'
    password = 'test'
    email = f'user{n}@test.com'  
    
    user = crud.create_user(username, password, email)

possible_tone_qualities = {
    'Anger': {
        'hex_base_value': '#ff0000',
    },
    'Disgust': {
        'hex_base_value': '#ff7700',
    },
    'Fear': {
         'hex_base_value': '#ff00ff',       
    },
    'Joy': {
         'hex_base_value': '#ffdd00',             
    },
    'Sadness': {
         'hex_base_value': '#0000ff',        
    },
    'Analytical': {
         'hex_base_value': '#6600cc',           
    },
    'Confident': {
         'hex_base_value': '#00ff00',          
    },
    'Tentative': {
         'hex_base_value': '#00ffff',         
    },
}

for possible_tone_quality, info in possible_tone_qualities.items():
    hex_base_value = info["hex_base_value"]

    tone_quality = crud.create_tone_quality(possible_tone_quality, hex_base_value)