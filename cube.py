maxX = 390
maxY = 390


class Cube:
    def __init__(self, cube=None, premier=False):
        self._color = (0, 128, 255)

        self._directionX = True
        self._deplacementPositif = True
        if premier:
            self.x = 30
            self.y = 30
            self.fils = 0
            self.ancienX = self.x
            self.ancienY = self.y
        else:
            self.cube = cube
            self.x = self.cube.ancienX
            self.y = self.cube.ancienY
            self.fils = 0
            self.ancienX = self.x
            self.ancienY = self.y

    def deplacementPere(self):
        self.ancienX = self.x
        self.ancienY = self.y
        step = -10

        if self._deplacementPositif:
            step = 10

        if self._directionX:
            if self.x + step <= maxX and self.x + step >= 0:
                self.x += step
        else:
            if self.y + step <= maxY and self.y + step >= 0:
                self.y += step

        # pour empecher les cubes fils de rentrer dans le mur
        if self.ancienX != self.x or self.ancienY != self.y:
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

    def ajouterFils(self):
        if self.fils != 0:
            return self.fils.ajouterFils()

        self.fils = Cube(self)
        return self.fils

    def color(self):
        return self._color

    def setDirectionSinge(self, directionX=True, estPositif=True):

        self._directionX = directionX
        self._deplacementPositif = estPositif

    def updateGoodPositions(self, positionArray):
        position = (self.x, self.y)
        isFood = positionArray.suprimmerIndex(position)
        if isFood == -1:
            print("Collision")
            return (1, False)
        self.updateGoodPositionsFils(positionArray)
        return (0, isFood)

    def updateGoodPositionsFils(self, positionArray):
        if self.fils != 0:
            self.fils.updateGoodPositionsFils(positionArray)
            return
        position = (self.ancienX, self.ancienY)
        positionArray.miseAJourIndex(position, False)

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




