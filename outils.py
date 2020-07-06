# coding: utf-8

# IP_PAR_DEFAUT = '86.194.73.178'
ADRESSE_IP = '127.0.0.1'
# ADRESSE_IP = 'onet.cavaliba.com'
PORT = '12800'

ETAT_PARTIE_LOGIN = -1
ETAT_PARTIE_MISE_EN_PLACE = 0
ETAT_PARTIE_JEU = 1
ETAT_PARTIE_FIN = 2

SOUS_ETAT_JEU_PIOCHER = 0
SOUS_ETAT_JEU_ATTENTE = 1
SOUS_ETAT_JEU_PASSER_PLACER_JETER = 2
SOUS_ETAT_JEU_PLACER_VALIDER = 3
SOUS_ETAT_JEU_JETER_PIOCHER = 4

ACTION_PARTIE_PIOCHER = 'ACTION_PARTIE_PIOCHER'
ACTION_PARTIE_PIOCHER_SPECIAL = 'ACTION_PARTIE_PIOCHER_SPECIAL'
ACTION_PARTIE_JETER = 'ACTION_PARTIE_JETER'
ACTION_PARTIE_PLACER = 'ACTION_PARTIE_PLACER'
ACTION_PARTIE_ENLEVER_DERNIERE_LETTRE = 'ACTION_PARTIE_ENLEVER_DERNIERE_LETTRE'
ACTION_PARTIE_MON_TOUR = 'ACTION_PARTIE_MON_TOUR'
ACTION_PARTIE_VALIDER = 'ACTION_PARTIE_VALIDER'
ACTION_PARTIE_VALIDER_PIOCHE_VIDE = 'ACTION_PARTIE_VALIDER_PIOCHE_VIDE'
ACTION_PARTIE_PASSER = 'ACTION_PARTIE_PASSER'


AUTOMATE_PARTIE = {
    SOUS_ETAT_JEU_JETER_PIOCHER: {ACTION_PARTIE_PIOCHER: SOUS_ETAT_JEU_ATTENTE,
                                  ACTION_PARTIE_PIOCHER_SPECIAL: SOUS_ETAT_JEU_PASSER_PLACER_JETER},
    SOUS_ETAT_JEU_ATTENTE: {ACTION_PARTIE_MON_TOUR: SOUS_ETAT_JEU_PASSER_PLACER_JETER},
    SOUS_ETAT_JEU_PASSER_PLACER_JETER: {ACTION_PARTIE_JETER: SOUS_ETAT_JEU_JETER_PIOCHER,
                                        ACTION_PARTIE_PLACER: SOUS_ETAT_JEU_PLACER_VALIDER,
                                        ACTION_PARTIE_PASSER: SOUS_ETAT_JEU_ATTENTE},
    SOUS_ETAT_JEU_PLACER_VALIDER: {ACTION_PARTIE_VALIDER: SOUS_ETAT_JEU_PIOCHER,
                                   ACTION_PARTIE_VALIDER_PIOCHE_VIDE: SOUS_ETAT_JEU_ATTENTE,
                                   ACTION_PARTIE_ENLEVER_DERNIERE_LETTRE: SOUS_ETAT_JEU_PASSER_PLACER_JETER},
    SOUS_ETAT_JEU_PIOCHER: {ACTION_PARTIE_PIOCHER: SOUS_ETAT_JEU_ATTENTE}
}

TAILLE_PLATEAU = 15
NB_CASES_CHEVALET = 13
NB_LETTRES_MAX = 7

TYPE_CASE_NORMAL = 0
TYPE_CASE_MOT_TRIPLE = 1
TYPE_CASE_MOT_DOUBLE = 2
TYPE_CASE_LETTRE_TRIPLE = 3
TYPE_CASE_LETTRE_DOUBLE = 4
TYPE_CASE_DEPART_MOT_DOUBLE = 5
LISTE_NATURES_CASES = [[TYPE_CASE_NORMAL for col in range(TAILLE_PLATEAU)] for lig in range(TAILLE_PLATEAU)]
liste = [[0, 0], [0, 7], [0, 14], [7, 0],
         [7, 14], [14, 0], [14, 7], [14, 14]]
for lig, col in liste:
    LISTE_NATURES_CASES[lig][col] = TYPE_CASE_MOT_TRIPLE
liste = [[1, 1], [2, 2], [3, 3], [4, 4], [10, 10], [11, 11], [12, 12], [13, 13],
         [1, 13], [2, 12], [3, 11], [4, 10], [10, 4], [11, 3], [12, 2], [13, 1]]
for lig, col in liste:
    LISTE_NATURES_CASES[lig][col] = TYPE_CASE_MOT_DOUBLE
liste = [[0, 3], [0, 11], [2, 6], [2, 8], [3, 0], [3, 7], [3, 14], [6, 2], [6, 6], [6, 8], [6, 12], [7, 3],
         [7, 11], [8, 2], [8, 6], [8, 8], [8, 12], [11, 0], [11, 7], [11, 14], [12, 6], [12, 8], [14, 3], [14, 11]]
for lig, col in liste:
    LISTE_NATURES_CASES[lig][col] = TYPE_CASE_LETTRE_DOUBLE
liste = [[1, 5], [13, 5], [1, 9], [13, 9], [5, 1], [9, 1],
         [5, 5], [9, 5], [5, 9], [9, 9], [5, 13], [9, 13]]
for lig, col in liste:
    LISTE_NATURES_CASES[lig][col] = TYPE_CASE_LETTRE_TRIPLE

LISTE_NATURES_CASES[7][7] = TYPE_CASE_DEPART_MOT_DOUBLE

POINTS_PAR_LETTRE = {'A': 1,
                     'B': 3,
                     'C': 3,
                     'D': 2,
                     'E': 1,
                     'F': 4,
                     'G': 2,
                     'H': 4,
                     'I': 1,
                     'J': 8,
                     'K': 10,
                     'L': 1,
                     'M': 2,
                     'N': 1,
                     'O': 1,
                     'P': 3,
                     'Q': 8,
                     'R': 1,
                     'S': 1,
                     'T': 1,
                     'U': 1,
                     'V': 4,
                     'W': 10,
                     'X': 10,
                     'Y': 10,
                     'Z': 10,
                     '*': 0}

OCCURENCES_PAR_LETTRE = {'A': 9,
                         'B': 2,
                         'C': 2,
                         'D': 3,
                         'E': 15,
                         'F': 2,
                         'G': 2,
                         'H': 2,
                         'I': 8,
                         'J': 1,
                         'K': 1,
                         'L': 5,
                         'M': 3,
                         'N': 6,
                         'O': 6,
                         'P': 2,
                         'Q': 1,
                         'R': 6,
                         'S': 6,
                         'T': 6,
                         'U': 6,
                         'V': 2,
                         'W': 1,
                         'X': 1,
                         'Y': 1,
                         'Z': 1,
                         '*': 2}

VOYELLES = ['A', 'E', 'I', 'O', 'U', 'Y']

JOKER = '*'
