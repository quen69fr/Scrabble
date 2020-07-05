# coding: utf-8

from model import *
from affichage import *
from outils import *


pygame.mixer.init(22100, -16, 2, 64)

AUDIO_MON_TOUR = pygame.mixer.Sound("Audio/MonTour.wav")
AUDIO_TOUR_SUIVANT = pygame.mixer.Sound("Audio/TourSuivant.wav")
AUDIO_PLUS_DE_LETTRE = pygame.mixer.Sound("Audio/PlusDeLettre.wav")
AUDIO_POSER_LETTRE = pygame.mixer.Sound("Audio/PoserLettre.wav")


BEIGE_1 = (211, 166, 114)
BEIGE_2 = (255, 199, 135)
BEIGE_3 = (158, 123, 83)
BLEU_1 = (29, 167, 211)
BLEU_2 = (0, 83, 209)
ROUGE_1 = (255, 110, 110)
ROUGE_2 = (255, 0, 0)
ROUGE_3 = (150, 0, 0)
VERT_SCRABBLE = (57, 173, 57)
COULEUR_FONT = VERT_SCRABBLE

IMAGE_ETOILE = pygame.image.load('Images/Etoile.png')
IMAGE_SAC = pygame.image.load('Images/Sac.png')

COTE_CASE = 40
MARGE_CASE = 3
MARGES = 18
X_PLATEAU = 679
Y_PLATEAU = MARGES
MARGE_PLATEAU = 10

Y_PANNEAU_DEPART = 290
HAUTEUR_PANNEAU_DEPART = 205
Y_TEXTE_DEPART = Y_PANNEAU_DEPART + 12
Y_BOUTON_VALIDER_DEPART = Y_PANNEAU_DEPART + 150
Y_BARRE_TEXTE = Y_PANNEAU_DEPART + 75
LARGEUR_BARRE_TEXTE = 400
HAUTEUR_BARRE_TEXTE = 50

Y_PANNEAU_ATTENT_JOUEUR = 220
LARGEUR_PANNEAU_ATTENT_JOUEUR = 360
HAUTEUR_PANNEAU_ATTENT_JOUEUR = 365
Y_TEXTE_JOUEUR_PRESENT = Y_PANNEAU_ATTENT_JOUEUR + 10
Y_BOUTON_DEMARRER = Y_PANNEAU_ATTENT_JOUEUR + 290
Y_JOUEUR_MISE_EN_PLACE = Y_PANNEAU_ATTENT_JOUEUR + 72
ECART_JOUEUR_MISE_EN_PLACE = 50

Y_PANNEAU_INFOS = 140
HAUTEUR_PANNEAU_INFOS = 100
LARGEUR_TOUR_PANNEAU_INFOS = 100
X_IMAGE_SAC = 2 * MARGES + LARGEUR_TOUR_PANNEAU_INFOS + 364
X_SCORE_ACTUEL = 2 * MARGES + LARGEUR_TOUR_PANNEAU_INFOS + 40

Y_JOUEURS = Y_PANNEAU_INFOS + HAUTEUR_PANNEAU_INFOS + 40
HAUTEUR_JOUEURS = 95

Y_MON_JOUEUR = Y_JOUEURS + HAUTEUR_JOUEURS + 16
HAUTEUR_MON_JOUEUR = 150

Y_CHEVALET = Y_MON_JOUEUR + 22

Y_BOUTONS_MON_JOUEUR = Y_MON_JOUEUR + 22 + 60
HAUTEUR_BOUTON_MON_JOUEUR = 50

Y_TEST_MOT = Y_MON_JOUEUR + HAUTEUR_MON_JOUEUR + 40
HAUTEUR_TEST_MOT = HAUTEUR - Y_TEST_MOT - 20
X_BARRE_TEXTE_TEST_MOT = MARGES + 10
Y_BARRE_TEXTE_TEST_MOT = Y_TEST_MOT + 10
LARGEUR_BARRE_TEXTE_TEST_MOT = 500
HAUTEUR_BARRE_TEXTE_TEST_MOT = 40


