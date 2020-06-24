from classes.labyrinthe    import Labyrinthe
from settings.settings     import *
from pygame.locals          import *
import pygame


if "__main__" == __name__:

    pygame.init()
    pygame.font.init()
    
    labyrinth = Labyrinthe(LABYRINTHE_PATH)
    parselabyrinth = labyrinth.parse_file

    labyrinth.objet_repartition()

    boucle = True

    while boucle:
        labyrinth.show_labyrinthe

        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):

                    if labyrinth.finish_the_game():
                        boucle = False

                    if (event.key == pygame.K_UP):
                        new_coo = labyrinth.find_new_coo('UP')
                    if (event.key == pygame.K_DOWN):
                        new_coo = labyrinth.find_new_coo('DOWN')
                    if (event.key == pygame.K_RIGHT):
                        new_coo = labyrinth.find_new_coo('RIGHT')
                    if (event.key == pygame.K_LEFT):
                        new_coo = labyrinth.find_new_coo('LEFT')
                
                    labyrinth.can_move(new_coo)

                    labyrinth.show_labyrinthe
                    pygame.display.flip()

                elif (event.key == pygame.K_ESCAPE):
                    boucle = False
                    break










