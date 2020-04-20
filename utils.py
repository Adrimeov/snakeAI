import pygame


def manual_mode(cube_pere):
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and cube_pere.verifY(positif=False):
        cube_pere.setDirectionSigne(False, False)

    elif pressed[pygame.K_DOWN] and cube_pere.verifY():
        cube_pere.setDirectionSigne(False, True)

    elif pressed[pygame.K_RIGHT] and cube_pere.verifX():
        cube_pere.setDirectionSigne(True, True)

    elif pressed[pygame.K_LEFT] and cube_pere.verifX(positif=False):
        cube_pere.setDirectionSigne(True, False)


def return_state(direction_actuelle, position_bouffe, x, y, positions_valides):
    bouffe_est_a_gauche = 0
    bouffe_est_a_droite = 0
    bouffe_devant = 0
    libre_a_gauche = 0
    libre_a_droite = 0
    libre_en_avant = 0
    haut = 0
    bas = 0
    droite = 0
    gauche = 0

    if direction_actuelle == "DROITE":
        bouffe_est_a_gauche = int(position_bouffe[1] < y)
        bouffe_est_a_droite = int(position_bouffe[1] > y)
        bouffe_devant = int(position_bouffe[1] > x)
        bouffe_derriere = int(position_bouffe[1] < x)

        libre_a_gauche = int(not positions_valides.estDansGrille((x, y - step)))
        libre_a_droite = int(not positions_valides.estDansGrille((x, y + step)))
        libre_en_avant = int(not positions_valides.estDansGrille((x + step, y)))

    if direction_actuelle == "GAUCHE":
        bouffe_est_a_gauche = int(position_bouffe[1] > y)
        bouffe_est_a_droite = int(position_bouffe[1] < y)
        bouffe_devant = int(position_bouffe[1] < x)
        bouffe_derriere = int(position_bouffe[1] > x)
        libre_a_gauche = int(not positions_valides.estDansGrille((x, y + step)))
        libre_a_droite = int(not positions_valides.estDansGrille((x, y - step)))
        libre_en_avant = int(not positions_valides.estDansGrille((x - step, y)))

    if direction_actuelle == "HAUT":
        bouffe_est_a_gauche = int(position_bouffe[0] < x)
        bouffe_est_a_droite = int(position_bouffe[0] > x)
        bouffe_devant = int(position_bouffe[0] < y)
        bouffe_derriere = int(position_bouffe[0] > y)
        libre_a_gauche = int(not positions_valides.estDansGrille((x - step, y)))
        libre_a_droite = int(not positions_valides.estDansGrille((x + step, y)))
        libre_en_avant = int(not positions_valides.estDansGrille((x, y - step)))

    if direction_actuelle == "BAS":
        bouffe_est_a_gauche = int(position_bouffe[0] > x)
        bouffe_est_a_droite = int(position_bouffe[0] < x)
        bouffe_devant = int(position_bouffe[0] > y)
        bouffe_derriere = int(position_bouffe[0] < y)
        libre_a_gauche = int(not positions_valides.estDansGrille((x + step, y)))
        libre_a_droite = int(not positions_valides.estDansGrille((x - step, y)))
        libre_en_avant = int(not positions_valides.estDansGrille((x, y + step)))

