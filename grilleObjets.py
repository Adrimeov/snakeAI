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
        return index in self.dictioPosition
