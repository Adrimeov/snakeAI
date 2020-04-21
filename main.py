import pygame
import cube as cb
import grilleObjets
import numpy
import utils


maxX = 390
maxY = 390
scoreParMiam = 10
scoreTotal = 0
step = 10
epochs = 10
manual = True
pygame.init()
textFont = pygame.font.SysFont("monospace", 15)
muck_predict = utils.muck_agent()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))


tick = 5
fps = tick / 4
ctrFps = 0
cubesParFood = 1


for i in range(epochs):
    done = 0
    cubePere = cb.Cube(premier=True)
    cubes = [cubePere]
    for i in range(1):
        cubes.append(cubePere.ajouterFils())
    positionsValides = grilleObjets.grilleObjets(400, step)
    positionBouffe = positionsValides.genererNouveauPoint()
    positionsValides.miseAJourIndex(positionBouffe, True)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = 1

        directionActuelle = cubePere.getDirection()

        x = cubePere.x
        y = cubePere.y


        utils.manual_mode(cubePere)
        old_state = utils.return_state(directionActuelle, positionBouffe, x, y, positionsValides, step)
        # predictions = next(muck_predict)
        # action = utils.translate_direction_from_bool(predictions)
        # cubePere.setDirectionSigne(predictions[0], predictions[1])
        cubePere.deplacementPere()
        # new_state = utils.return_state(directionActuelle, positionBouffe, x, y, positionsValides, step)

        reponse = cubePere.updateGoodPositions(positionsValides)
        done = reponse[0]
        reward = reponse[1]
        if reponse[1]:
            scoreTotal += scoreParMiam
            positionBouffe = positionsValides.genererNouveauPoint()
            positionsValides.miseAJourIndex(positionBouffe, True)
            for i in range(cubesParFood):
                cubes.append(cubePere.ajouterFils())

        for cube in cubes:
            pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))
        pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(positionBouffe[0], positionBouffe[1], 9, 9))
        pygame.display.flip()
        screen.fill((0, 0, 0))

        ctrFps += fps
        clock.tick(tick)
