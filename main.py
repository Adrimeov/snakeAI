import pygame
import cube

maxX = 390
maxY = 290
step = 5

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 300))
done = 0
a = 0
# x = 30
# y = 30
cubePere = cube.Cube(premier=True)
cubeFils = cube.Cube(cubePere)
cubes = [cubePere, cubeFils]
for i in range(20):
    cubeParent = cubes[-1]
    cubes.append(cube.Cube(cubeParent))




while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = 1

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and cubePere.verifY(positif=False):
        y = max(0, (cubePere.y-step))
        cubePere.deplacementPere(cubePere.x, y)
        cubePere.setDirectionSinge()

    elif pressed[pygame.K_DOWN] and cubePere.verifY():
        y = min(maxY, (cubePere.y+step))
        cubePere.deplacementPere(cubePere.x, y)
        cubePere.setDirectionSinge()

    elif pressed[pygame.K_RIGHT] and cubePere.verifX():
        x = min(maxX, (cubePere.x+step))
        cubePere.deplacementPere(x, cubePere.y)
        cubePere.setDirectionSinge()

    elif pressed[pygame.K_LEFT] and cubePere.verifX(positif=False):
        x = max(0, (cubePere.x-step))
        cubePere.deplacementPere(x, cubePere.y)
        cubePere.setDirectionSinge()

    if pressed[pygame.K_0]: print("OK")

    screen.fill((0, 0, 0))

    for cube in cubes:
        pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 10, 10))

    pygame.display.flip()
    clock.tick(60)