def cree_bouton_lettre(x: int, y: int, lettre: Lettre, couleurContour: tuple = None):
    largeurContours = 3
    if couleurContour is None:
        couleurContour = BEIGE_3
        largeurContours = 2
    coteSur2 = int(COTE_CASE / 2)
    taillePolice = 25
    listeEcrans = []
    if lettre.points == 0:
        taillePolice = 15
    else:
        listeEcrans.append(Text(str(lettre.points), coteSur2 + 6, coteSur2 + 6, 12))
    listeEcrans.append(Text(lettre.lettre, coteSur2, coteSur2, taillePolice, x_0left_1centre_2right=1,
                            y_0top_1centre_2bottom=1))

    return bouton_avec_ecrans(listeEcrans, x, y, COTE_CASE, COTE_CASE, couleurFont=BEIGE_1,
                              largeurContours=largeurContours,
                              couleurContours=couleurContour, parametre=lettre)


def cree_bouton_case_chevalet(i: int, lettre: Lettre = None):
    x_chevalet = int(X_PLATEAU / 2 - (NB_CASES_CHEVALET * (COTE_CASE + MARGE_CASE) - MARGE_CASE) / 2)
    x = x_chevalet + i * (COTE_CASE + MARGE_CASE)
    y = Y_CHEVALET
    if lettre is None:
        return bouton_avec_ecrans([], x, y, COTE_CASE, COTE_CASE, couleurFont=GRIS_CLAIR, parametre=lettre)
    else:
        return cree_bouton_lettre(x, y, lettre)


def cree_bouton_case_plateau(colonne: int, ligne: int, lettre: Lettre = None):
    x = X_PLATEAU + colonne * (COTE_CASE + MARGE_CASE) + MARGE_PLATEAU
    y = Y_PLATEAU + ligne * (COTE_CASE + MARGE_CASE) + MARGE_PLATEAU

    coteSur2 = int(COTE_CASE / 2)
    listeEcrans = []
    couleurFont = None
    typeCase = LISTE_NATURES_CASES[ligne][colonne]
    t1 = None
    t2 = None
    if typeCase != TYPE_CASE_NORMAL:
        if typeCase == TYPE_CASE_LETTRE_DOUBLE:
            couleurFont = BLEU_1
            t1 = 'LETTRE'
            t2 = 'DOUBLE'
        elif typeCase == TYPE_CASE_LETTRE_TRIPLE:
            couleurFont = BLEU_2
            t1 = 'LETTRE'
            t2 = 'TRIPLE'
        elif typeCase == TYPE_CASE_MOT_DOUBLE or typeCase == TYPE_CASE_DEPART_MOT_DOUBLE:
            couleurFont = ROUGE_1
            t1 = 'MOT'
            t2 = 'DOUBLE'
        else:
            couleurFont = ROUGE_2
            t1 = 'MOT'
            t2 = 'TRIPLE'

    if lettre is None:
        if typeCase == TYPE_CASE_DEPART_MOT_DOUBLE:
            return bouton_avec_ecrans([Image(IMAGE_ETOILE, coteSur2, coteSur2, x_0left_1centre_2right=1,
                                             y_0top_1centre_2bottom=1)], x, y, COTE_CASE, COTE_CASE,
                                      couleurFont=couleurFont)
        else:
            if couleurFont is None:
                couleurFont = GRIS_CLAIR
            if t1 is not None and t2 is not None:
                listeEcrans.append(Text(t1, coteSur2, coteSur2 - 4, 8,
                                        x_0left_1centre_2right=1, y_0top_1centre_2bottom=2))
                listeEcrans.append(Text('COMPTE', coteSur2, coteSur2, 8,
                                        x_0left_1centre_2right=1, y_0top_1centre_2bottom=1))
                listeEcrans.append(Text(t2, coteSur2, coteSur2 + 4, 8,
                                        x_0left_1centre_2right=1, y_0top_1centre_2bottom=0))
            return bouton_avec_ecrans(listeEcrans, x, y, COTE_CASE, COTE_CASE, couleurFont=couleurFont)

    else:
        return cree_bouton_lettre(x, y, lettre, couleurContour=couleurFont)


