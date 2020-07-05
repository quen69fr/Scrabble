# coding: utf-8

import pygame.gfxdraw
from pygame.locals import FULLSCREEN
from math import sqrt, cos, sin, atan

POLICE_NONE = 'Font/freesansbold.ttf'

NOIR = (0, 0, 0)
GRIS_FONCE = (50, 50, 50)
GRIS_MOYEN = (90, 90, 90)
GRIS_CLAIR = (190, 190, 190)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
VERT = (52, 175, 0)
ROUGE = (255, 0, 0)
ORANGE = (255, 127, 0)
JAUNE = (255, 255, 0)

LARGEUR = 1360
HAUTEUR = 700
PLEIN_ECRAN = False
FPS = 100
CAPTION = 'Scrabble'


def trouve_xy(x: int, y: int, largeur: int, hauteur: int, x_0left_1centre_2right: int, y_0top_1centre_2bottom: int):
    nouveau_x = int(x - largeur * x_0left_1centre_2right / 2)
    nouveau_y = int(y - hauteur * y_0top_1centre_2bottom / 2)
    return nouveau_x, nouveau_y


def point_dans_polygone(x: int, y: int, polygone: list):
    xinters = 0
    n = len(polygone)
    inside = False
    p1x, p1y = polygone[0]
    for i in range(n + 1):
        p2x, p2y = polygone[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


class Ecran:
    def __init__(self, ecran, x: int, y: int, y_0top_1centre_2bottom: int, x_0left_1centre_2right: int):
        self.ecran = ecran
        self.largeur = ecran.get_width()
        self.hauteur = ecran.get_height()
        self.x, self.y = trouve_xy(x, y, self.largeur, self.hauteur, x_0left_1centre_2right, y_0top_1centre_2bottom)

    def affiche(self, screen: pygame.Surface):
        screen.blit(self.ecran, (self.x, self.y))

    def affiche_copy(self, screen: pygame.Surface, x: int, y: int, y_0top_1centre_2bottom=0, x_0left_1centre_2right=0):
        x, y = trouve_xy(x, y, self.largeur, self.hauteur, x_0left_1centre_2right, y_0top_1centre_2bottom)
        screen.blit(self.ecran, (x, y))

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        if self.x - marge_erreur <= x_souris <= self.x + self.largeur + marge_erreur \
                and self.y - marge_erreur <= y_souris <= self.y + self.hauteur + marge_erreur:
            return True
        return False


class Draw(Ecran):
    def __init__(self, draws: list, x: int, y: int, couleurFont=BLANC,
                 y_0top_1centre_2bottom=0, x_0left_1centre_2right=0):
        ecransize = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        ecransize.fill((255, 255, 255, 0))
        ecran = pygame.Surface((LARGEUR, HAUTEUR))
        ecran.fill(couleurFont)
        for draw in draws:
            draw.affiche(ecran)
            draw.affiche(ecransize)
        ecran = ecran.subsurface(ecransize.get_bounding_rect())
        Ecran.__init__(self, ecran, x, y, y_0top_1centre_2bottom, x_0left_1centre_2right)


class Text(Ecran):
    def __init__(self, texte: str, x: int, y: int, taillePolice=30, couleur=NOIR, police=None,
                 x_0left_1centre_2right=0, y_0top_1centre_2bottom=0):
        if police is None:
            police = POLICE_NONE
        font = pygame.font.Font(police, int(taillePolice))
        ecran = font.render(texte, True, couleur)
        Ecran.__init__(self, ecran, x, y, y_0top_1centre_2bottom, x_0left_1centre_2right)


class Image(Ecran):
    def __init__(self, image, x: int, y: int, angleRotation=0, coefRapport=1,
                 y_0top_1centre_2bottom=0, x_0left_1centre_2right=0):
        if angleRotation != 0 or coefRapport != 1:
            image = pygame.transform.rotozoom(image, angleRotation, coefRapport)
        Ecran.__init__(self, image, x, y, y_0top_1centre_2bottom, x_0left_1centre_2right)


class Rectangle:
    def __init__(self, x: int, y: int, largeur: int, hauteur: int, couleur: tuple, pleinOuLargeurContour=0,
                 couleurFont=None, x_0left_1centre_2right=0, y_0top_1centre_2bottom=0):
        self.x, self.y = trouve_xy(x, y, largeur, hauteur, x_0left_1centre_2right, y_0top_1centre_2bottom)
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.width = pleinOuLargeurContour
        self.couleurFont = couleurFont

    def affiche(self, screen: pygame.Surface):
        if self.width == 0:
            pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.largeur, self.hauteur), self.width)
        elif self.couleurFont is None:
            pygame.draw.rect(screen, self.couleur, (self.x, self.y, self.largeur, self.hauteur), self.width)
        else:
            n1 = int(self.width / 2)
            n2 = self.width - n1
            pygame.draw.rect(screen, self.couleur, (self.x - n1, self.y - n1,
                                                    self.largeur + 2 * n1, self.hauteur + 2 * n1), 0)
            pygame.draw.rect(screen, self.couleurFont, (self.x + n2, self.y + n2,
                                                        self.largeur - 2 * n2, self.hauteur - 2 * n2), 0)

    def affiche_copy(self, screen: pygame.Surface, x: int, y: int, y_0top_1centre_2bottom=0, x_0left_1centre_2right=0):
        x, y = trouve_xy(x, y, self.largeur, self.hauteur, x_0left_1centre_2right, y_0top_1centre_2bottom)
        if self.width == 0:
            pygame.draw.rect(screen, self.couleur, (x, y, self.largeur, self.hauteur), self.width)
        elif self.couleurFont is None:
            pygame.draw.rect(screen, self.couleur, (x, y, self.largeur, self.hauteur), self.width)
        else:
            n1 = int(self.width / 2)
            n2 = self.width - n1
            pygame.draw.rect(screen, self.couleur, (x - n1, y - n1, self.largeur + 2 * n1, self.hauteur + 2 * n1), 0)
            pygame.draw.rect(screen, self.couleurFont, (x + n2, y + n2, self.largeur - 2 * n2, self.hauteur - 2 * n2),
                             0)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        if self.x - marge_erreur <= x_souris <= self.x + self.largeur + marge_erreur \
                and self.y - marge_erreur <= y_souris <= self.y + self.hauteur + marge_erreur:
            return True
        return False


