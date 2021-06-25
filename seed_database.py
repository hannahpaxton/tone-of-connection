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
        'hsl_base_value': '(0, 100%, ',
    },
    'Disgust': {
        'hsl_base_value': '(28, 100%, ',
    },
    'Fear': {
         'hsl_base_value': '(300, 100%, ',       
    },
    'Joy': {
         'hsl_base_value': '(52, 100%, ',             
    },
    'Sadness': {
         'hsl_base_value': '(240, 100%, ',        
    },
    'Analytical': {
         'hsl_base_value': '(270, 100%, ',           
    },
    'Confident': {
         'hsl_base_value': '(120, 100%, ',          
    },
    'Tentative': {
         'hsl_base_value': '(180, 100%, ',         
    },
}

for possible_tone_quality, info in possible_tone_qualities.items():
    hsl_base_value = info["hsl_base_value"]

    tone_quality = crud.create_tone_quality(possible_tone_quality, hsl_base_value)