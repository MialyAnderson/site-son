# Copyright 2024 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import g
from flask import request
from .database import Database
import random
import re

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

def generer_chiffre_aleatoire(liste_id):
    existe = False
    i = 0
    animaux = get_db().get_animaux()
    id = random.randint(1,len(animaux))
    while not existe and i < len(liste_id) :
        if liste_id[i] == id :
            existe = True
        i += 1
    if existe == True :
        id = -1
    else :
        liste_id.append(id)
    return id

@app.route('/')
def afficher_animaux_aleatoire(): 
    liste_id = []
    i = 0
    id = -1
    animaux_afficher = []
    while i < 5 :
        id = -1
        while id == -1 :
            id = generer_chiffre_aleatoire(liste_id)
        i +=1
    for element in liste_id:
        animaux_afficher.append(get_db().get_animal(element))
    return render_template('index.html', animaux=animaux_afficher)
    
@app.route('/recherche')
def rechercher():
	terme = request.args.get('search')
	resultats = []
	resultats = get_db().recherche_terme(terme)
	if len(resultats) == 0:
		return render_template('aucun_animal.html')
	return render_template('recherche.html', resultats=resultats)
	
@app.route('/animal/<int:id>')
def afficher_detail_animal(id):
	animal = get_db().get_animal(id)
	return render_template('details.html', animal=animal)
	

def valider_nom(nom):

    if nom is None or nom == "":
        return False
    elif "," in nom:
        return False
    elif len(nom) < 3 or len(nom) > 20:
        return False
    else:
        return True

def valider_espece(espece):

    if espece is None or espece == "":
        return False
    elif "," in espece:
        return False
    else:
        return True

def valider_race(race):
    if race is None or race == "":
        return False
    elif "," in race:
        return False
    else:
        return True

def valider_age(age):
    if age is None or age == "":
        return False
    elif "," in age:
        return False
    elif not age.isdigit():
        return False
    elif int(age) < 2 or int(age) > 30 :
        return False
    else :
        return True

def valider_description(description):
    if description is None or description == "":
        return False
    elif "," in description:
        return False
    else :
        return True

def valider_courriel(courriel):

    format_couriel = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if courriel is None or courriel == "":
        return False
    elif "," in courriel:
        return False
    elif not re.match(format_couriel, courriel):
        return False
    else :
        return True

def valider_adresse_civique(adresse):
    if adresse is None or adresse == "":
        return False
    elif "," in adresse:
        return False
    else :
        return True

def valider_ville(ville):
    if ville is None or ville == "":
        return False
    elif "," in ville:
        return False
    else :
        return True

def valider_code_postal(cp):

    format_cp = r'^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d$'

    if cp is None or cp == "":
        return False
    elif "," in cp:
        return False
    elif not re.match(format_cp, cp):
        return False
    else : 
        return True


@app.route('/soumettre', methods=['POST'])
def soumettre_formulaire ():
    nom = request.form['nom']
    espece = request.form['espece']
    race = request.form['race']
    age = request.form['age']
    description = request.form['description']
    courriel = request.form['courriel']
    adresse = request.form['adresse']
    ville = request.form['ville']
    cp = request.form['cp']
    nom_valide = valider_nom(nom)
    espece_valide = valider_espece(espece)
    race_valide = valider_race(race)
    age_valide = valider_age(age)
    description_valide = valider_description(description)
    courriel_valide = valider_courriel(courriel)
    adresse_valide = valider_adresse_civique(adresse)
    ville_valide = valider_ville(ville)
    cp_valide = valider_code_postal(cp)

    if  nom_valide and espece_valide and race_valide and age_valide and description_valide and courriel_valide and adresse_valide and ville_valide and cp_valide:

        get_db().add_animal(nom, espece, race, age, description, courriel, adresse, ville, cp)
        animal =  get_db().get_animal(len(get_db().get_animaux()))
        return render_template('details.html', animal=animal)
    
    return render_template('400.html'), 400
	
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
