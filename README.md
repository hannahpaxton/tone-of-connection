# 🎨 Tone of Connection 

Tone of Connection is a full-stack web application that analyzes a user’s mood and translates it to color. It acts as a journal that captures emotional snapshots by prompting users with a random self-care focused question to elicit rich responses that are analyzed for tone qualities. The results are then run through an algorithm that produces a uniquely saturated color that corresponds to the intensity of the detected tone qualities in the post. 

The color of the most resonant tone is then used to style a marker on an anonymized map where users can explore posts from others all over the U.S. Users can also look back on all of their previous posts to reflect on their emotional journey.

💻 **Deployment Link:** Coming Soon


## Contents

* [Technologies & Stack](#technologies-&-stack)
* [Set-up & Installation](#set-up-&-installation)
* [About the Developer](#about-the-developer)

## 🎨 Technologies and Stack
**Backend:** Python, Flask, SQL (PostgreSQL & SQLAlchemy)<br/>
**Frontend:** HTML(Bootstrap, Jinja), CSS, JavaScript, React<br/>
**APIs:** IBM Watson Tone Analyzer, Geocodio, Mapbox

## 🎨 Set-up & Installation

Install a code editor such as VS code or Sublime Text.
Install Python3
Install pip, the package installer for Python
Install postgreSQL for the relational database.

Clone or fork repository:
```
$ git clone https://github.com/hannahpaxton/tone-of-connection.git
```
Create and activate a virtual environment inside the tone-of-connection directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip3 install -r requirements.txt
```
Make an account with [IBM Watson](https://www.ibm.com/cloud/watson-tone-analyzer) for the Tone Analyzer & get an [API Key](https://www.ibm.com/docs/en/app-connect/cloud?topic=apps-watson-tone-analyzer).<br/>
Make an account with [Geocodio](https://www.geocod.io/) & get an [API key](https://dash.geocod.io/login).

Store these keys in a file named 'secrets.sh'
```
$ source secrets.sh
```
With PostgreSQL, create the tones database
```
$ createdb tones
```
Create all tables and relations in the database and seed all data:
```
$ python3 seed_database.py
```
Run the app from the command line:
```
$ python3 server.py
```
## 🎨 About the Developer

Tone of Connection creator Hannah Paxton is a creative strategist who has been working in the tech agency space since 2017. Currently, she works at a voice and conversational AI firm in NYC, where her passion has grown for sentiment and intent analysis, which inspired this project.  Beyond working in tech, she is the founder of Tasted Wasted, a bakery that specializes in turning cocktails into cupcakes, and has worked on two NASA space grants. This is her first full-stack project. She can be found on [LinkedIn](https://www.linkedin.com/in/hannah-paxton/) and [Github](https://github.com/hannahpaxton).
