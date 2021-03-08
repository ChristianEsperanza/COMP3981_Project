import pygame
# import pygame_gui

from GUI.gui import GUI
from Utility.constants import *


def main():
    pygame.init()
    gui = GUI()
    gui.run()

if __name__ == '__main__':
    main()
