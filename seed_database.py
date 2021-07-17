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

post_prompts = [
     "What brings you joy?",
     "What does your dream life look like?",
     "What is one thing that you’d like to be different by this time next year?",
     "List five traits that you love about yourself",  
     "How are you currently sabotaging your goals?",
     "What are you grateful for today?",
     "What are your top five goals that you want to accomplish by the end of the year?",
     "What are you interested in learning more about?",
     "List five habits that you want to include in your daily routine",
What makes you happy?
What is bothering you right now?
What is my biggest regret in life?
What are some challenges that you are currently facing and how can you overcome them?
What makes you anxious or stressed?
Name three people that you are blessed to have and cannot go a day without
What are five things that you are really good at?
What do I need to do more of this year?
Are you happy with your current life? If not, what can you do to change that?
What are five things you won’t take for granted after self-isolation?
What are your five biggest fears?
What are you putting off right now?
What did you learn today?
How can you do better tomorrow?
Who or what gives you comfort?
What do you feel like your life is missing and how can you get more of what you need?
How can you love yourself more daily?
What is the best compliment you’ve ever been given? How did it make you feel?
Write a thank-you note to yourself
If failure was impossible, what would you try that you have never done before?
What is one thing that you need to start saying yes to and why?
If there was a solution to your anxiety, how would it look?
When was the last time you did something for the first time? What was it? How did it make you feel?
What would you tell your past self?
What are you in control of at this very moment?
What is the easiest part of quarantine?
What is the worst part of quarantine?
How do you refresh?
What is one goal that you can accomplish in the week ahead?
Describe your ideal day
Who is inspiring you right now? Why?
Who can you encourage today? How?
What habits would you like to change?
What scares you?
What did you learn this week?
What can you declutter physically or emotionally to find more ease and simplicity?
What does self-care look like for you?
When did you last feel truly alive?
How would you like people to describe you?
What did you do to make yourself proud this week?
]



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