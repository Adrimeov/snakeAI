import pygame
import cube as cb
import grilleObjets
import utils
import pickle
import time

from random import randint, random
from agent import Agent

maxX = 190
maxY = 190
scoreParMiam = 1
step = 10
epochs = 200
manual = True
pygame.init()
textFont = pygame.font.SysFont("monospace", 15)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((200, 200))

start_time = time.time()
game_scores = []
moves_per_game = []
MAXIMUM_MOVES = 3000

tick = 20
fps = tick / 4
ctrFps = 0
cubesParFood = 1

epsilon_decay = 1 / 100
date = time.time()

agent = Agent()

for i in range(epochs):
    done = 0
    scoreTotal = 0
    moves_counter = 0

    cubePere = cb.Cube(premier=True)
    cubes = [cubePere]
    for j in range(1):
        cubes.append(cubePere.ajouterFils())
    positionsValides = grilleObjets.grilleObjets(200, step)
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

        old_state, debug_1 = utils.return_state(directionActuelle, positionBouffe, x, y, positionsValides, step)
        epsilon = 1 - i * epsilon_decay

        if random() < max(epsilon, 0.01):
            action = randint(0, 2)
        else:
            action = agent.predict_move(old_state).item()

        new_direction = utils.prediction_to_direction(utils.direction_from_string_to_bool(directionActuelle), action)

        cubePere.setDirectionSigne(new_direction[0], new_direction[1])
        cubePere.deplacementPere()
        moves_counter += 1

        reponse = cubePere.updateGoodPositions(positionsValides)
        done = reponse[0]
        if moves_counter > MAXIMUM_MOVES:
            done = True
        reward = reponse[1]
        directionActuelle = cubePere.getDirection()
        x = cubePere.x
        y = cubePere.y
        new_state, debug_2 = utils.return_state(directionActuelle, positionBouffe, x, y, positionsValides, step)
        if reponse[1]:
            scoreTotal += scoreParMiam
            positionBouffe = positionsValides.genererNouveauPoint()
            for j in range(cubesParFood):
                cubes.append(cubePere.ajouterFils())
        positionsValides.miseAJourIndex(positionBouffe, True)

        reward = agent.set_reward(reward, done)
        loss = agent.train_step(old_state, action, new_state, reward, done)
        agent.save_state(old_state, action, new_state, reward, done)

        for cube in cubes:
            pygame.draw.rect(screen, cube.color(), pygame.Rect(cube.x, cube.y, 9, 9))
        pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(positionBouffe[0], positionBouffe[1], 9, 9))
        pygame.display.flip()
        screen.fill((0, 0, 0))
        # clock.tick(tick)

    game_scores.append(scoreTotal)
    moves_per_game.append(moves_counter)

    print(f"game #{i} score: {scoreTotal} moves: {moves_counter}")
    with open(f"game_scores_{date}", "wb") as file:
        pickle.dump(game_scores, file)
    with open(f"moves_per_game_{date}", "wb") as file:
        pickle.dump(moves_per_game, file)
    agent.save_model()


end_time = time.time()
print(f"training duration: {time.strftime('%M:%S', time.localtime(end_time - start_time))}")
