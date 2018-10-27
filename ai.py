from network import Network
import cube
import grilleObjets
import pygame
import numpy as np

class ai:
    def __init__(self, nbrInput, nbrMilieu, nbrOutput):
        self.network = Network(nbrInput, nbrMilieu, nbrOutput)
        self.performance = 0
        self.longueurParDefaut = 5
        self.step = 10
        self.cubePere = 0
        self.cubePere = cube.Cube(premier=True)
        self.cubes = [self.cubePere]
        self.creationDuVers()
        self.positionsValides = grilleObjets.grilleObjets(400, self.step)
        self.positionBouffe = self.positionsValides.genererNouveauPoint()
        self.cubesParFood = 10


    def __lt__(self, other):
        try:
            return self.performance < other.performance
        except AttributeError:
            print("Impossible de comparer !")

    def creationDuVers(self):
        # self.cubes.append(self.cubePere)
        for i in range(self.longueurParDefaut):
            self.cubes.append(self.cubePere.ajouterFils())

    def afficher(self, screen):
        for morceau in self.cubes:
            pygame.draw.rect(screen, morceau.color(), pygame.Rect(morceau.x, morceau.y, 9, 9))
        pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(self.positionBouffe[0], self.positionBouffe[1], 9, 9))

    def fitness(self):
        self.performance += 1


    def networkInput(self):

        x = self.cubePere.x
        y = self.cubePere.y
        step = self.step
        directionActuelle = self.cubePere.getDirection()

        if directionActuelle == "DROITE":
            bouffeEstAGauche = int(self.positionBouffe[1] < y)
            bouffeEstADroite = int(self.positionBouffe[1] > y)
            bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
            libreAGauche = int(self.positionsValides.estDansGrille((x, y - step)))
            libreADroite = int(self.positionsValides.estDansGrille((x, y + step)))
            libreEnAvant = int(self.positionsValides.estDansGrille((x + step, y)))

        if directionActuelle == "GAUCHE":
            bouffeEstAGauche = int(self.positionBouffe[1] > y)
            bouffeEstADroite = int(self.positionBouffe[1] < y)
            bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
            libreAGauche = int(self.positionsValides.estDansGrille((x, y + step)))
            libreADroite = int(self.positionsValides.estDansGrille((x, y - step)))
            libreEnAvant = int(self.positionsValides.estDansGrille((x - step, y)))

        if directionActuelle == "HAUT":
            bouffeEstAGauche = int(self.positionBouffe[0] < x)
            bouffeEstADroite = int(self.positionBouffe[0] > x)
            bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
            libreAGauche = int(self.positionsValides.estDansGrille((x - step, y)))
            libreADroite = int(self.positionsValides.estDansGrille((x + step, y)))
            libreEnAvant = int(self.positionsValides.estDansGrille((x, y - step)))

        if directionActuelle == "BAS":
            bouffeEstAGauche = int(self.positionBouffe[0] > x)
            bouffeEstADroite = int(self.positionBouffe[0] < x)
            bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
            libreAGauche = int(self.positionsValides.estDansGrille((x + step, y)))
            libreADroite = int(self.positionsValides.estDansGrille((x - step, y)))
            libreEnAvant = int(self.positionsValides.estDansGrille((x, y + step)))

        return np.array([bouffeDroitDevant,
                         bouffeEstADroite,
                         bouffeEstAGauche,
                         libreEnAvant,
                         libreADroite,
                         libreAGauche])

    def prochainDeplacementVers(self):
        self.network.feed_forward(self.networkInput())
        decision = self.network.decider()
        if decision == 0:
            self.cubePere.tounerGauche()

        if decision == 2:
            self.cubePere.tournerDroite()

    def deplacementVers(self):
        self.cubePere.deplacementPere()
        reponse = self.cubePere.updateGoodPositions(self.positionsValides)

        if reponse[0]:
            del self.cubes[:]
            return 0
        if reponse[1]:
            self.performance += 100
            self.positionBouffe = self.positionsValides.genererNouveauPoint()
            self.positionsValides.miseAJourIndex(self.positionBouffe, True)
            for i in range(self.cubesParFood):
                self.cubes.append(self.cubePere.ajouterFils())

        self.performance += 1

        return 1

    def AIaction(self, screen):
        self.afficher(screen)
        self.networkInput()
        self.prochainDeplacementVers()
        return self.deplacementVers()

    def reset(self):
        self.performance = 0
        self.cubePere = cube.Cube(premier=True)
        self.cubes = [self.cubePere]
        self.creationDuVers()




