import pygame
import ai
import pickle

def main():

    maxX = 390
    maxY = 390
    scoreParMiam = 10
    scoreTotal = 0
    step = 10
    cubesParFood = 10
    done = 0
    tick = 20
    fps = tick / 4
    ctrFps = 0
    compteur = 0
    fileName = "AISave"

    lastAI = 0
    with open(fileName, "rb") as f:
        lastAI = pickle.load(f)

    nbBestAI = len(lastAI)
    ai1 = []
    for i in range(nbBestAI):
        ai1 += lastAI[i] * 10

    for ai in ai1:
        ai.mutation()

    print(len(ai1))

    pygame.init()
    textFont = pygame.font.SysFont("monospace", 15)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((400, 400))
    # ai1 = []
    # for i in range(100):
    #     ai1.append(ai.ai(6, 6, 3))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = 1

        screen.fill((0, 0, 0))
        scoretext = "SCORE: " + scoreTotal.__str__()
        label = textFont.render(scoretext, 1, (255, 255, 255))
        screen.blit(label, (0, 0))

        for i in ai1:
            try:
                if not i.AIaction(screen):
                    del i
            except:
                pass

        pygame.display.flip()
        ctrFps += fps
        clock.tick(tick)
        compteur += 1

        if compteur >= 50:
            done = True

    ai1 = sorted(ai1)
    tableauScore = []
    for i in ai1:
        tableauScore.append(i.performance)
        i.reset()

    bestAis = ai1[-10:]

    fileName = "AISave"
    with open(fileName, 'wb') as file:
        pickle.dump(bestAis, file)




    print(tableauScore)





