from flask import redirect, render_template, request, url_for, flash
import requests
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from .forms import LoginForm, PokemonForm, SignUpForm

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return f'Hello! {name}'

@app.route('/login', methods = ['GET','POST'])
def login():
    #loginForm = LoginForm()
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            flash(f'Welcome {queried_user.username}!', 'info')
            login_user(queried_user)
        # flash('Login Successful !', 'info')
            return redirect(url_for('home'))
        else: 
            flash('Invalid user email or password', 'warning')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    #signUpForm = signUpForm()
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data 
        new_user = User(username,email, password)
        new_user.save()
        flash('Success ! Thank you for Signing up with Theives !', 'success')
        return redirect(url_for('login')) #login here is the function name for Login, not the route '/login'
    else:
        return render_template('signup.html', form=form)



def pokemon_info(my_pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{my_pokemon}'

    response = requests.get(url)

    if response.ok:
        data = response.json()
        poke_dict = {
        'name' :  data['name'],
        'id' : data['id'], 
        'ability' : data['abilities'][0]['ability']['name'],
        'sprite': data['sprites']['front_default']
        }
    print(poke_dict)
    return poke_dict
       
print(pokemon_info(66))

@app.route('/pokemon', methods = ['GET','POST'])
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name_id = request.form.get('pokemon_name_id')
        pokemon_deets = pokemon_info(pokemon_name_id)
        return render_template('pokemon.html', pokemon_deets=pokemon_deets)
    return render_template('pokemon.html')
 



