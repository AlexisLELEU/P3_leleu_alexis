
from 'classes/Labyrinthe'   import Labyrinthe
from pygame.locals          import *
import pygame


if "__main__" == __name__:

    pygame.init()
    
    labyrinth = Labyrinthe(LABYRINTHE_PATH)
    parselabyrinth = labyrinth.parseFile

    labyrinth.objet_repartition()


    boucle = True
    start = False

    
    while boucle:

        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_s):
                        start = True

        while start:
            labyrinth.showLabyrinthe

            pygame.display.flip()

            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):

                        if labyrinth.finish_the_game():
                            start = False

                        if (event.key == pygame.K_UP):
                            new_coo = labyrinth.find_new_coo('UP')
                        if (event.key == pygame.K_DOWN):
                            new_coo = labyrinth.find_new_coo('DOWN')
                        if (event.key == pygame.K_RIGHT):
                            new_coo = labyrinth.find_new_coo('RIGHT')
                        if (event.key == pygame.K_LEFT):
                            new_coo = labyrinth.find_new_coo('LEFT')
                    
                        labyrinth.can_move(new_coo)

                        labyrinth.showLabyrinthe
                        pygame.display.flip()

                    elif (event.key == pygame.K_ESCAPE):
                        boucle = False
                        start = False
                        break










