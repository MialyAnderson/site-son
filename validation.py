import re

class Validation:

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
