from flask import Flask, session, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Search, db, connect_db
from forms import UserForm, SearchForm, LoginForm
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "carmelvalley"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///prag_dict"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return render_template('home.html', form=SearchForm())


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


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = UserForm()
    if form.validate_on_submit():
        username = form.data['username']
        email = form.data['email']
        password = form.data['password']
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        new_user = User.register(username=username, email=email, pwd=password, first_name=first_name, last_name=last_name)
        session['username'] = username
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        if User.authenticate(username=username, pwd=password):
            session['username'] = username
            return redirect('/')
        else:
            flash('Incorrect credentials')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/')