class AfficheJoueur:
    def __init__(self, joueur: Joueur, i: int, nbJoueurs: int, monTour: bool):
        self.joueur = joueur
        largeur = (X_PLATEAU - 1.5 * MARGES) / nbJoueurs
        self.rect = Rectangle(int(MARGES + i * largeur), Y_JOUEURS, int(largeur - MARGES / 2), HAUTEUR_JOUEURS, NOIR,
                              pleinOuLargeurContour=3, couleurFont=BLANC)
        self.rectSelect = Rectangle(self.rect.x, self.rect.y, self.rect.largeur, self.rect.hauteur, NOIR,
                                    pleinOuLargeurContour=6, couleurFont=BLANC)
        m2 = 6
        self.pseudo = Text(self.joueur.pseudo.upper(), int(self.rect.x + self.rect.largeur / 2), Y_JOUEURS + m2 + 5,
                           x_0left_1centre_2right=1)
        self.score = Text(f'Score : {self.joueur.score}', self.rect.x + m2, Y_JOUEURS + 45, taillePolice=22)
        self.dernierScore = Text(f'Dernier mot : {self.joueur.dernierScore}', self.rect.x + m2, Y_JOUEURS + 70,
                                 taillePolice=17)
        self.monTour = monTour

    def update(self, monTour=None):
        m2 = 6
        self.score = Text(f'Score : {self.joueur.score}', self.rect.x + m2, Y_JOUEURS + 45, taillePolice=22)
        self.dernierScore = Text(f'Dernier mot : {self.joueur.dernierScore}', self.rect.x + m2, Y_JOUEURS + 70,
                                 taillePolice=17)
        if monTour is not None:
            self.monTour = monTour

    def affiche(self, screen):
        if self.monTour:
            self.rectSelect.affiche(screen)
        else:
            self.rect.affiche(screen)
        self.pseudo.affiche(screen)
        self.score.affiche(screen)
        self.dernierScore.affiche(screen)


class PanneauDepart:
    def __init__(self):
        self.rectangle = Rectangle(MARGES, Y_PANNEAU_DEPART, X_PLATEAU - 2 * MARGES, HAUTEUR_PANNEAU_DEPART, NOIR,
                                   pleinOuLargeurContour=4, couleurFont=BLANC)
        self.barreTexte = BarreTexte(Rectangle(int(X_PLATEAU / 2), Y_BARRE_TEXTE, LARGEUR_BARRE_TEXTE,
                                               HAUTEUR_BARRE_TEXTE, GRIS_FONCE, 3, x_0left_1centre_2right=1),
                                     texte_x_0left_1centre_2right=1, texteDepart=IP_PAR_DEFAUT, tailleTexte=35)
        self.texte2 = Text('Pseudo', int(X_PLATEAU / 2), Y_TEXTE_DEPART, 50, x_0left_1centre_2right=1)
        self.texte1 = Text('Adresse ip', int(X_PLATEAU / 2), Y_TEXTE_DEPART, 50, x_0left_1centre_2right=1)
        self.bouonValider = bouton_autour_ecran(Text('Valider', int(X_PLATEAU / 2), Y_BOUTON_VALIDER_DEPART,
                                                     x_0left_1centre_2right=1))
        self.etat = 1

    def gere_clavier(self, keyEvent: pygame.event):
        return self.barreTexte.gere_clavier(keyEvent)

    def click(self, x_souris: int, y_souris: int):
        if self.bouonValider.clic(x_souris, y_souris):
            return self.barreTexte.valider()
        return None

    def affiche(self, screen: pygame.Surface):
        self.rectangle.affiche(screen)
        self.barreTexte.affiche(screen)
        if self.etat == 1:
            self.texte1.affiche(screen)
        else:
            self.texte2.affiche(screen)
        self.bouonValider.affiche(screen)