class Ligne:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, largeur: int, couleur: tuple):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.largeur = largeur
        self.couleur = couleur

        if largeur > 1:
            if self.x1 == self.x2:
                n = int(self.largeur / 2)
                n2 = self.largeur - n
                self.p1 = (x1 + n, y1)
                self.p2 = (x1 - n2, y1)
                self.p3 = (x2 + n, y2)
                self.p4 = (x2 - n2, y2)

            elif self.y1 == self.y2:
                n = int(self.largeur / 2)
                n2 = self.largeur - n
                self.p1 = (x1, y1 + n)
                self.p2 = (x1, y1 - n2)
                self.p3 = (x2, y2 + n)
                self.p4 = (x2, y2 - n2)

            else:
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                longueur = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                angle = atan((y2 - y1) / (x2 - x1))

                self.p1 = (cx + (longueur / 2) * cos(angle) - (largeur / 2) * sin(angle),
                           cy + (largeur / 2) * cos(angle) + (longueur / 2) * sin(angle))
                self.p2 = (cx - (longueur / 2) * cos(angle) - (largeur / 2) * sin(angle),
                           cy + (largeur / 2) * cos(angle) - (longueur / 2) * sin(angle))
                self.p3 = (cx + (longueur / 2) * cos(angle) + (largeur / 2) * sin(angle),
                           cy - (largeur / 2) * cos(angle) + (longueur / 2) * sin(angle))
                self.p4 = (cx - (longueur / 2) * cos(angle) + (largeur / 2) * sin(angle),
                           cy - (largeur / 2) * cos(angle) - (longueur / 2) * sin(angle))

    def affiche(self, screen: pygame.Surface):
        if self.largeur == 1:
            pygame.gfxdraw.line(screen, self.x1, self.y1, self.x2, self.y2, self.couleur)
        else:
            pygame.gfxdraw.aapolygon(screen, (self.p1, self.p2, self.p4, self.p3), self.couleur)
            pygame.gfxdraw.filled_polygon(screen, (self.p1, self.p2, self.p4, self.p3), self.couleur)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        if marge_erreur == 0:
            if self.largeur > 1:
                return point_dans_polygone(x_souris, y_souris, [self.p1, self.p2, self.p4, self.p3])
            return False
        else:
            cx = (self.x1 + self.x2) / 2
            cy = (self.y1 + self.y2) / 2
            longueur = sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
            angle = atan((self.y2 - self.y1) / (self.x2 - self.x1))
            largeur = self.largeur + marge_erreur
            p1 = (cx + (longueur / 2) * cos(angle) - (largeur / 2) * sin(angle),
                  cy + (largeur / 2) * cos(angle) + (longueur / 2) * sin(angle))
            p2 = (cx - (longueur / 2) * cos(angle) - (largeur / 2) * sin(angle),
                  cy + (largeur / 2) * cos(angle) - (longueur / 2) * sin(angle))
            p3 = (cx + (longueur / 2) * cos(angle) + (largeur / 2) * sin(angle),
                  cy - (largeur / 2) * cos(angle) + (longueur / 2) * sin(angle))
            p4 = (cx - (longueur / 2) * cos(angle) + (largeur / 2) * sin(angle),
                  cy - (largeur / 2) * cos(angle) - (longueur / 2) * sin(angle))
            return point_dans_polygone(x_souris, y_souris, [p1, p2, p4, p3])


