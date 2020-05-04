from random import choice
import pygame
from pygame.locals import *

class Labyrinthe:
    def __init__(self, file):
        self.screen = pygame.display.set_mode((640, 480))
        self.grass = pygame.image.load('grass.png').convert()
        self.wall = pygame.image.load('wall.png').convert()
        self.gardienEnd = pygame.image.load('Gardien.png').convert()
        self.perso = pygame.image.load('MacGyver.png').convert()
        self.file = file
        self.dic = {}
        self.mcgyver = ''
        self.parseFile()
        self.getPathList = self.getPathList()
        self.showLabyrinthe = self.showLabyrinthe()
        self.gardien = ''
        self.objets = []
        self.objetsCount = 0

    #
    # Cette méthode permet de parse le fichier text du labyrinthe en dictionnaire de donnée
    # représentant les positions de chaque cases sur des coordonnées X et Y et leur état
    #
    def parseFile (self):
        file = open(self.file, mode = 'r', encoding = 'utf-8-sig')
        lines = file.readlines()
        file.close()
        dic = {}
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == 'c':
                    dic.update({(i,j) : 'chemin'})
                if lines[i][j] == 'm':
                    dic.update({(i,j) : 'mur'})
                if lines[i][j] == 'D':
                    dic.update({(i,j) : 'depart'})
                    self.mcgyver = McGyver((i,j))
                if lines[i][j] == 'A':
                    dic.update({(i,j) : 'arrivee'})
                    self.gardien = Gardien((i,j))
        self.dic = dic
        return self.dic

    #
    # Cette méthode parcour le dictionnaire et forme un tableau regroupant les coordonnée
    # de toutes les cases chemin du labyrinthe
    #
    def getPathList (self) :
        pathList = []
        for i in self.dic:
            if self.dic[i] == 'chemin':
                pathList.append(i)
        return pathList

    def showLabyrinthe (self):
        for i in self.dic:
            test =  tuple(j*20 for j in i)
            if self.dic[i] == 'chemin' or self.dic[i] == 'depart' or self.dic[i] == 'arrivee':
                self.screen.blit(self.grass, test)
                if self.dic[i] == 'depart':
                    self.screen.blit(self.perso, test)
                if self.dic[i] == 'arrivee':
                    self.screen.blit(self.gardienEnd, test)
            if self.dic[i] == 'mur':
                self.screen.blit(self.wall, test)

    #
    # Cette méthode répartit aléatoirement, dans le labyrinthe, les objects en faisant attention
    # de ne pas en placer deux dans la même case
    #
    def objet_repartition(self):
        while range(len(self.objets)) != range(0,3):
            objects = choice(self.getPathList)
            if (objects in self.objets):
                pass
            else:
                self.objets.append(objects)
        print(self.objets)

    #
    # trouve les nouvelles coordonnées en fonction d'un déplacement (z, q, s, d)
    #
    def find_new_coo(self, interaction):
        if interaction == 'z':
            newPosition = (self.mcgyver.position[0] - 1, self.mcgyver.position[1])
        if interaction == 's':
            newPosition = (self.mcgyver.position[0] + 1, self.mcgyver.position[1])
        if interaction == 'd':
            newPosition = (self.mcgyver.position[0], self.mcgyver.position[1] + 1)
        if interaction == 'q':
            newPosition = (self.mcgyver.position[0], self.mcgyver.position[1] - 1)

        return newPosition
    #
    # methode 'manager' pour test et attribuer les nouvelles coordonnées
    #
    def can_move(self, new_coo):
        test = tuple(j*20 for j in new_coo)
        if(new_coo in self.dic and (self.dic[new_coo] == 'chemin' or self.dic[new_coo] == 'arrivee')):
            self.mcgyver.position = new_coo
            self.screen.blit(self.perso, test)
            if(self.mcgyver.position in self.objets):
                self.objetsCount += 1
        print(self.objetsCount)

    #
    # methode qui permet de déterminer si l'utilisateur a gagner le jeu ou non en arrivant sur l'arrivee
    #
    def finish_the_game(self):
        if self.dic[self.mcgyver.position] == 'arrivee' and self.objetsCount == 3:
           print('Vous Avez Gagné Bravo !!!!')
           return True

        if self.dic[self.mcgyver.position] == 'arrivee'  and self.objetsCount != 3:
            print('Vous n\'avez pas récuper tous les objects vous avez perdu !!!!')
            return True

        return False

class McGyver:
    def __init__ (self, position):
        self.position = position

class Gardien:
    def __init__ (self, position):
        self.position = position

class Objet:
    def __init__ (self):
        pass


 

if "__main__" == __name__:

    pygame.init()

    direction = ['z', 'q', 's', 'd']
    labyrinth = Labyrinthe('labyrinthe.txt')
    parselabyrinth = labyrinth.parseFile

    labyrinth.objet_repartition()

    labyrinth.showLabyrinthe

    pygame.display.flip()

    interaction = input('Entrez un déplacement: ')

    while interaction != 'e':

        interaction = input('Position non valdie: ')
        if(interaction in direction):

            if labyrinth.finish_the_game():
                break

            new_coo = labyrinth.find_new_coo(interaction)
            labyrinth.can_move(new_coo)
            interaction = input('Entrez un déplacement: ')

            pygame.display.update()

        else:
            interaction = input('Position non valdie: ')









