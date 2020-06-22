from flask import Flask, session, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "carmelvalley"

@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/api/dictionary/<word>', methods=['GET','POST'])
def return_dict(word):
    url = f'https://dictionaryapi.com/api/v3/references/learners/json/{word}'

    resp = requests.get(url, params={
        'key': "99fab773-b4fa-4665-a0e2-7940d86e3df0"
    })
    data = resp.json()
    definition = data[0]['meta']['app-shortdef']['def']
    return jsonify(definition)


@app.route('/api/sketchengine/<word>/<pos>', methods=['GET','POST'])
def return_gramrels(word, pos):
    USERNAME = 'thor.sawin'
    API_KEY = '7ca89afd71a44589a83c3ee8da64d143'
    url = 'https://api.sketchengine.eu/bonito/run.cgi/wsketch'
    data = requests.get(url, auth=(USERNAME, API_KEY), params={
         'corpname': 'preloaded/bnc2',
         'format': 'json',
         'lemma': word,
         'lpos': pos
    }).json()
    return jsonify(data['Gramrels'])