class LignesBrisees:
    def __init__(self, points: list, largeur: int, couleur: tuple):
        self.largeur = largeur
        self.listeLignes = [Ligne(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], largeur, couleur)
                            for i in range(len(points) - 1)]
        self.listeCercles = []
        if self.largeur > 3:
            self.listeCercles = [Cercle(x, y, int(largeur / 2), couleur) for x, y in points]

    def affiche(self, screen: pygame.Surface):
        for ligne in self.listeLignes:
            ligne.affiche(screen)
        for cercle in self.listeCercles:
            cercle.affiche(screen)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        for ligne in self.listeLignes:
            if ligne.clic(x_souris, y_souris, marge_erreur):
                return True
        for cercle in self.listeCercles:
            if cercle.clic(x_souris, y_souris, marge_erreur):
                return True


class PolygonePlein:
    def __init__(self, points: list, couleur: tuple, largeurContours=0, couleurContours=NOIR):
        self.points = points
        self.couleur = couleur
        self.contoursAffichage = False
        if largeurContours > 0:
            self.contoursAffichage = True
        pts = points[:]
        pts.append(points[0])
        self.contours = LignesBrisees(pts, largeurContours if self.contoursAffichage else 1, couleurContours)

    def affiche(self, screen: pygame.Surface):
        pygame.gfxdraw.aapolygon(screen, self.points, self.couleur)
        pygame.gfxdraw.filled_polygon(screen, self.points, self.couleur)
        if self.contoursAffichage:
            self.contours.affiche(screen)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        if point_dans_polygone(x_souris, y_souris, self.points):
            return True
        return self.contours.clic(x_souris, y_souris, marge_erreur)


class Cercle:
    def __init__(self, cx, cy, rayon, couleur=NOIR, pleinOuLargeurContour=0, couleurFond=BLANC):
        self.cx = cx
        self.cy = cy
        self.rayon = rayon
        self.couleur = couleur
        self.width = pleinOuLargeurContour
        if self.width > 0:
            self.couleurFont = couleurFond

    def affiche(self, screen: pygame.Surface):
        pygame.gfxdraw.filled_circle(screen, self.cx, self.cy, self.rayon, self.couleur)
        pygame.gfxdraw.aacircle(screen, self.cx, self.cy, self.rayon, self.couleur)
        if self.width > 0:
            pygame.gfxdraw.filled_circle(screen, self.cx, self.cy, self.rayon - self.width, self.couleurFont)
            pygame.gfxdraw.aacircle(screen, self.cx, self.cy, self.rayon - self.width, self.couleurFont)

    def affiche_copy(self, screen: pygame.Surface, cx: int, cy: int):
        pygame.gfxdraw.filled_circle(screen, cx, cy, self.rayon, self.couleur)
        pygame.gfxdraw.aacircle(screen, cx, cy, self.rayon, self.couleur)
        if self.width > 0:
            pygame.gfxdraw.filled_circle(screen, cx, cy, self.rayon - self.width, self.couleurFont)
            pygame.gfxdraw.aacircle(screen, cx, cy, self.rayon - self.width, self.couleurFont)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        if (x_souris - self.cx) ** 2 + (y_souris - self.cy) ** 2 <= (self.rayon + marge_erreur) ** 2:
            return True
        return False


