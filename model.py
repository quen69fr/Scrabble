# coding: utf-8

from outils import *


class Partie:
    def __init__(self):
        self.etat = ETAT_PARTIE_LOGIN
        self.sousEtatJeu = SOUS_ETAT_JEU_PIOCHER
        self.monPseudo = ''
        self.monJoueur = None
        self.pseudoJoueurPrecedent = None
        self.listeOrdrePseudos = []
        self.dicJoueurs = {}
        self.joueurTour = None
        self.joueurTourPiocher = None
        self.dicJoueurSuivant = {}
        self.plateau = Plateau()
        self.nbTours = 1

    def login(self, monPseudo):
        self.monPseudo = monPseudo
        self.monJoueur = Joueur(monPseudo)
        self.dicJoueurs[monPseudo] = self.monJoueur
        self.etat = ETAT_PARTIE_MISE_EN_PLACE

    def ajoute_joueur(self, pseudo):
        if self.etat == ETAT_PARTIE_MISE_EN_PLACE and pseudo not in self.dicJoueurs.keys():
            self.dicJoueurs[pseudo] = Joueur(pseudo)

    def demarrer(self, listeOrdrePseudos):
        self.listeOrdrePseudos = listeOrdrePseudos
        if self.etat == ETAT_PARTIE_MISE_EN_PLACE and len(listeOrdrePseudos) > 1:
            self.etat = ETAT_PARTIE_JEU
            ancienPseudo = None
            for i, pseudo in enumerate(listeOrdrePseudos):
                if i == 0:
                    self.joueurTour = self.dicJoueurs[pseudo]
                    self.joueurTourPiocher = self.dicJoueurs[pseudo]
                else:
                    self.dicJoueurSuivant[self.dicJoueurs[ancienPseudo]] = self.dicJoueurs[pseudo]
                if pseudo == self.monPseudo:
                    self.pseudoJoueurPrecedent = ancienPseudo
                ancienPseudo = pseudo
            self.dicJoueurSuivant[self.dicJoueurs[ancienPseudo]] = self.joueurTour
            if self.pseudoJoueurPrecedent is None:
                self.pseudoJoueurPrecedent = listeOrdrePseudos[-1]

    def joueur_suivant(self):
        self.joueurTour = self.dicJoueurSuivant[self.joueurTour]
        self.nbTours += 1

    def joueur_piocher_suivant(self):
        self.joueurTourPiocher = self.dicJoueurSuivant[self.joueurTourPiocher]

    def etat_suivant(self, action: str):
        if self.sousEtatJeu in AUTOMATE_PARTIE:
            dicSousEtatSuivant = AUTOMATE_PARTIE[self.sousEtatJeu]
            if action in dicSousEtatSuivant:
                self.sousEtatJeu = dicSousEtatSuivant[action]
                return True
        return False


class Lettre:
    def __init__(self, lettre: str, validee=False):
        self.lettre = lettre.upper()[0]
        self.validee = validee
        self.points = POINTS_PAR_LETTRE[self.lettre]

    def __str__(self):
        return f'Lettre : {self.lettre}'


