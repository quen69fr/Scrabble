# coding: utf-8

from outilsReseau import *
import requests
import time

NB_MAX_REJEUX = 10
DELAY_SERVEUR_REQUESTS = 0.2


class ReseauClient:
    def __init__(self, adresse_ip: str, port: str, pseudo: str):
        self.pseudoJoueur = pseudo
        self.adresse_ip = adresse_ip
        self.port = port
        self.id_actuelle = -1
        self.time_last_request = 0

    def get_serveur(self, route, dicParametre=None):
        if dicParametre is None:
            dicParametre = {}
        lien = f'http://{self.adresse_ip}:{self.port}/scrabble/{route}'
        if len(dicParametre) != 0:
            lien += '?'
            for cle, valeur in dicParametre.items():
                lien += f'{cle}={valeur}&'
            lien = lien[:-1]
        i = 0
        while i < NB_MAX_REJEUX:
            try:
                r = requests.get(lien).json()
            except:
                i += 1
            else:
                return r

    def envoie_evt_au_serveur(self, typeEvt, dicParametre=None):
        if dicParametre is None:
            dicParametre = {}
        url = f'http://{self.adresse_ip}:{self.port}/scrabble/{ROUTE_ACTION_EVENT}'
        paramjson = {PARAM_PSEUDO: self.pseudoJoueur, PARAM_TYPE: typeEvt, PARAM_CONTENU: dicParametre}

        i = 0
        while i < NB_MAX_REJEUX:
            try:
                r = requests.post(url, json=paramjson)
            except:
                i += 1
            else:
                return r

    def login(self):
        self.get_serveur(ROUTE_LOGIN, {PARAM_PSEUDO: self.pseudoJoueur})

    def regardeEvenementsNonFait(self):
        if time.time() - self.time_last_request > DELAY_SERVEUR_REQUESTS:
            reponse = self.get_serveur(ROUTE_GET_EVENT, {PARAM_PSEUDO: self.pseudoJoueur, PARAM_ID: self.id_actuelle})
            self.time_last_request = time.time()
            if len(reponse) != 0:
                self.id_actuelle = reponse[-1][PARAM_ID]
                return reponse
        return []

    def placerLettre(self, lettre: str, lig: int, col: int, joker=False):
        self.envoie_evt_au_serveur(TYPE_EVT_PLACER_LETTRE, {EVT_CONTENU_LETTRE: lettre, EVT_CONTENU_LIGNE: lig,
                                                            EVT_CONTENU_COLONNE: col, EVT_CONTENU_LETTRE_JOKER: joker})

    def enleverLettre(self, lig: int, col: int):
        self.envoie_evt_au_serveur(TYPE_EVT_ENLEVER_LETTRE, {EVT_CONTENU_LIGNE: lig, EVT_CONTENU_COLONNE: col})

    def valider(self):
        self.envoie_evt_au_serveur(TYPE_EVT_VALIDER, {})

    def passer(self):
        self.envoie_evt_au_serveur(TYPE_EVT_PASSER, {})

    def piocher(self, nbLettres: int):
        reponse = self.get_serveur(ROUTE_PIOCHER_LETTRES, {PARAM_NB_LETTRES: nbLettres})
        return reponse

    def jeter(self, lettre: str):
        reponse = self.get_serveur(ROUTE_JETER_LETTRES, {PARAM_LETTRE: lettre})
        return reponse

    def demarrer(self):
        reponse = self.get_serveur(ROUTE_DEMARRER, {})
        return reponse

    def piocher_suivant(self):
        self.envoie_evt_au_serveur(TYPE_EVT_PIOCHER_SUIVANT, {})

    def fin_partie(self):
        self.envoie_evt_au_serveur(TYPE_EVT_FIN_PARTIE, {})

    def envoie_points_chevalet(self, nb_points: int):
        self.envoie_evt_au_serveur(TYPE_EVT_NB_POINTS_CHEVALET, nb_points)

    def reinit_serveur(self):
        self.get_serveur(ROUTE_REINIT)
