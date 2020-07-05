# coding: utf-8

from dico import *
from view import *
from model import *
from reseauMessage import *
from outils import *


class Controller:
    def __init__(self, partie: Partie, view: View):
        self.port = PORT
        self.hote = ADRESSE_IP
        self.partie = partie
        self.view = view
        self.reseauClient = None
        self.lettresJetees = []

    def etat_depart_suivant(self, contenu: str):
        if self.view.panneauDepart.etat == 1:
            self.hote = contenu
            self.view.panneauDepart.etat += 1
        else:
            self.login(contenu)

    def login(self, pseudo: str):
        self.partie.login(pseudo)
        self.reseauClient = ReseauClient(self.hote, self.port, pseudo)
        self.reseauClient.login()
        self.view.update_all()

    def demarrer(self, listeOrdrePseudos):
        self.partie.demarrer(listeOrdrePseudos)
        self.view.demarrer()
        self.update_buttons()

    def etat_partie_suivant(self, action):
        if self.partie.etat_suivant(action):
            self.update_buttons()

    def jeter_que_consonne_ou_que_voyelle(self):
        voyelles = False
        consonnes = False
        for lettre in self.lettresJetees:
            if lettre in VOYELLES:
                voyelles = True
                if consonnes:
                    return False
            elif lettre == JOKER:
                return False
            else:
                consonnes = True
                if voyelles:
                    return False
        return True

    def jete_assez_consonnes_voyelles(self):
        nbVoyelles = 0
        nbConsonnes = 0
        i = 0
        lettres = self.lettresJetees
        while nbVoyelles < 2 and nbConsonnes < 2 and i < len(lettres) - 1:
            lettre = lettres[i]
            if lettre in VOYELLES:
                nbVoyelles += 1
            elif lettre == JOKER:
                nbVoyelles += 1
                nbConsonnes += 1
            else:
                nbConsonnes += 1
            i += 1
        r = nbVoyelles < 2 or nbConsonnes < 2
        return r

    def placer_lettre_plateau(self, lettre: Lettre, lig: int, col: int):
        if self.partie.plateau.placer_lettre(lettre, lig, col):
            self.reseauClient.placerLettre(lettre.lettre, lig, col, lettre.points == 0)
            self.gere_score()
            self.etat_partie_suivant(ACTION_PARTIE_PLACER)
            self.view.update_lettre_plateau()
            return True
        return False

    def enlever_lettre_plateau(self, lettre: Lettre):
        r = self.partie.plateau.get_index_lettre(lettre)
        if r is not None:
            lig, col = r
            self.vider_case_plateau(lig, col)
            return True
        return False

    def vider_case_plateau(self, lig: int, col: int):
        if self.partie.plateau.vider_case(lig, col):
            self.reseauClient.enleverLettre(lig, col)
            self.gere_score()
            if self.partie.monJoueur == self.partie.joueurTour:
                if len(self.partie.plateau.get_lettres_placees()) == 0:
                    self.etat_partie_suivant(ACTION_PARTIE_ENLEVER_DERNIERE_LETTRE)
            self.view.update_lettre_plateau()
            return True
        return False

    def deplacer_lettre_plateau(self, lettre: Lettre, lig: int, col: int):
        if self.enlever_lettre_plateau(lettre):
            if self.placer_lettre_plateau(lettre, lig, col):
                return True
            return 'Erreur !!'
        return False

    def gere_click_plateau(self, boutonCaseClickPlateau, lig, col):
        lettreClick = boutonCaseClickPlateau.parametre
        if lettreClick is None:
            if self.view.boutonCaseSelectionne is not None:
                lettreSelectionnee = self.view.boutonCaseSelectionne.parametre
                if self.view.boutonCaseSelectionne in self.view.chevalet:
                    self.placer_lettre_plateau(lettreSelectionnee, lig, col)
                    self.partie.monJoueur.chevalet.enlever_lettre(lettreSelectionnee)
                else:
                    self.deplacer_lettre_plateau(lettreSelectionnee, lig, col)
                self.view.deselectionner_case_selectionnee()
        else:
            if not lettreClick.validee:
                self.view.selectionner_case(boutonCaseClickPlateau)

    def gere_click_chevalet(self, boutonCaseClickChevalet, i):
        lettreClick = boutonCaseClickChevalet.parametre
        if lettreClick is None:
            if self.view.boutonCaseSelectionne is not None:
                lettreSelectionnee = self.view.boutonCaseSelectionne.parametre
                if lettreSelectionnee in self.partie.monJoueur.chevalet.cases:
                    self.partie.monJoueur.chevalet.deplacer_lettre(lettreSelectionnee, new_i=i)
                else:
                    self.enlever_lettre_plateau(lettreSelectionnee)
                    self.partie.monJoueur.chevalet.placer_lettre(lettreSelectionnee, i)
                self.view.deselectionner_case_selectionnee()
        else:
            self.view.selectionner_case(boutonCaseClickChevalet)
        self.view.update_lettre_chevalet()

    def piocher_lettres(self):
        nouvellesLettres = self.reseauClient.piocher(NB_LETTRES_MAX - self.partie.monJoueur.chevalet.nb_lettres())
        for lettre in nouvellesLettres:
            self.partie.monJoueur.chevalet.placer_lettre(Lettre(lettre))
        self.view.update_lettre_chevalet()

    def gere_valider(self):
        self.partie.plateau.valider()
        self.view.update_lettre_plateau()
        if self.partie.joueurTour == self.partie.monJoueur:
            if self.view.nbTuilesRestantes == 0 and self.partie.monJoueur.chevalet.nb_lettres() == 0:
                self.reseauClient.fin_partie()
                self.prepare_fin_partie()
                return
            self.reseauClient.valider()
            if self.view.nbTuilesRestantes == 0:
                self.etat_partie_suivant(ACTION_PARTIE_VALIDER_PIOCHE_VIDE)
            else:
                self.etat_partie_suivant(ACTION_PARTIE_VALIDER)
            self.view.deselectionner_case_selectionnee()
        self.fin_tour()

    def fin_tour(self):
        self.partie.plateau.valider()
        self.view.update_lettre_plateau()
        self.partie.joueurTour.ajouter_points(self.view.nbPointsMot)
        self.view.motPossible = False
        self.view.nouveau_score_actuel(0)
        self.partie.joueur_suivant()
        self.lettresJetees = []
        self.view.update_joueurs()

    def prepare_fin_partie(self):
        self.partie.joueurTour.ajouter_points(self.view.nbPointsMot)
        self.view.motPossible = False
        self.view.nouveau_score_actuel(0)
        self.lettresJetees = []
        for joueur in self.partie.dicJoueurs.values():
            joueur.dernierScore = 0
        if not self.partie.monJoueur == self.partie.joueurTour:
            self.gere_points_fin_partie(self.partie.monPseudo, self.partie.monJoueur.chevalet.nb_point_total())
        else:
            self.view.update_joueurs()
        self.partie.etat = ETAT_PARTIE_FIN
        self.update_buttons()

    def gere_points_fin_partie(self, pseudo, nb_points_chevalet):
        self.partie.dicJoueurs[pseudo].ajouter_points(- nb_points_chevalet, True)
        self.partie.joueurTour.ajouter_points(nb_points_chevalet, True)
        self.view.update_joueurs()

    def mot_possible(self):
        lettres_placees = self.partie.plateau.get_lettres_placees()
        if len(lettres_placees) == 1:
            if (lettres_placees[0][1], lettres_placees[0][2]) == (7, 7) or \
                    len(self.partie.plateau.get_mot_colonne(lettres_placees[0][0], lettres_placees[0][1],
                                                            lettres_placees[0][2])) > 1 or \
                    len(self.partie.plateau.get_mot_ligne(lettres_placees[0][0], lettres_placees[0][1],
                                                          lettres_placees[0][2])) > 1:
                return True
        elif len(lettres_placees) != 0:
            mot_1 = self.partie.plateau.get_mot_ligne(lettres_placees[0][0], lettres_placees[0][1],
                                                      lettres_placees[0][2])
            mot_2 = self.partie.plateau.get_mot_colonne(lettres_placees[0][0], lettres_placees[0][1],
                                                        lettres_placees[0][2])
            for lettre_placee, _, _ in lettres_placees:
                if mot_1 is not None:
                    if lettre_placee not in mot_1:
                        mot_1 = None
                if mot_2 is not None:
                    if lettre_placee not in mot_2:
                        mot_2 = None

            if mot_1 is not None or mot_2 is not None:
                if mot_1 is not None:
                    for lettre_placee, ligne, colonne in lettres_placees:
                        if len(self.partie.plateau.get_mot_colonne(lettre_placee, ligne, colonne)) > 1:
                            return True
                        for lettre in self.partie.plateau.get_mot_ligne(lettre_placee, ligne, colonne):
                            if lettre.validee:
                                return True
                elif mot_2 is not None:
                    for lettre_placee, ligne, colonne in lettres_placees:
                        if len(self.partie.plateau.get_mot_ligne(lettre_placee, ligne, colonne)) > 1:
                            return True
                        for lettre in self.partie.plateau.get_mot_colonne(lettre_placee, ligne, colonne):
                            if lettre.validee:
                                return True
                for lettre_placee, ligne, colonne in lettres_placees:
                    if (ligne, colonne) == (7, 7):
                        return True
        return False

    def mot_existe(self):
        lettres_placees = self.partie.plateau.get_lettres_placees()
        if len(lettres_placees) > 0:
            for lettre_placee, ligne, colone in lettres_placees:
                for mot in [self.partie.plateau.get_mot_colonne(lettre_placee, ligne, colone),
                            self.partie.plateau.get_mot_ligne(lettre_placee, ligne, colone)]:
                    if not (len(mot) == 1 or mot_valide(self.partie.plateau.convert_mot_to_string(mot))):
                        return False
            if len(lettres_placees) == 1 and len(self.partie.plateau.get_mot_colonne(lettres_placees[0][0],
                                                                                     lettres_placees[0][1],
                                                                                     lettres_placees[0][2])) == 1 \
                    and len(self.partie.plateau.get_mot_ligne(lettres_placees[0][0], lettres_placees[0][1],
                                                              lettres_placees[0][2])) == 1:
                return False
            return True
        return False

    def calcule_score(self):
        score = 0
        lettres_placees = self.partie.plateau.get_lettres_placees()
        if len(lettres_placees) == 0:
            return False
        elif len(lettres_placees) == 1:
            liste_mots_a_compter = []
            for mot in [self.partie.plateau.get_mot_ligne(lettres_placees[0][0], lettres_placees[0][1],
                                                          lettres_placees[0][2]),
                        self.partie.plateau.get_mot_colonne(lettres_placees[0][0], lettres_placees[0][1],
                                                            lettres_placees[0][2])]:
                if len(mot) > 1:
                    liste_mots_a_compter.append(mot)
            if len(liste_mots_a_compter) == 0:
                liste_mots_a_compter.append([lettres_placees[0][0]])
        else:
            mot_vertical = (lettres_placees[1][0] in self.partie.plateau.get_mot_colonne(lettres_placees[0][0],
                                                                                         lettres_placees[0][1],
                                                                                         lettres_placees[0][2]))
            liste_mots_a_compter = []
            for lettre_placee, ligne, colonne in lettres_placees:
                if mot_vertical:
                    mot = self.partie.plateau.get_mot_ligne(lettre_placee, ligne, colonne)
                else:
                    mot = self.partie.plateau.get_mot_colonne(lettre_placee, ligne, colonne)
                if len(mot) > 1:
                    liste_mots_a_compter.append(mot)
            if mot_vertical:
                liste_mots_a_compter.append(self.partie.plateau.get_mot_colonne(lettres_placees[0][0],
                                                                                lettres_placees[0][1],
                                                                                lettres_placees[0][2]))
            else:
                liste_mots_a_compter.append(self.partie.plateau.get_mot_ligne(lettres_placees[0][0],
                                                                              lettres_placees[0][1],
                                                                              lettres_placees[0][2]))

        for mot in liste_mots_a_compter:
            coef_mot = 1
            nb_points_mot = 0
            for lettre in mot:
                if not lettre.validee:
                    ligne, colonne = self.partie.plateau.get_index_lettre(lettre)
                    natureCase = LISTE_NATURES_CASES[ligne][colonne]
                    if natureCase == TYPE_CASE_LETTRE_DOUBLE:
                        nb_points_mot += lettre.points
                    elif natureCase == TYPE_CASE_LETTRE_TRIPLE:
                        nb_points_mot += 2 * lettre.points
                    elif natureCase == TYPE_CASE_MOT_DOUBLE or natureCase == TYPE_CASE_DEPART_MOT_DOUBLE:
                        coef_mot *= 2
                    elif natureCase == TYPE_CASE_MOT_TRIPLE:
                        coef_mot *= 3
                nb_points_mot += lettre.points
            score += nb_points_mot * coef_mot
        if len(lettres_placees) == NB_LETTRES_MAX:
            score += 50
        return score

    def gere_score(self):
        self.view.motPossible = self.mot_possible()
        if self.view.motPossible:
            self.view.nouveau_score_actuel(self.calcule_score())
        else:
            self.view.nouveau_score_actuel(0)
        self.update_bouton_valider()

    def update_buttons(self):
        if self.partie.etat == ETAT_PARTIE_FIN:
            self.view.tous_boutons_non_clicable()
        else:
            self.view.update_bouton_jeter()
            self.update_bouton_valider()
            self.view.boutonPasser.clicable = (self.partie.sousEtatJeu == SOUS_ETAT_JEU_PASSER_PLACER_JETER)
            self.update_bouton_piocher()

    def update_bouton_valider(self):
        self.view.boutonValider.clicable = (self.partie.sousEtatJeu == SOUS_ETAT_JEU_PLACER_VALIDER
                                            and self.view.motPossible and self.mot_existe())

    def update_bouton_piocher(self):
        self.view.boutonPiocherLettres.clicable = False
        if self.partie.sousEtatJeu in [SOUS_ETAT_JEU_PIOCHER, SOUS_ETAT_JEU_JETER_PIOCHER]:
            if self.partie.joueurTourPiocher == self.partie.monJoueur:
                self.view.boutonPiocherLettres.clicable = True
            # Si plus de pioche on force le passage à l'état suivant
            if self.view.nbTuilesRestantes == 0:
                self.etat_partie_suivant(ACTION_PARTIE_PIOCHER)

    def gere_jeter(self):
        if self.view.boutonCaseSelectionne is not None:
            lettre = self.view.boutonCaseSelectionne.parametre
            if self.partie.monJoueur.chevalet.enlever_lettre(lettre):
                self.reseauClient.jeter(lettre.lettre)
                self.etat_partie_suivant(ACTION_PARTIE_JETER)
                self.view.deselectionner_case_selectionnee()
                self.lettresJetees.append(lettre.lettre)
                self.view.update_lettre_chevalet()

    def gere_passer(self):
        self.etat_partie_suivant(ACTION_PARTIE_PASSER)
        if self.partie.joueurTour == self.partie.monJoueur:
            self.reseauClient.passer()
        self.fin_tour()

    def gere_piocher(self):
        self.piocher_lettres()
        if self.partie.sousEtatJeu == SOUS_ETAT_JEU_JETER_PIOCHER:
            if len(self.lettresJetees) == NB_LETTRES_MAX and ((self.partie.nbTours < 16 and
                                                               self.jete_assez_consonnes_voyelles())
                                                              or (self.partie.nbTours >= 16 and
                                                                  self.jeter_que_consonne_ou_que_voyelle())):
                self.etat_partie_suivant(ACTION_PARTIE_PIOCHER_SPECIAL)
            else:
                self.etat_partie_suivant(ACTION_PARTIE_PIOCHER)
                self.reseauClient.passer()
                self.fin_tour()
        else:
            self.etat_partie_suivant(ACTION_PARTIE_PIOCHER)

    def run(self):
        if self.partie.sousEtatJeu == SOUS_ETAT_JEU_ATTENTE:
            if self.partie.joueurTourPiocher == self.partie.monJoueur:
                self.reseauClient.piocher_suivant()
                self.partie.joueur_piocher_suivant()
            if self.partie.monJoueur == self.partie.joueurTour:
                self.etat_partie_suivant(ACTION_PARTIE_MON_TOUR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if self.partie.etat == ETAT_PARTIE_LOGIN:
                    r = self.view.panneauDepart.gere_clavier(event)
                    if r is not None:
                        self.etat_depart_suivant(r)
                elif self.partie.etat != ETAT_PARTIE_MISE_EN_PLACE:
                    r = self.view.testMot.gere_clavier(event)
                    if r is not None:
                        self.view.testMot.valider(mot_valide(r))
                    if self.view.boutonCaseSelectionne is not None:
                        lettre_select = self.view.boutonCaseSelectionne.parametre
                        if lettre_select.points == 0 and not lettre_select.validee and \
                                lettre_select in self.partie.monJoueur.chevalet.cases:
                            newLettre = event.unicode.upper()
                            if newLettre in OCCURENCES_PAR_LETTRE:
                                lettre_select.lettre = newLettre
                                self.view.remake_bouton_case_select_chevalet()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                souris = pygame.mouse.get_pos()
                x_souris = souris[0]
                y_souris = souris[1]
                if event.button:
                    if self.partie.etat == ETAT_PARTIE_LOGIN:
                        r = self.view.panneauDepart.click(x_souris, y_souris)
                        if r is not None:
                            self.etat_depart_suivant(r)
                    elif self.partie.etat == ETAT_PARTIE_MISE_EN_PLACE:
                        if self.view.boutonDemarrer.clic(x_souris, y_souris):
                            self.reseauClient.demarrer()
                    else:
                        r = self.view.testMot.click(x_souris, y_souris)
                        if r is not None:
                            self.view.testMot.valider(mot_valide(r))
                        if self.partie.sousEtatJeu in [SOUS_ETAT_JEU_PASSER_PLACER_JETER, SOUS_ETAT_JEU_PLACER_VALIDER]:
                            r = self.view.click_sur_plateau(x_souris, y_souris)
                            if r is not None:
                                boutonCaseClickPlateau, lig, col = r
                                self.gere_click_plateau(boutonCaseClickPlateau, lig, col)
                                continue

                        if self.view.boutonValider.clic(x_souris, y_souris):
                            self.gere_valider()
                            continue
                        elif self.view.boutonJeterLettre.clic(x_souris, y_souris):
                            self.gere_jeter()
                            continue
                        elif self.view.boutonPasser.clic(x_souris, y_souris):
                            self.gere_passer()
                            continue
                        elif self.view.boutonPiocherLettres.clic(x_souris, y_souris):
                            self.gere_piocher()
                            continue

                        r = self.view.click_sur_chevalet(x_souris, y_souris)
                        if r is not None:
                            boutonCaseClickChevalet, i = r
                            self.gere_click_chevalet(boutonCaseClickChevalet, i)
                            continue

        if self.partie.etat != ETAT_PARTIE_LOGIN:
            for event in self.reseauClient.regardeEvenementsNonFait():
                eventType = event[PARAM_TYPE]
                eventContenu = event[PARAM_CONTENU]
                if eventType == TYPE_EVT_LOGIN:
                    self.partie.ajoute_joueur(event[PARAM_PSEUDO])
                    self.view.update_joueurs_mise_en_place()
                elif eventType == TYPE_EVT_FIN_PARTIE:
                    self.prepare_fin_partie()
                    self.reseauClient.envoie_points_chevalet(self.partie.monJoueur.chevalet.nb_point_total())
                elif eventType == TYPE_EVT_NB_POINTS_CHEVALET:
                    self.gere_points_fin_partie(event[PARAM_PSEUDO], eventContenu)
                elif eventType == TYPE_EVT_PLACER_LETTRE:
                    lettreStr = eventContenu[EVT_CONTENU_LETTRE]
                    ligne = eventContenu[EVT_CONTENU_LIGNE]
                    col = eventContenu[EVT_CONTENU_COLONNE]
                    joker = eventContenu[EVT_CONTENU_LETTRE_JOKER]
                    lettre = Lettre(lettreStr)
                    if joker:
                        lettre.points = 0
                    self.partie.plateau.placer_lettre(lettre, ligne, col)
                    self.view.update_lettre_plateau()
                    self.gere_score()
                elif eventType == TYPE_EVT_ENLEVER_LETTRE:
                    ligne = eventContenu[EVT_CONTENU_LIGNE]
                    col = eventContenu[EVT_CONTENU_COLONNE]
                    self.partie.plateau.vider_case(ligne, col)
                    self.view.update_lettre_plateau()
                    self.gere_score()
                elif eventType == TYPE_EVT_VALIDER:
                    self.gere_valider()
                elif eventType == TYPE_EVT_PASSER:
                    self.gere_passer()
                elif eventType == TYPE_EVT_LONGEUR_PIOCHE:
                    self.view.nouveau_nb_tuile_restante(eventContenu)
                elif eventType == TYPE_EVT_DEMARRER:
                    self.demarrer(eventContenu)
                elif eventType == TYPE_EVT_PIOCHER_SUIVANT:
                    self.partie.joueur_piocher_suivant()
                    self.update_bouton_piocher()
