CHEMIN_FICHIER_DICO = 'french.dic'

DICTIONNAIRE = []

fichier = open(CHEMIN_FICHIER_DICO, 'r')
for mot in fichier:
    DICTIONNAIRE.append(mot.rstrip())
DICTIONNAIRE = tuple(DICTIONNAIRE)


def mot_valide(mot: str):
    return mot.upper() in DICTIONNAIRE
