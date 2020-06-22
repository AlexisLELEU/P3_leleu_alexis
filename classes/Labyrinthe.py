import pygame
from random                 import choice
from pygame.locals          import *
from settings.settings import *
from .Gardien      import Gardien
from .Objet        import Objet
from .McGyver      import McGyver

class Labyrinthe:
    def __init__(self, file):
        self._pygame_init()
        self._set_attributes(file)
        self._launch_init()
        
    def _pygame_init(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.grass = pygame.image.load(PATH).convert()
        self.wall = pygame.image.load(WALL).convert()
        self.gardienEnd = pygame.image.load(GARDIEN).convert()
        self.perso = pygame.image.load(MCGYVER).convert()
        self.obj = pygame.image.load(OBJECT_IMG).convert()
        self.menu = pygame.image.load(MENU).convert()
        self.bg = pygame.image.load(BACKGROUND).convert()

    def _set_attributes(self, file):
        self.file = file
        self.dic = {}
        self.mcgyver = ''
        self.gardien = ''
        self.objects = []
        self.objectsCount = 0

    def _launch_init(self):
        self.parseFile()
        self.getPathList = self.getPathList()
        self.showLabyrinthe = self.showLabyrinthe()

    #
    # This method allows to parse the text file of the labyrinth in data dictionary 
    # representing the positions of each box on X and Y coordinates and their state
    #
    def parseFile (self):
        file = open(self.file, mode = 'r', encoding = 'utf-8-sig')
        lines = file.readlines()
        file.close()
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == 'c':
                    self.dic.update({(i,j) : 'chemin'})
                if lines[i][j] == 'm':
                    self.dic.update({(i,j) : 'mur'})
                if lines[i][j] == 'D':
                    self.dic.update({(i,j) : 'depart'})
                    self.mcgyver = McGyver((i,j))
                if lines[i][j] == 'A':
                    self.dic.update({(i,j) : 'arrivee'})
                    self.gardien = Gardien((i,j))
        return self.dic

    #
    # This method goes through the dictionary and forms a table grouping the coordinates
    # of all the boxes in the labyrinth path.
    #
    def getPathList (self) :
        pathList = []
        for i in self.dic:
            if self.dic[i] == 'chemin':
                pathList.append(i)
        return pathList

    def showLabyrinthe (self):
        self.screen.blit(self.bg, (0, 0))
        pygame.display.update()
        for i in self.dic:
            convertedTuple =  tuple(j*IMG_SIZE for j in i)
            if self.dic[i] == 'chemin' or self.dic[i] == 'depart' or self.dic[i] == 'arrivee':
                self.screen.blit(self.grass, convertedTuple)
                if self.dic[i] == 'depart':
                    self.screen.blit(self.perso, convertedTuple)
                if self.dic[i] == 'arrivee':
                    self.screen.blit(self.gardienEnd, convertedTuple)
            if self.dic[i] == 'mur':
                self.screen.blit(self.wall, convertedTuple)
        pygame.display.update()
        return True



    #
    # This method randomly distributes objects in the labyrinth,
    # being careful not to place two in the same box
    #
    def objet_repartition(self):
        while range(len(self.objects)) != range(0,3):
            path = choice(self.getPathList)
            if (path in self.objects):
                pass
            else:
                self.objects.append(path)
                self.screen.blit(self.obj, tuple(j*IMG_SIZE for j in path))

    #
    # This method is about to find the new coordinates according to a displacement (z, q, s, d)
    #
    def find_new_coo(self, interaction):
        if interaction == 'LEFT':
            return (self.mcgyver.position[0] - 1, self.mcgyver.position[1])
        if interaction == 'RIGHT':
            return (self.mcgyver.position[0] + 1, self.mcgyver.position[1])
        if interaction == 'DOWN':
            return (self.mcgyver.position[0], self.mcgyver.position[1] + 1)
        if interaction == 'UP':
           return (self.mcgyver.position[0], self.mcgyver.position[1] - 1)

        return None
    #
    # 'manager' method for testing and assigning new coordinates
    #
    def can_move(self, new_coo):
        newFormattedCoo =  tuple(j*IMG_SIZE for j in new_coo)
        lastCoo =  tuple(j*IMG_SIZE for j in self.mcgyver.position)
        if(new_coo in self.dic and (self.dic[new_coo] == 'chemin' or self.dic[new_coo] == 'arrivee')):
            self.mcgyver.position = new_coo
            self.screen.blit(self.perso, newFormattedCoo)
            self.screen.blit(self.grass, lastCoo)
            if(self.mcgyver.position in self.objects):
                self.objectsCount += 1

    #
    # Method to determine if the user has won the game or not when arriving on arrival
    #
    def finish_the_game(self):
        if self.dic[self.mcgyver.position] == 'arrivee' and self.objectsCount == 3:
           return True

        if self.dic[self.mcgyver.position] == 'arrivee'  and self.objectsCount != 3:
            return True

        return False
