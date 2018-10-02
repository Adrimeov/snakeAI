import pygame


class Cube:
    def __init__(self, cube=None, premier=False):
        self._color = (0, 128, 255)

        self._directionX = False
        self._deplacementPositif = False
        if premier:
            self.x = 30
            self.y = 30
        else:
            self.cube = cube
            self.x = self.cube.ancienX
            self.y = self.cube.ancienY
            self.fils = 0
            cube.ajouterFils(self)

        self.ancienX = 0
        self.ancienY = 0

    def deplacementPere(self, nouveauX, nouveauY):
        self.ancienX = self.x
        self.ancienY = self.y
        self.x = nouveauX
        self.y = nouveauY
        self.fils.deplacementFils()

    def deplacementFils(self):
            self.ancienX = self.x
            self.ancienY = self.y
            self.x = self.cube.ancienX
            self.y = self.cube.ancienY
            try:
                self.fils.deplacementFils()
            except:
                return 0

    def ajouterFils(self, cube):
        self.fils = cube

    def color(self):
        return self._color

    def setDirectionSinge(self):
        difX = self.x - self.ancienX
        difY = self.y - self.ancienY

        if difX < 0:
            self._directionX = True
            self._deplacementPositif = False
        elif difX > 0:
            self._directionX = True
            self._deplacementPositif = True
        elif difY < 0:
            self._directionX = False
            self._deplacementPositif = False
        elif difY > 0:
            self._directionX = False
            self._deplacementPositif = True

    def verifX(self, positif=True):
        if positif:
            if self._directionX and not self._deplacementPositif:
                return False
        elif not positif:
            if self._directionX and self._deplacementPositif:
                return False
        return True

    def verifY(self, positif=True):
        if positif:
            if not self._directionX and not self._deplacementPositif:
                return False
        elif not positif:
            if not self._directionX and self._deplacementPositif:
                return False
        return True