class Bouton:
    def __init__(self, rectangle: Rectangle, objets: list, rectangleSelec: Rectangle, rectangleNonClicabble: Rectangle,
                 clicable: bool, selectionne: bool, selectionClicAuto: bool, parametre=None):
        self.objets = objets
        self.rectangle = rectangle
        self.rectangleSelec = rectangleSelec
        self.rectangleNonClicabble = rectangleNonClicabble
        self.clicable = clicable
        self.selectionne = selectionne
        self.selectionClicAuto = selectionClicAuto
        self.parametre = parametre

    def affiche(self, screen: pygame.Surface):
        if not self.clicable:
            self.rectangleNonClicabble.affiche(screen)
        elif self.selectionne:
            self.rectangleSelec.affiche(screen)
        else:
            self.rectangle.affiche(screen)
        for objet in self.objets:
            objet.affiche(screen)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        if self.clicable and self.rectangle.clic(x_souris, y_souris, marge_erreur):
            if self.selectionClicAuto:
                self.selectionne = not self.selectionne
            return True
        return False


# Le bouton se construit autour d'un ecran :
def bouton_autour_ecran(ecran: Ecran, margeContoursX=10, margeContoursY=10, largeur=None, hauteur=None,
                        couleurFont=GRIS_CLAIR, largeurContours=0, couleurContours=NOIR,
                        couleurFontSelec=GRIS_CLAIR, largeurContoursSelec=3, couleurContoursSelec=NOIR,
                        couleurFontNonClic=GRIS_FONCE, largeurContoursNonClic=0, couleurContoursNonClic=NOIR,
                        selectionClicAuto=False, selectionne=False, clicable=True, parametre=None):
    if largeur is not None:
        margeContoursX = int((largeur - ecran.largeur) / 2)
    if hauteur is not None:
        margeContoursY = int((hauteur - ecran.hauteur) / 2)
    rectangle = Rectangle(ecran.x - margeContoursX, ecran.y - margeContoursY,
                          ecran.largeur + 2 * margeContoursX, ecran.hauteur + 2 * margeContoursY,
                          couleurContours if largeurContours > 0 else couleurFont, largeurContours, couleurFont)
    rectangleSelec = Rectangle(ecran.x - margeContoursX, ecran.y - margeContoursY,
                               ecran.largeur + 2 * margeContoursX, ecran.hauteur + 2 * margeContoursY,
                               couleurContoursSelec if largeurContoursSelec > 0 else couleurFontSelec,
                               largeurContoursSelec, couleurFontSelec)
    rectangleNonClic = Rectangle(ecran.x - margeContoursX, ecran.y - margeContoursY,
                                 ecran.largeur + 2 * margeContoursX, ecran.hauteur + 2 * margeContoursY,
                                 couleurContoursNonClic if largeurContoursNonClic > 0 else couleurFontNonClic,
                                 largeurContoursNonClic, couleurFontNonClic)
    return Bouton(rectangle, [ecran], rectangleSelec, rectangleNonClic,
                  clicable, selectionne, selectionClicAuto, parametre)