class TestMot:
    def __init__(self):
        self.rectangle = Rectangle(MARGES, Y_TEST_MOT, X_PLATEAU - 2 * MARGES, HAUTEUR_TEST_MOT, NOIR,
                                   pleinOuLargeurContour=4, couleurFont=BLANC)
        self.barreTexte = BarreTexte(Rectangle(X_BARRE_TEXTE_TEST_MOT, Y_BARRE_TEXTE_TEST_MOT,
                                               LARGEUR_BARRE_TEXTE_TEST_MOT, HAUTEUR_BARRE_TEXTE_TEST_MOT,
                                               GRIS_FONCE, 3), selectionneAuto=True, selectionne=False,
                                     nbCaracteresMax=16, texteSupAutoSiValider=False)
        m = 10
        self.boutonValidee = bouton_avec_ecrans([Text('Tester', 0, 0)], X_BARRE_TEXTE_TEST_MOT +
                                                LARGEUR_BARRE_TEXTE_TEST_MOT + m, Y_BARRE_TEXTE_TEST_MOT,
                                                self.rectangle.largeur - LARGEUR_BARRE_TEXTE_TEST_MOT - 3 * m,
                                                HAUTEUR_BARRE_TEXTE_TEST_MOT, centrerTOUSLesEcrans=True)
        self.texteOui = Text('Ce mot est accepté.',
                             int(X_BARRE_TEXTE_TEST_MOT + LARGEUR_BARRE_TEXTE_TEST_MOT / 2),
                             int(Y_BARRE_TEXTE_TEST_MOT + (self.rectangle.hauteur + self.rectangle.y -
                                                           Y_BARRE_TEXTE_TEST_MOT + HAUTEUR_BARRE_TEXTE_TEST_MOT) / 2),
                             x_0left_1centre_2right=1, y_0top_1centre_2bottom=1, couleur=VERT_SCRABBLE, taillePolice=25)
        self.texteNon = Text("Ce mot n'est pas accepté.",
                             int(X_BARRE_TEXTE_TEST_MOT + LARGEUR_BARRE_TEXTE_TEST_MOT / 2),
                             int(Y_BARRE_TEXTE_TEST_MOT + (self.rectangle.hauteur + self.rectangle.y -
                                                           Y_BARRE_TEXTE_TEST_MOT + HAUTEUR_BARRE_TEXTE_TEST_MOT) / 2),
                             x_0left_1centre_2right=1, y_0top_1centre_2bottom=1, couleur=ROUGE_3, taillePolice=25)
        self.texteAccepte = None

    def valider(self, mot_possible: bool):
        self.texteAccepte = mot_possible

    def affiche(self, screen: pygame.Surface):
        self.rectangle.affiche(screen)
        self.barreTexte.affiche(screen)
        self.boutonValidee.affiche(screen)
        if self.texteAccepte is not None:
            if self.texteAccepte:
                self.texteOui.affiche(screen)
            else:
                self.texteNon.affiche(screen)

    def gere_clavier(self, keyEvent: pygame.event):
        r = self.barreTexte.gere_clavier(keyEvent)
        if r is None and self.barreTexte.selectionne:
            self.texteAccepte = None
        return r

    def click(self, x_souris: int, y_souris: int):
        self.barreTexte.clic(x_souris, y_souris)
        if self.boutonValidee.clic(x_souris, y_souris):
            return self.barreTexte.valider()
        return None


