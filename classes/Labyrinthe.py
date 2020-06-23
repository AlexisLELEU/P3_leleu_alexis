from random                 import choice
import pygame
from pygame.locals          import *
from settings.settings import WIDTH, HEIGHT, PATH, WALL, GARDIEN, MCGYVER, OBJECT_IMG, MENU, BACKGROUND, IMG_SIZE
from .gardien      import Gardien
from .objet        import Objet
from .mcgyver     import McGyver

class Labyrinthe:
    def __init__(self, file):
        self._set_attributes(file)
        self._pygame_init()
        self._launch_init()

    def _pygame_init(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.grass = pygame.image.load(PATH).convert()
        self.wall = pygame.image.load(WALL).convert()
        self.gardien_end = pygame.image.load(GARDIEN).convert()
        self.perso = pygame.image.load(MCGYVER).convert()
        self.obj = pygame.image.load(OBJECT_IMG).convert()
        self.menu = pygame.image.load(MENU).convert()
        self.bg = pygame.image.load(BACKGROUND).convert()

    def _set_attributes(self, file):
        self.file = file
        self.dic = {}
        self.McGyver= ''
        self.gardien = ''
        self.objects = []
        self.objects_count = 0

    def _launch_init(self):
        self.parse_file()
        self.show_labyrinthe = self.show_labyrinthe()
        self.get_path_list = self.get_path_list()

    #
    # This method allows to parse the text file of the labyrinth in data dictionary
    # representing the positions of each box on X and Y coordinates and their state
    #
    def parse_file(self):
        file = open(self.file, mode='r', encoding='utf-8-sig')
        lines = file.readlines()
        file.close()
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == 'c':
                    self.dic.update({(i+15, j+10) : 'chemin'})
                if lines[i][j] == 'm':
                    self.dic.update({(i+15, j+10) : 'mur'})
                if lines[i][j] == 'D':
                    self.dic.update({(i+15, j+10) : 'depart'})
                    self.McGyver= McGyver((i+15, j+10))
                if lines[i][j] == 'A':
                    self.dic.update({(i+15, j+10) : 'arrivee'})
                    self.gardien = Gardien((i+15, j+10))
        return self.dic

    #
    # This method goes through the dictionary and forms a table grouping the coordinates
    # of all the boxes in the labyrinth path.
    #
    def get_path_list(self):
        path_list = []
        for i in self.dic:
            if self.dic[i] == 'chemin':
                path_list.append(i)
        return path_list

    def show_labyrinthe(self):
        self.screen.blit(self.bg, (0, 0))
        pygame.display.update()
        for i in self.dic:
            converted_tuple = tuple(j*IMG_SIZE for j in i)
            if self.dic[i] == 'chemin' or self.dic[i] == 'depart' or self.dic[i] == 'arrivee':
                self.screen.blit(self.grass, converted_tuple)
                if self.dic[i] == 'depart':
                    self.screen.blit(self.perso, converted_tuple)
                if self.dic[i] == 'arrivee':
                    self.screen.blit(self.gardien_end, converted_tuple)
            if self.dic[i] == 'mur':
                self.screen.blit(self.wall, converted_tuple)
        pygame.display.update()
        return True



    #
    # This method randomly distributes objects in the labyrinth,
    # being careful not to place two in the same box
    #
    def objet_repartition(self):
        while range(len(self.objects)) != range(0, 3):
            path = choice(self.get_path_list)
            if path in self.objects:
                pass
            else:
                self.objects.append(path)
                self.screen.blit(self.obj, tuple(j*IMG_SIZE for j in path))

    #
    # This method is about to find the new coordinates according to a displacement (z, q, s, d)
    #
    def find_new_coo(self, interaction):
        if interaction == 'LEFT':
            return (self.McGyver.position[0] - 1, self.McGyver.position[1])
        if interaction == 'RIGHT':
            return (self.McGyver.position[0] + 1, self.McGyver.position[1])
        if interaction == 'DOWN':
            return (self.McGyver.position[0], self.McGyver.position[1] + 1)
        if interaction == 'UP':
            return (self.McGyver.position[0], self.McGyver.position[1] - 1)

        return None
    #
    # 'manager' method for testing and assigning new coordinates
    #
    def can_move(self, new_coo):
        new_formatted_coo = tuple(j*IMG_SIZE for j in new_coo)
        last_coo = tuple(j*IMG_SIZE for j in self.McGyver.position)
        if(new_coo in self.dic and (self.dic[new_coo] == 'chemin' or self.dic[new_coo] == 'arrivee')):
            self.McGyver.position = new_coo
            self.screen.blit(self.perso, new_formatted_coo)
            self.screen.blit(self.grass, last_coo)
            if self.McGyver.position in self.objects:
                self.objects_count += 1

    #
    # Method to determine if the user has won the game or not when arriving on arrival
    #
    def finish_the_game(self):
        if self.dic[self.McGyver.position] == 'arrivee' and self.objects_count == 3:
            print('----------------' +
            '\n'+
            'VOUS AVEZ GAGNE'+
            '\n'+
            '----------------')
            return True

        if self.dic[self.McGyver.position] == 'arrivee' and self.objects_count != 3:
            print('----------------' +
            '\n'+
            'VOUS AVEZ PERDU, vous n\'avez pas recolte tous les objets'+
            '\n'+
            '----------------')
            return True

        return False
