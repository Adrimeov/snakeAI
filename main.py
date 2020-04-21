import pygame
import cube as cb
import grilleObjets
import numpy
import utils

from random import randint, random
from agent import Agent

maxX = 390
maxY = 390
scoreParMiam = 10
scoreTotal = 0
step = 10
epochs = 1000
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

epsilon_decay = 1/50

agent = Agent()


for i in range(epochs):
    done = 0
    cubePere = cb.Cube(premier=True)
    cubes = [cubePere]
    for j in range(4):
        cubes.append(cubePere.ajouterFils())
    positionsValides = grilleObjets.grilleObjets(400, step)
    positionBouffe = positionsValides.genererNouveauPoint()
    positionsValides.miseAJourIndex(positionBouffe, True)

    agent.replay_memory(100)
    loss = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = 1

        directionActuelle = cubePere.getDirection()

        x = cubePere.x
        y = cubePere.y

        # utils.manual_mode(cubePere)

        old_state, debug_1 = utils.return_state(directionActuelle, positionBouffe, x, y, positionsValides, step)
        epsilon = 1 - i * epsilon_decay

        if random() < .1:
            action = randint(0, 2)
        else:
            action = agent.predict_move(old_state).item()

        new_direction = utils.prediction_to_direction(utils.direction_from_string_to_bool(directionActuelle), action)

        cubePere.setDirectionSigne(new_direction[0], new_direction[1])
        cubePere.deplacementPere()

        reponse = cubePere.updateGoodPositions(positionsValides)
        done = reponse[0]
        reward = reponse[1]
        directionActuelle = cubePere.getDirection()
        x = cubePere.x
        y = cubePere.y
        new_state, debug_2 = utils.return_state(directionActuelle, positionBouffe, x, y, positionsValides, step)
        if reponse[1]:
            scoreTotal += scoreParMiam
            positionBouffe = positionsValides.genererNouveauPoint()
            positionsValides.miseAJourIndex(positionBouffe, True)
            for i in range(cubesParFood):
                cubes.append(cubePere.ajouterFils())

        reward = agent.set_reward(reward, done)
        loss = agent.train_step(old_state, action, new_state, reward, done)
        agent.save_state(old_state, action, new_state, reward, done)

        for cube in cubes:
            pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))
        pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(positionBouffe[0], positionBouffe[1], 9, 9))
        pygame.display.flip()
        screen.fill((0, 0, 0))

        # clock.tick(tick)

    print(f"game #{i} loss: {loss} epsilon: {epsilon}")
