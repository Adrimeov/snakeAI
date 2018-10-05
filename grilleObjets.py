import random

class grilleObjets:
    def __init__(self, taille, step):
        self.dictioPosition = {}
        self.taille = taille
        self.step = step
        self.genererDictionnaire()

    def genererDictionnaire(self):
        nbCase = int(self.taille/self.step)
        for i in range(nbCase):
            for j in range(nbCase):
                index = (i*self.step, j*self.step)
                self.dictioPosition[index] = False

    def miseAJourIndex(self, index, etat= False):
            self.dictioPosition[index] = etat

    def suprimmerIndex(self, index):
        return self.dictioPosition.pop(index, -1)

    def genererNouveauPoint(self):
        return random.choice(list(self.dictioPosition.keys()))

    def estDansGrille(self, index):
        try:
            ok = self.dictioPosition[index]
            return True
        except:
            return False

    def collisionADroite(self, index):
        for i in range(index[0] + self.step, self.taille - self.step + 1, self.step):
            if not self.estDansGrille((i, index[1])):
                return True
        return False

    def collisionAGauche(self, index):
        for i in range(index[0] - self.step, 0, -self.step):
            if not self.estDansGrille((i, index[1])):
                return True
        return False

    def collisionEnHaut(self, index):
        for i in range(index[1] - self.step, 0, -self.step):
            if not self.estDansGrille((index[0], i)):
                return True
        return False

    def collisionEnBas(self, index):
        for i in range(index[1] + self.step, self.taille - self.step + 1, self.step):
            if not self.estDansGrille((index[0], i)):
                return True
        return False