# coding: utf-8

from outils import *
from outilsReseau import *
from flask import Flask, request, jsonify
import random
# import json

app = Flask(__name__)


class Evenement:
    id_max = 1

    def __init__(self, pseudo, type_event, contenu=None):
        self.id = Evenement.id_max
        Evenement.id_max += 1
        self.pseudo = pseudo
        self.type = type_event
        self.contenu = contenu

    def dump(self):
        return {PARAM_ID: self.id, PARAM_PSEUDO: self.pseudo, PARAM_TYPE: self.type, PARAM_CONTENU: self.contenu}


liste_pseudos_joueurs = []
liste_events = []
liste_lettres_sac = []


@app.route(f'/scrabble/{ROUTE_LOGIN}')
def login():
    pseudo = request.args.get(PARAM_PSEUDO)
    if len(liste_pseudos_joueurs) > 3:
        return str(0)
    if pseudo not in liste_pseudos_joueurs:
        liste_pseudos_joueurs.append(pseudo)
    liste_events.append(Evenement(pseudo, TYPE_EVT_LOGIN))
    return str(1)


@app.route(f'/scrabble/{ROUTE_ACTION_EVENT}', methods=['POST'])
def action():
    req_data = request.get_json()
    pseudo = req_data[PARAM_PSEUDO]
    type = req_data[PARAM_TYPE]
    contenu = req_data[PARAM_CONTENU]
    event = Evenement(pseudo, type, contenu)
    liste_events.append(event)
    return '1'


@app.route(f'/scrabble/{ROUTE_GET_EVENT}')
def event():
    pseudo = request.args.get(PARAM_PSEUDO)
    id_str = request.args.get(PARAM_ID)
    l = []
    if id_str is not None:
        try:
            id = int(id_str)
        except:
            pass
        else:
            if id == -1:
                id_utilisee = 0
            else:
                id_utilisee = id
            for i in range(id_utilisee, len(liste_events)):
                event = liste_events[i]
                if event.pseudo != pseudo or id == -1:
                    l.append(event.dump())
    return jsonify(l)


@app.route(f'/scrabble/{ROUTE_PIOCHER_LETTRES}')
def piocher():
    nbLettres = int(request.args.get(PARAM_NB_LETTRES))
    if nbLettres > len(liste_lettres_sac):
        nbLettres = len(liste_lettres_sac)
    l = liste_lettres_sac[:nbLettres]
    for i in range(nbLettres):
        del liste_lettres_sac[0]
    event = Evenement(None, TYPE_EVT_LONGEUR_PIOCHE, len(liste_lettres_sac))
    liste_events.append(event)
    return jsonify(l)


@app.route(f'/scrabble/{ROUTE_JETER_LETTRES}')
def jeter():
    lettre = str(request.args.get(PARAM_LETTRE))
    liste_lettres_sac.append(lettre.upper()[0])
    random.shuffle(liste_lettres_sac)
    event = Evenement(None, TYPE_EVT_LONGEUR_PIOCHE, len(liste_lettres_sac))
    liste_events.append(event)
    return str(1)


@app.route(f'/scrabble/{ROUTE_DEMARRER}')
def demarrer():
    random.shuffle(liste_pseudos_joueurs)
    event = Evenement(None, TYPE_EVT_DEMARRER, liste_pseudos_joueurs)
    liste_events.append(event)
    return str(1)


@app.route(f'/scrabble/{ROUTE_EXIT}')
def exit():
    for pseudo in liste_pseudos_joueurs:
        liste_pseudos_joueurs.remove(pseudo)
    for event in liste_events:
        liste_events.remove(event)
    for lettre in liste_lettres_sac:
        liste_lettres_sac.remove(lettre)


if __name__ == '__main__':
    for lettre, occurence in OCCURENCES_PAR_LETTRE.items():
        for i in range(occurence):
            liste_lettres_sac.append(lettre)
    random.shuffle(liste_lettres_sac)
    app.run(host='0.0.0.0', port=12800)
