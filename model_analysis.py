
import pickle
import matplotlib.pyplot as plt
import numpy as np

with open("moves_per_game_1587683302.140041", "rb") as file:
    game_scores = pickle.load(file)

print(np.mean(game_scores))
print(max(game_scores))

x = np.array([game_number for game_number in range(len(game_scores))])
y = np.array(game_scores)
plt.scatter(x, y)

m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.xlabel("parties")
plt.ylabel("nombre de déplacements")
plt.show()
