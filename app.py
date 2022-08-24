import os
from flask import Flask, session, render_template, redirect, request, jsonify, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Search, db, connect_db
from forms import UserForm, NoteForm, LoginForm
# from secrets import merriam_webster, sketch
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',"carmelvalley")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', "postgres:///prag_dict")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

def check_login():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        g.user = user

@app.route('/')
def home_page():
    check_login()
    return render_template('home.html', form=NoteForm())


# Make a call to the Merriam Webster Dictionary API and get short definitions
@app.route('/api/dictionary/<word>', methods=['GET','POST'])
def return_dict(word):
    url = f'https://dictionaryapi.com/api/v3/references/learners/json/{word}'

    resp = requests.get(url, params={
        'key': os.environ.get('mw_apikey', 'secret_api')
    })
    data = resp.json()
    definition = data[0]['meta']['app-shortdef']['def']
    return jsonify(definition)

# Make a call to the Sketch Engine API and get the corpus data
@app.route('/api/sketchengine/<word>/<pos>', methods=['GET','POST'])
def return_gramrels(word, pos):
    USERNAME = 'thor.sawin'
    API_KEY = os.environ.get('sketch_apikey', 'secret_api')
    url = 'https://api.sketchengine.eu/bonito/run.cgi/wsketch'
    data = requests.get(url, auth=(USERNAME, API_KEY), params={
         'corpname': 'preloaded/bnc2',
         'format': 'json',
         'lemma': word,
         'lpos': pos
    }).json()
    session['word'] = word
    session['pos'] = pos
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
        session['user_id'] = new_user.id
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
        user = User.authenticate(username=username, pwd=password)
        if user:
            session['user_id'] = user.id
            g.user = user
            return redirect('/')
        else:
            flash('Incorrect credentials')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)

# show user their notes page
@app.route('/<int:user_id>/notes', methods=['GET'])
def show_notes(user_id):
    g.user = User.query.get_or_404(user_id)
    form = NoteForm()
    if user_id != session['user_id']:
        flash('Access denied')
        return redirect('/')
    else:
        notes = g.user.searches
        return render_template('notes.html', notes=notes)
    
@app.route('/<int:user_id>/notes', methods=['POST'])
def save_notes(user_id):
    g.user = User.query.get_or_404(user_id)
    word, pos, user_id, note = [request.json[k] for k in ('word', 'pos', 'user_id', 'note')]
    if len(Search.query.filter(Search.word==word, Search.user_id == user_id).all()) == 0:
        search = Search(word=word, pos=pos, note=note, user_id=user_id)
        db.session.add(search)
        db.session.commit()
        return 'Note created'
    else:
        search = Search.query.filter(Search.word==word, Search.user_id == user_id).one()
        search.note = note
        db.session.commit()
        return 'Note saved'

    

@app.route('/<int:user_id>/notes/<int:search_id>')
def show_note(user_id, search_id):
    g.user = User.query.get_or_404(user_id)
    note = Search.query.get_or_404(search_id)
    word = note.word
    pos = note.pos.value
    if user_id != session['user_id']:
        flash('Access denied')
        return redirect('/')
    return render_template('home.html', word_to_search=word, pos=pos, form=NoteForm(obj=note))

@app.route('/<int:user_id>/notes/<int:search_id>/delete')
def delete_note(user_id, search_id):
    g.user = User.query.get_or_404(user_id)
    note = Search.query.get_or_404(search_id)
    if note.user_id == g.user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted', 'success')
        return redirect(f'/{user_id}/notes')
    else:
        flash('Permission denied', 'danger')
        return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    del session['user_id']
    return redirect('/')