class Plateau:
    def __init__(self):
        self.cases = [[None for col in range(TAILLE_PLATEAU)] for lig in range(TAILLE_PLATEAU)]

    def placer_lettre(self, lettre: Lettre, lig: int, col: int):
        if 0 <= lig < TAILLE_PLATEAU and 0 <= col < TAILLE_PLATEAU and self.cases[lig][col] is None:
            self.cases[lig][col] = lettre
            return True
        return False

    def enlever_lettre(self, lettre: Lettre):
        for nl, lig in enumerate(self.cases):
            for nc, case in enumerate(lig):
                if case == lettre:
                    self.cases[nl][nc] = None
                    return True
        return False

    def vider_case(self, lig: int, col: int):
        if 0 <= lig < TAILLE_PLATEAU and 0 <= col < TAILLE_PLATEAU:
            self.cases[lig][col] = None
            return True
        return False

    def get_index_lettre(self, lettre: Lettre):
        for nl, lig in enumerate(self.cases):
            for nc, case in enumerate(lig):
                if case == lettre:
                    return nl, nc
        print('non')
        return None

    def get_lettres_placees(self):
        listeLettres = []
        for nl, ligne in enumerate(self.cases):
            for nc, case in enumerate(ligne):
                if case is not None and not case.validee:
                    listeLettres.append([case, nl, nc])
        return listeLettres

    def valider(self):
        listeLettres = self.get_lettres_placees()
        for l, _, _ in listeLettres:
            l.validee = True

    def get_mot_ligne(self, lettre: Lettre, i_lettre=None, j_lettre=None):
        if i_lettre is None or j_lettre is None:
            i_lettre, j_lettre = self.get_index_lettre(lettre)
        j_gauche = j_lettre
        j_droite = j_lettre
        gauche = not j_gauche == 0
        droite = not j_droite == len(self.cases) - 1
        mot = [lettre]
        while gauche or droite:
            if gauche:
                j_gauche -= 1
                case = self.cases[i_lettre][j_gauche]
                if case is None:
                    gauche = False
                else:
                    if j_gauche == 0:
                        gauche = False
                    mot.insert(0, case)
            if droite:
                j_droite += 1
                case = self.cases[i_lettre][j_droite]
                if case is None:
                    droite = False
                else:
                    if j_droite == len(self.cases) - 1:
                        droite = False
                    mot.append(case)
        return mot

    def get_mot_colonne(self, lettre: Lettre, i_lettre=None, j_lettre=None):
        if i_lettre is None or j_lettre is None:
            i_lettre, j_lettre = self.get_index_lettre(lettre)
        i_haut = i_lettre
        i_bas = i_lettre
        haut = not i_haut == 0
        bas = not i_bas == len(self.cases[0]) - 1
        mot = [lettre]
        while haut or bas:
            if haut:
                i_haut -= 1
                case = self.cases[i_haut][j_lettre]
                if case is None:
                    haut = False
                else:
                    if i_haut == 0:
                        haut = False
                    mot.insert(0, case)
            if bas:
                i_bas += 1
                case = self.cases[i_bas][j_lettre]
                if case is None:
                    bas = False
                else:
                    if i_bas == len(self.cases[0]) - 1:
                        bas = False
                    mot.append(case)
        return mot

    def convert_mot_to_string(self, mot: list):
        string = ''
        for lettre in mot:
            string += lettre.lettre
        return string

    def __str__(self):
        str = f'Plateau :'
        for ligne in self.cases:
            str += f'\n{ligne}'
        return str


class Chevalet:
    def __init__(self):
        self.cases = [None for i in range(NB_CASES_CHEVALET)]

    def placer_lettre(self, lettre: Lettre, i: int = None):
        if i is not None:
            if 0 <= i < NB_CASES_CHEVALET and self.cases[i] is None:
                self.cases[i] = lettre
                return True
        else:
            for i, case in enumerate(self.cases):
                if case is None:
                    self.cases[i] = lettre
                    return True
        return False

    def enlever_lettre(self, lettre: Lettre):
        for i, case in enumerate(self.cases):
            if case == lettre:
                self.cases[i] = None
                return True
        return False

    def vider_case(self, i: int):
        if 0 <= i < NB_CASES_CHEVALET:
            self.cases[i] = None

    def deplacer_lettre(self, lettre: Lettre = None, indexLettre: int = None, new_i: int = None):
        if lettre is not None:
            if lettre in self.cases and (new_i is None or 0 <= new_i < NB_CASES_CHEVALET):
                if self.enlever_lettre(lettre):
                    if self.placer_lettre(lettre, new_i):
                        return True
                    return 'Erreur !'
        if indexLettre is not None:
            if self.placer_lettre(lettre, new_i):
                self.vider_case(indexLettre)
                return True
        return False

    def get_lettres_placees(self):
        listeLettres = []
        for i, case in enumerate(self.cases):
            if case is not None:
                listeLettres.append([case, i])
        return listeLettres

    def nb_point_total(self):
        nb_points = 0
        for case in self.cases:
            if case is not None:
                nb_points += case.points
        return nb_points

    def nb_lettres(self):
        n = 0
        for case in self.cases:
            if case is not None:
                n += 1
        return n

    def __str__(self):
        return f'Chevalet : {self.cases}'


class Joueur:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.score = 0
        self.dernierScore = 0
        self.chevalet = Chevalet()

    def ajouter_points(self, points: int, ajoute_au_dernierScore=False):
        self.score += points
        if ajoute_au_dernierScore:
            self.dernierScore += points
        else:
            self.dernierScore = points