# Le bouton se construit où on le demande puis il décale les écransRelatifs de son x (dx) et son y (dy) pour
# qu'ils soient dans le bouton :
def bouton_avec_ecrans(ecransRelatifs: list, x, y, largeur, hauteur, x_0left_1centre_2right=0, y_0top_1centre_2bottom=0,
                       couleurFont=GRIS_CLAIR, largeurContours=0, couleurContours=NOIR,
                       couleurFontSelec=GRIS_CLAIR, largeurContoursSelec=3, couleurContoursSelec=NOIR,
                       couleurFontNonClic=GRIS_FONCE, largeurContoursNonClic=0, couleurContoursNonClic=NOIR,
                       centrerTOUSLesEcrans=False, decallerlesEcranenFonctionDeXEtY=True,
                       selectionClicAuto=False, selectionne=False, clicable=True, parametre=None):
    rectangle = Rectangle(x, y, largeur, hauteur, couleurContours if largeurContours > 0 else couleurFont,
                          largeurContours, couleurFont, x_0left_1centre_2right, y_0top_1centre_2bottom)
    rectangleSelec = Rectangle(x, y, largeur, hauteur, couleurContoursSelec if largeurContoursSelec > 0 else
                               couleurFontSelec, largeurContoursSelec, couleurFontSelec,
                               x_0left_1centre_2right, y_0top_1centre_2bottom)
    rectangleNonClic = Rectangle(x, y, largeur, hauteur, couleurContoursNonClic if largeurContoursNonClic > 0 else
                                 couleurFontNonClic, largeurContoursNonClic, couleurFontNonClic,
                                 x_0left_1centre_2right, y_0top_1centre_2bottom)
    if centrerTOUSLesEcrans:
        cx = x + largeur / 2
        cy = y + hauteur / 2
        for ecran in ecransRelatifs:
            ecran.x = int(cx - ecran.largeur / 2)
            ecran.y += int(cy - ecran.hauteur / 2)
    elif decallerlesEcranenFonctionDeXEtY:
        dx = rectangle.x
        dy = rectangle.y
        for ecran in ecransRelatifs:
            ecran.x += dx
            ecran.y += dy
    return Bouton(rectangle, ecransRelatifs, rectangleSelec, rectangleNonClic,
                  clicable, selectionne, selectionClicAuto, parametre)


class BulleRectanle:
    def __init__(self, x: int, y: int, largeur: int, hauteur: int, positionFleche_0top_1bottom_2left_3right: int,
                 x_0left_1centre_2right=0, y_0top_1centre_2bottom=0, x_ou_y_fleche=None,
                 baseFleche=18, hauteurFleche=14, largeurContours=4, couleurFond=BLANC, couleurContours=NOIR):
        x, y = trouve_xy(x, y, largeur, hauteur, x_0left_1centre_2right, y_0top_1centre_2bottom)
        baseFlecheSurDeux = int(baseFleche / 2)
        pts = [(x, y), (x + largeur, y), (x + largeur, y + hauteur), (x, y + hauteur)]
        if x_ou_y_fleche is None:
            x_ou_y_fleche = int(x + largeur / 2)
        if positionFleche_0top_1bottom_2left_3right == 0:
            p1 = pts[0]
            p2 = (x_ou_y_fleche - baseFlecheSurDeux, y)
            p3 = (x_ou_y_fleche, y - hauteurFleche)
            p4 = (x_ou_y_fleche + baseFlecheSurDeux, y)
            p5 = pts[1]
            p6 = pts[2]
            p7 = pts[3]
        elif positionFleche_0top_1bottom_2left_3right == 1:
            p1 = pts[0]
            p2 = pts[1]
            p3 = pts[2]
            p4 = (x_ou_y_fleche + baseFlecheSurDeux, y + hauteur)
            p5 = (x_ou_y_fleche, y + hauteur + hauteurFleche)
            p6 = (x_ou_y_fleche - baseFlecheSurDeux, y + hauteur)
            p7 = pts[3]
        elif positionFleche_0top_1bottom_2left_3right == 2:
            p1 = pts[0]
            p2 = pts[1]
            p3 = pts[2]
            p4 = pts[3]
            p5 = (x, x_ou_y_fleche + baseFlecheSurDeux)
            p6 = (x - hauteurFleche, x_ou_y_fleche)
            p7 = (x, x_ou_y_fleche - baseFlecheSurDeux)
        else:
            p1 = pts[0]
            p2 = pts[1]
            p3 = (x + largeur, x_ou_y_fleche - baseFlecheSurDeux)
            p4 = (x + largeur + hauteurFleche, x_ou_y_fleche)
            p5 = (x + largeur, x_ou_y_fleche + baseFlecheSurDeux)
            p6 = pts[2]
            p7 = pts[3]
        self.polygone = PolygonePlein([p1, p2, p3, p4, p5, p6, p7], couleurFond, largeurContours, couleurContours)

    def affiche(self, screen: pygame.Surface):
        self.polygone.affiche(screen)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        return self.polygone.clic(x_souris, y_souris, marge_erreur)


