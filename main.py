import pygame
import cube
import grilleObjets

maxX = 390
maxY = 390
step = 4

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 400))
done = 0
a = 0
# x = 30
# y = 30
cubePere = cube.Cube(premier=True)
cubeFils = cube.Cube(cubePere)
cubes = [cubePere, cubeFils]
positionsValides = grilleObjets.grilleObjets(400, 10)
for i in range(10):
    cubeParent = cubes[-1]
    cubes.append(cube.Cube(cubeParent))

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

    if pressed[pygame.K_0]: print("OK")

    screen.fill((0, 0, 0))
    cubePere.deplacementPere()
    done = cubePere.updateGoodPositions(positionsValides)

    for cube in cubes:
        pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))

    pygame.display.flip()
    clock.tick(15)


