import pygame
from random                 import choice
from pygame.locals          import *
from 'settings/settings.py' import *
from 'classes/Gardien'      import Gardien
from 'classes/Objet'        import Objet
from 'classes/McGyver'      import McGyver
from 'classes/Labyrinthe'   import Labyrinthe

class Labyrinthe:
    def __init__(self, file):
        self._pygame_init()
        self._set_attributes(file)
        self._launch_init()
        
    def _pygame_init(self):
        self.screen = pygame.display.set_mode((HEIGHT, WIDTH))
        self.grass = pygame.image.load(PATH).convert()
        self.wall = pygame.image.load(WALL).convert()
        self.gardienEnd = pygame.image.load(GARDIEN).convert()
        self.perso = pygame.image.load(MCGYVER).convert()
        self.obj = pygame.image.load(OBJECT_IMG).convert()

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
    # Cette méthode permet de parse le fichier text du labyrinthe en dictionnaire de donnée
    # représentant les positions de chaque cases sur des coordonnées X et Y et leur état
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
            test =  tuple(j*IMG_SIZE for j in i)
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
        while range(len(self.objects)) != range(0,3):
            path = choice(self.getPathList)
            if (path in self.objects):
                pass
            else:
                self.objects.append(path)
                self.screen.blit(self.obj, tuple(j*IMG_SIZE for j in path))

    #
    # trouve les nouvelles coordonnées en fonction d'un déplacement (z, q, s, d)
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
    # methode 'manager' pour test et attribuer les nouvelles coordonnées
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
    # methode qui permet de déterminer si l'utilisateur a gagner le jeu ou non en arrivant sur l'arrivee
    #
    def finish_the_game(self):
        if self.dic[self.mcgyver.position] == 'arrivee' and self.objectsCount == 3:
           return True

        if self.dic[self.mcgyver.position] == 'arrivee'  and self.objectsCount != 3:
            return True

        return False