class BarreTexte:
    def __init__(self, rectangle: Rectangle, rectangleNonSelect: Rectangle=None, couleurNonSelect=GRIS_CLAIR,
                 tailleTexte=30, couleurTexte=NOIR, texte_x_0left_1centre_2right=0, margesBords=10, selectionne=True,
                 selectionneAuto=False, texteDepart='', nbCaracteresMax=25, texteSupAutoSiValider=True):
        self.rectangle = rectangle
        self.rectangleNonSelect = rectangleNonSelect
        if rectangleNonSelect is None:
            self.rectangleNonSelect = Rectangle(rectangle.x, rectangle.y, rectangle.largeur, rectangle.hauteur,
                                                couleurNonSelect, rectangle.width, rectangle.couleurFont)
        self.tailleTexte = tailleTexte
        self.couleurTexte = couleurTexte
        self.texte_x_0left_1centre_2right = texte_x_0left_1centre_2right
        self.selectionne = selectionne
        self.selectionneAuto = selectionneAuto
        self.texteSupAutoSiValider = texteSupAutoSiValider
        self.strTexte = texteDepart
        self.nbCaracteresMax = nbCaracteresMax
        if texte_x_0left_1centre_2right == 0:
            self.x = rectangle.x + margesBords
        elif texte_x_0left_1centre_2right == 1:
            self.x = int(rectangle.x + rectangle.largeur / 2)
        else:
            self.x = rectangle.x + rectangle.largeur - margesBords
        self.y = int(rectangle.y + rectangle.hauteur / 2)
        self.texte = Text('', 0, 0)
        self.update_texte()

    def update_texte(self):
        self.texte = Text(self.strTexte, self.x, self.y, self.tailleTexte, self.couleurTexte,
                          x_0left_1centre_2right=self.texte_x_0left_1centre_2right, y_0top_1centre_2bottom=1)

    def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
        if self.rectangle.clic(x_souris, y_souris, marge_erreur):
            if self.selectionneAuto:
                self.selectionne = True
            return True
        else:
            if self.selectionneAuto:
                self.selectionne = False
            return False

    def affiche(self, screen: pygame.Surface):
        if self.selectionne:
            self.rectangle.affiche(screen)
        else:
            self.rectangleNonSelect.affiche(screen)
        self.texte.affiche(screen)

    def valider(self):
        if self.strTexte != '':
            r = self.strTexte
            if self.texteSupAutoSiValider:
                self.strTexte = ''
                self.update_texte()
            return r
        return None

    def gere_clavier(self, keyEvent: pygame.event):
        if self.selectionne:
            if keyEvent.key == pygame.K_RETURN or keyEvent.key == 271:
                return self.valider()
            elif keyEvent.key == pygame.K_BACKSPACE:
                self.strTexte = self.strTexte[:-1]
                self.update_texte()
            else:
                if len(self.strTexte) < self.nbCaracteresMax:
                    self.strTexte += keyEvent.unicode
                    self.update_texte()
        return None


# class BoutonInfoBulle:
#     def __init__(self, bouton: Bouton, bulleRectangle: BulleRectanle, contenuFixe=None, contenuModofiable=None):
#         self.bouton = bouton
#         self.bouton.selectionClicAuto = True
#         self.bulleRectangle = bulleRectangle
#         self.contenuFixe = []
#         if contenuFixe is not None:
#             self.contenuFixe = contenuFixe
#         self.contenuModofiable = []
#         if contenuModofiable is not None:
#             self.contenuModofiable = contenuModofiable
#
#     def affiche(self, screen: pygame.Surface):
#         self.bouton.affiche(screen)
#         if self.bouton.selectionne:
#             self.bulleRectangle.affiche(screen)
#             for objet in self.contenuFixe + self.contenuModofiable:
#                 objet.affiche(screen)
#
#     def clic(self, x_souris: int, y_souris: int, marge_erreur=0):
#         if self.bouton.selectionne:
#             for objet in self.contenuFixe + self.contenuModofiable:
#                 if objet.clic(x_souris, y_souris, marge_erreur):
#                     return objet
#         return self.bouton.clic(x_souris, y_souris, marge_erreur)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(CAPTION)
    if PLEIN_ECRAN:
        mainScreen = pygame.display.set_mode((LARGEUR, HAUTEUR), FULLSCREEN)
    else:
        mainScreen = pygame.display.set_mode((LARGEUR, HAUTEUR))

    # On prépare les objets que l'on veut afficher ...

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        mainScreen.fill(BLANC)

        # On affiche les objets que l'on a préparé ...

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