class View:
    def __init__(self, partie: Partie):
        self.partie = partie
        pygame.init()
        pygame.display.set_caption(CAPTION)
        if PLEIN_ECRAN:
            self.mainScreen = pygame.display.set_mode((LARGEUR, HAUTEUR), FULLSCREEN)
        else:
            self.mainScreen = pygame.display.set_mode((LARGEUR, HAUTEUR))

        self.boutonCaseSelectionne = None
        self.motPossible = False
        self.nbPointsMot = 0
        self.nbTuilesRestantes = sum(OCCURENCES_PAR_LETTRE.values())

        self.texteTitre = Text('SCRABBLE', int(X_PLATEAU / 2), Y_PLATEAU, x_0left_1centre_2right=1, taillePolice=100)

        # attente joueur
        self.panneauDepart = PanneauDepart()
        self.rectangleAttenteJoueur = Rectangle(int(X_PLATEAU / 2), Y_PANNEAU_ATTENT_JOUEUR,
                                                LARGEUR_PANNEAU_ATTENT_JOUEUR, HAUTEUR_PANNEAU_ATTENT_JOUEUR,
                                                NOIR, 3, BLANC, x_0left_1centre_2right=1)
        self.texteJoueurPresent = Text('Joueurs présents', int(X_PLATEAU / 2), Y_TEXTE_JOUEUR_PRESENT, 38,
                                       x_0left_1centre_2right=1)
        self.boutonDemarrer = bouton_autour_ecran(Text('Démarrer', int(X_PLATEAU / 2), Y_BOUTON_DEMARRER, 50,
                                                       x_0left_1centre_2right=1), margeContoursX=20)
        self.listeTexteJoueursMiseEnPlace = []

        # plateau
        n = (COTE_CASE + MARGE_CASE) * TAILLE_PLATEAU + 2 * MARGE_PLATEAU - MARGE_CASE
        self.rectanglePlateau = Rectangle(X_PLATEAU, Y_PLATEAU, n, n, NOIR, 4, BLANC)
        self.plateau = [[cree_bouton_case_plateau(colone, ligne) for colone in range(TAILLE_PLATEAU)]
                        for ligne in range(TAILLE_PLATEAU)]

        # joueurs
        self.joueursAffichage = []

        # mon_joueur
        self.maBulle = None
        self.maBulleSelect = None
        self.chevalet = [cree_bouton_case_chevalet(i) for i in range(NB_CASES_CHEVALET)]
        x = 2 * MARGES
        n = MARGES / 2
        large = (X_PLATEAU - 5.5 * MARGES) / 4 + n
        self.boutonValider = bouton_avec_ecrans([Text('Valider', 0, 0)], x, Y_BOUTONS_MON_JOUEUR, large - n,
                                                HAUTEUR_BOUTON_MON_JOUEUR, centrerTOUSLesEcrans=True)
        self.boutonJeterLettre = bouton_avec_ecrans([Text('Jeter', 0, 0)], x + large, Y_BOUTONS_MON_JOUEUR, large - n,
                                                    HAUTEUR_BOUTON_MON_JOUEUR, centrerTOUSLesEcrans=True)
        self.boutonPiocherLettres = bouton_avec_ecrans([Text('Piocher', 0, 0)],
                                                       x + 2 * large, Y_BOUTONS_MON_JOUEUR, large - n,
                                                       HAUTEUR_BOUTON_MON_JOUEUR, centrerTOUSLesEcrans=True)
        self.boutonPasser = bouton_avec_ecrans([Text('Passer', 0, 0)], x + 3 * large, Y_BOUTONS_MON_JOUEUR, large - n,
                                               HAUTEUR_BOUTON_MON_JOUEUR, centrerTOUSLesEcrans=True)

        # Panneau infos
        self.rectanglePanneauInfos = Rectangle(2 * MARGES + LARGEUR_TOUR_PANNEAU_INFOS, Y_PANNEAU_INFOS,
                                               X_PLATEAU - 3 * MARGES - LARGEUR_TOUR_PANNEAU_INFOS,
                                               HAUTEUR_PANNEAU_INFOS,  NOIR, 3, BLANC)
        self.rectangleTourPanneauInfos = Rectangle(MARGES, Y_PANNEAU_INFOS, LARGEUR_TOUR_PANNEAU_INFOS,
                                                   HAUTEUR_PANNEAU_INFOS, NOIR, 3, BLANC)
        self.imageSac = Image(IMAGE_SAC, X_IMAGE_SAC, int(Y_PANNEAU_INFOS + HAUTEUR_PANNEAU_INFOS / 2),
                              y_0top_1centre_2bottom=1)
        self.texteScoreActuel = None
        self.texteNbTuilesRestantes = None
        self.texteNbTour = None
        self.texteNbTour2 = Text('Tour',
                                 int(self.rectangleTourPanneauInfos.x + self.rectangleTourPanneauInfos.largeur / 2),
                                 self.rectangleTourPanneauInfos.y + 6, x_0left_1centre_2right=1, taillePolice=25)

        # Test mots
        self.testMot = TestMot()

        self.texteFin = Text('Fin de la partie !', int(X_PLATEAU / 2), Y_BOUTONS_MON_JOUEUR, 50, couleur=GRIS_FONCE,
                             x_0left_1centre_2right=1)

    def demarrer(self):
        listeOrdrePseudos = self.partie.listeOrdrePseudos
        for i, pseudo in enumerate(listeOrdrePseudos):
            self.joueursAffichage.append(AfficheJoueur(self.partie.dicJoueurs[pseudo], i, len(listeOrdrePseudos),
                                                       (self.partie.dicJoueurs[pseudo] == self.partie.joueurTour)))
            if pseudo == self.partie.monPseudo:
                self.maBulle = BulleRectanle(MARGES, Y_MON_JOUEUR, X_PLATEAU - 2 * MARGES, HAUTEUR_MON_JOUEUR, 0,
                                             largeurContours=2,
                                             x_ou_y_fleche=int(self.joueursAffichage[i].rect.x +
                                                               self.joueursAffichage[i].rect.largeur / 2))
                self.maBulleSelect = BulleRectanle(MARGES, Y_MON_JOUEUR, X_PLATEAU - 2 * MARGES, HAUTEUR_MON_JOUEUR, 0,
                                                   largeurContours=5,
                                                   x_ou_y_fleche=int(self.joueursAffichage[i].rect.x +
                                                                     self.joueursAffichage[i].rect.largeur / 2))
        self.update_joueurs()

    def deselectionner_case_selectionnee(self):
        if self.boutonCaseSelectionne is not None:
            self.boutonCaseSelectionne.selectionne = False
            self.boutonCaseSelectionne = None
            self.update_lettre_chevalet()
            return True
        return False

    def selectionner_case(self, case: Bouton):
        deja_selectionne = (self.boutonCaseSelectionne == case)
        if self.boutonCaseSelectionne is not None:
            self.deselectionner_case_selectionnee()
        if not deja_selectionne:
            self.boutonCaseSelectionne = case
            self.boutonCaseSelectionne.selectionne = True

    def update_plateau(self):
        for nbLig, ligne in enumerate(self.partie.plateau.cases):
            for nbCol, case in enumerate(ligne):
                boutonCase = self.plateau[nbLig][nbCol]
                if case != boutonCase.parametre:
                    self.plateau[nbLig][nbCol] = cree_bouton_case_plateau(nbCol, nbLig, case)
                    boutonCase = self.plateau[nbLig][nbCol]
                    if boutonCase.parametre is not None:
                        AUDIO_POSER_LETTRE.play()
                if case is not None and case.validee and boutonCase.rectangle.couleurFont == BEIGE_1:
                    boutonCase.rectangle.couleurFont = BEIGE_2
                    boutonCase.rectangle.couleur = BEIGE_3
                    boutonCase.rectangle.width = 2

    def click_sur_plateau(self, x_souris, y_souris):
        for nb_l, ligne in enumerate(self.plateau):
            for nb_c, case in enumerate(ligne):
                if case.clic(x_souris, y_souris):
                    return case, nb_l, nb_c
        return None

    def affiche_plateau(self):
        self.rectanglePlateau.affiche(self.mainScreen)
        for ligne in self.plateau:
            for case in ligne:
                case.affiche(self.mainScreen)

    def remake_bouton_case_select_chevalet(self):
        if self.boutonCaseSelectionne is not None:
            for i, case in enumerate(self.chevalet):
                if case == self.boutonCaseSelectionne:
                    self.chevalet[i] = cree_bouton_case_chevalet(i, case.parametre)
                    return True
        return False

    def update_chevalet(self):
        for i, case in enumerate(self.partie.monJoueur.chevalet.cases):
            boutonCase = self.chevalet[i]
            if case != boutonCase.parametre:
                self.chevalet[i] = cree_bouton_case_chevalet(i, case)

    def click_sur_chevalet(self, x_souris, y_souris):
        for i, case in enumerate(self.chevalet):
            if case.clic(x_souris, y_souris):
                return case, i
        return None

    def affiche_chevalet(self):
        for caseChevalet in self.chevalet:
            caseChevalet.affiche(self.mainScreen)

    def update_joueurs(self):
        for joueurAffichage in self.joueursAffichage:
            if joueurAffichage.joueur == self.partie.joueurTour:
                if not joueurAffichage.monTour:
                    if joueurAffichage.joueur == self.partie.monJoueur:
                        AUDIO_MON_TOUR.play()
                    else:
                        AUDIO_TOUR_SUIVANT.play()
            joueurAffichage.update((joueurAffichage.joueur == self.partie.joueurTour))
        self.texteNbTour = Text(str(self.partie.nbTours),
                                int(self.rectangleTourPanneauInfos.x + self.rectangleTourPanneauInfos.largeur / 2),
                                self.rectangleTourPanneauInfos.y + 30, x_0left_1centre_2right=1, taillePolice=70)

    def affiche_joueurs(self):
        for joueurAffichage in self.joueursAffichage:
            joueurAffichage.affiche(self.mainScreen)

    def update_bouton_jeter(self):
        self.boutonJeterLettre.clicable = (self.partie.sousEtatJeu in [SOUS_ETAT_JEU_JETER_PIOCHER,
                                                                       SOUS_ETAT_JEU_PASSER_PLACER_JETER]
                                           and self.boutonCaseSelectionne is not None
                                           and self.nbTuilesRestantes >= 7)

    def tous_boutons_non_clicable(self):
        self.boutonJeterLettre.clicable = False
        self.boutonValider.clicable = False
        self.boutonPasser.clicable = False
        self.boutonPiocherLettres.clicable = False

    def affiche_mon_joueur(self):
        if self.maBulle is not None:
            if self.partie.joueurTour == self.partie.monJoueur:
                self.maBulleSelect.affiche(self.mainScreen)
            else:
                self.maBulle.affiche(self.mainScreen)
        self.affiche_chevalet()

        if self.partie.etat == ETAT_PARTIE_FIN:
            self.texteFin.affiche(self.mainScreen)
        else:
            self.boutonValider.affiche(self.mainScreen)
            self.boutonJeterLettre.affiche(self.mainScreen)
            self.boutonPiocherLettres.affiche(self.mainScreen)
            self.boutonPasser.affiche(self.mainScreen)

    def update_lettre_plateau(self):
        self.update_plateau()

    def update_lettre_chevalet(self):
        self.update_chevalet()
        self.update_bouton_jeter()

    def update_all(self):
        self.update_joueurs()
        self.update_lettre_plateau()
        self.update_lettre_chevalet()
        self.update_score_actuel()
        self.update_nb_tuiles_restantes()
        self.update_joueurs_mise_en_place()

    def nouveau_score_actuel(self, nouveauScore: int):
        self.nbPointsMot = nouveauScore
        self.update_score_actuel()

    def nouveau_nb_tuile_restante(self, n: int):
        if n == 0 and not self.nbTuilesRestantes == 0:
            AUDIO_PLUS_DE_LETTRE.play()
        self.nbTuilesRestantes = n
        self.update_nb_tuiles_restantes()

    def affiche_panneau_info_partie(self):
        self.rectangleTourPanneauInfos.affiche(self.mainScreen)
        self.rectanglePanneauInfos.affiche(self.mainScreen)
        self.imageSac.affiche(self.mainScreen)
        self.texteNbTour2.affiche(self.mainScreen)
        self.texteNbTour.affiche(self.mainScreen)
        self.texteScoreActuel.affiche(self.mainScreen)
        self.texteNbTuilesRestantes.affiche(self.mainScreen)

    def update_score_actuel(self):
        self.texteScoreActuel = Text(f'Score actuel : {self.nbPointsMot}', X_SCORE_ACTUEL,
                                     int(self.rectanglePanneauInfos.y + self.rectanglePanneauInfos.hauteur / 2),
                                     y_0top_1centre_2bottom=1)

    def update_nb_tuiles_restantes(self):
        self.texteNbTuilesRestantes = Text(str(self.nbTuilesRestantes),
                                           int(self.imageSac.x + self.imageSac.largeur / 2),
                                           int(self.imageSac.y + self.imageSac.hauteur / 2), couleur=GRIS_CLAIR,
                                           x_0left_1centre_2right=1)

    def update_joueurs_mise_en_place(self):
        if len(self.listeTexteJoueursMiseEnPlace) != len(self.partie.dicJoueurs):
            self.listeTexteJoueursMiseEnPlace = []
            for i, pseudo in enumerate(self.partie.dicJoueurs):
                if self.partie.monPseudo == pseudo:
                    t = f'Vous : {pseudo}'
                else:
                    t = pseudo
                self.listeTexteJoueursMiseEnPlace.append(Text(t, int(X_PLATEAU / 2),
                                                              Y_JOUEUR_MISE_EN_PLACE + i * ECART_JOUEUR_MISE_EN_PLACE,
                                                              couleur=GRIS_FONCE, x_0left_1centre_2right=1))

    def affiche_mise_en_place(self):
        self.rectangleAttenteJoueur.affiche(self.mainScreen)
        self.texteJoueurPresent.affiche(self.mainScreen)
        self.boutonDemarrer.affiche(self.mainScreen)
        for texteJoueurMiseEnPlace in self.listeTexteJoueursMiseEnPlace:
            texteJoueurMiseEnPlace.affiche(self.mainScreen)

    def affiche(self):
        self.mainScreen.fill(COULEUR_FONT)

        self.texteTitre.affiche(self.mainScreen)
        self.affiche_plateau()
        if self.partie.etat == ETAT_PARTIE_LOGIN:
            self.panneauDepart.affiche(self.mainScreen)
        elif self.partie.etat == ETAT_PARTIE_MISE_EN_PLACE:
            self.affiche_mise_en_place()
        else:
            self.affiche_joueurs()
            self.affiche_mon_joueur()
            self.affiche_panneau_info_partie()
            self.testMot.affiche(self.mainScreen)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
