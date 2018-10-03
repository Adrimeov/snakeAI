import pygame
import cube
import grilleObjets

maxX = 390
maxY = 390
step = 4
scoreParMiam = 10
scoreTotal = 0
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
done = 0

cubePere = cube.Cube(premier=True)
cubes = [cubePere]
cubesParFood = 10

positionsValides = grilleObjets.grilleObjets(400, 10)
position = positionsValides.genererNouveauPoint()
positionsValides.miseAJourIndex(position, True)

tick = 60
fps = tick / 4
ctrFps = 0

for i in range(10):
    cubes.append(cubePere.ajouterFils())

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = 1

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and cubePere.verifY(positif=False):
        cubePere.setDirectionSinge(False, False)

    elif pressed[pygame.K_DOWN] and cubePere.verifY():
        cubePere.setDirectionSinge(False, True)

    elif pressed[pygame.K_RIGHT] and cubePere.verifX():
        cubePere.setDirectionSinge(True, True)

    elif pressed[pygame.K_LEFT] and cubePere.verifX(positif=False):
        cubePere.setDirectionSinge(True, False)

    if ctrFps % tick == 0:
        screen.fill((0, 0, 0))
        for cube in cubes:
            pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))
        pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(position[0], position[1], 9, 9))
        pygame.display.flip()
        cubePere.deplacementPere()

        reponse = cubePere.updateGoodPositions(positionsValides)
        done = reponse[0]

        if reponse[1]:
            scoreTotal += scoreParMiam
            print(scoreTotal)
            position = positionsValides.genererNouveauPoint()
            positionsValides.miseAJourIndex(position, True)
            for i in range(cubesParFood):
                cubes.append(cubePere.ajouterFils())

    ctrFps += fps
    clock.tick(tick)
