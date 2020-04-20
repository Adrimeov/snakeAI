import pygame
import cube
import grilleObjets
import numpy


maxX = 390
maxY = 390
scoreParMiam = 10
scoreTotal = 0
step = 10
manual = True
pygame.init()
textFont = pygame.font.SysFont("monospace", 15)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
done = 0

cubePere = cube.Cube(premier=True)
cubes = [cubePere]
cubesParFood = 1

positionsValides = grilleObjets.grilleObjets(400, step)
positionBouffe = positionsValides.genererNouveauPoint()
positionsValides.miseAJourIndex(positionBouffe, True)

tick = 10
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

    bouffeEstAGauche = 0
    bouffeEstADroite = 0
    bouffeDroitDevant = 0
    libreAGauche = 0
    libreEnAvant = 0

    manual_mode(cubePere)
    cubePere.deplacementPere()
    for cube in cubes:
        pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))
    pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(positionBouffe[0], positionBouffe[1], 9, 9))
    pygame.display.flip()

    inputs = numpy.array([
        bouffeDroitDevant,
        bouffeEstADroite,
        bouffeEstAGauche,
        libreEnAvant,
        libreADroite,
        libreAGauche
    ])


    screen.fill((0, 0, 0))
    # scoretext = "SCORE: " + scoreTotal.__str__()
    # label = textFont.render(scoretext, 1, (255, 255, 255))
    # screen.blit(label, (0, 0))
    # for cube in cubes:
    #     pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))
    # pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(positionBouffe[0], positionBouffe[1], 9, 9))
    # pygame.display.flip()


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
