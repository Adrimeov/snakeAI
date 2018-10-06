import pygame
import cube
import grilleObjets
import numpy

maxX = 390
maxY = 390
scoreParMiam = 10
scoreTotal = 0
step = 10

pygame.init()
textFont = pygame.font.SysFont("monospace", 15)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
done = 0

cubePere = cube.Cube(premier=True)
cubes = [cubePere]
cubesParFood = 10

positionsValides = grilleObjets.grilleObjets(400, step)
positionBouffe = positionsValides.genererNouveauPoint()
positionsValides.miseAJourIndex(positionBouffe, True)

tick = 5
fps = tick / 4
ctrFps = 0

for i in range(10):
    cubes.append(cubePere.ajouterFils())

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = 1

    directionActuelle = cubePere.getDirection()

    x = cubePere.x
    y = cubePere.y

    if directionActuelle == "DROITE":
        bouffeEstAGauche = int(positionBouffe[1] < y)
        bouffeEstADroite = int(positionBouffe[1] > y)
        bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
        libreAGauche = int(positionsValides.estDansGrille((x, y - step)))
        libreADroite = int(positionsValides.estDansGrille((x, y + step)))
        libreEnAvant = int(positionsValides.estDansGrille((x + step, y)))

    if directionActuelle == "GAUCHE":
        bouffeEstAGauche = int(positionBouffe[1] > y)
        bouffeEstADroite = int(positionBouffe[1] < y)
        bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
        libreAGauche = int(positionsValides.estDansGrille((x, y + step)))
        libreADroite = int(positionsValides.estDansGrille((x, y - step)))
        libreEnAvant = int(positionsValides.estDansGrille((x - step, y)))

    if directionActuelle == "HAUT":
        bouffeEstAGauche = int(positionBouffe[0] < x)
        bouffeEstADroite = int(positionBouffe[0] > x)
        bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
        libreAGauche = int(positionsValides.estDansGrille((x - step, y)))
        libreADroite = int(positionsValides.estDansGrille((x + step, y)))
        libreEnAvant = int(positionsValides.estDansGrille((x, y - step)))

    if directionActuelle == "BAS":
        bouffeEstAGauche = int(positionBouffe[0] > x)
        bouffeEstADroite = int(positionBouffe[0] < x)
        bouffeDroitDevant = int(not bouffeEstADroite and not bouffeEstAGauche)
        libreAGauche = int(positionsValides.estDansGrille((x + step, y)))
        libreADroite = int(positionsValides.estDansGrille((x - step, y)))
        libreEnAvant = int(positionsValides.estDansGrille((x, y + step)))

    inputs = numpy.array([
        bouffeDroitDevant,
        bouffeEstADroite,
        bouffeEstAGauche,
        libreEnAvant,
        libreADroite,
        libreAGauche
    ])

    print(inputs)

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and cubePere.verifY(positif=False):
        cubePere.setDirectionSinge(False, False)

    elif pressed[pygame.K_DOWN] and cubePere.verifY():
        cubePere.setDirectionSinge(False, True)

    elif pressed[pygame.K_RIGHT] and cubePere.verifX():
        cubePere.setDirectionSinge(True, True)

    elif pressed[pygame.K_LEFT] and cubePere.verifX(positif=False):
        cubePere.setDirectionSinge(True, False)

    screen.fill((0, 0, 0))
    scoretext = "SCORE: " + scoreTotal.__str__()
    label = textFont.render(scoretext, 1, (255, 255, 255))
    screen.blit(label, (0, 0))
    for cube in cubes:
        pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))
    pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(positionBouffe[0], positionBouffe[1], 9, 9))
    pygame.display.flip()
    cubePere.deplacementPere()

    reponse = cubePere.updateGoodPositions(positionsValides)
    done = reponse[0]

    if reponse[1]:
        scoreTotal += scoreParMiam
        print(scoreTotal)
        positionBouffe = positionsValides.genererNouveauPoint()
        positionsValides.miseAJourIndex(positionBouffe, True)
        for i in range(cubesParFood):
            cubes.append(cubePere.ajouterFils())

    ctrFps += fps
    clock.tick(tick)
