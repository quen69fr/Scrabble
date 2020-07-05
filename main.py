# coding: utf-8

from controller import *
from view import *


if __name__ == "__main__":
    partie = Partie()
    view = View(partie)
    controller = Controller(partie, view)

    while True:
        controller.run()
        view.affiche()




