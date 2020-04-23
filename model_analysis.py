
import pickle
import matplotlib.pyplot as plt
import numpy as np

with open("game_scores_41", "rb") as file:
    game_scores = pickle.load(file)

x = np.array([game_number for game_number in range(len(game_scores))])
y = np.array(game_scores)
plt.scatter(x, y)

m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.xlabel("parties")
plt.ylabel("points")
plt.show()
