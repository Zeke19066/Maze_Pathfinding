'''
We generate the maze and feed it to the search_ai

At each tick, we plot the closed list;
once the finishline is found we flash the finl path in a different color.

Everything is generated and stored, to be rendered by the game in the loop.


EVERYTHING IN Y,X FORMAT

'''
import pygame
import numpy as np
import time
import os
import random
from collections import deque

import Maze_AI
import Maze_Generator

class SnakeGame():
    def __init__(self):
        print('Game Initialized!')
        self.ai_control = True #no human control.
        self.random_mode = True
        self.death_count = 0 #how many ded snek?

        self.res_x = 48*4#48
        self.res_y = 27*4#27
        self.pixel_size = 6
        self.game_speed = 6500
        self.final_speed = 0
        self.game_close = False

        self.modes = ["Squared Difference", "Geometric Mean", "Manhattan Heuristic"]
        self.py_ai = Maze_AI.Maze_AI(f_mode=0) #dont forget fmode
        self.maze_generator = Maze_Generator.Maze_Generator(self.res_y,self.res_x)
        self.cycle = 1

        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{100},{100}" # This is how we set the window position on the screen. Must come before pygame init.
        
        pygame.init()
        self.dis = pygame.display.set_mode((self.res_x*self.pixel_size, self.res_y*self.pixel_size))
        #self.dis = pygame.display.set_mode((self.res_x*self.pixel_size, self.res_y*self.pixel_size), pygame.FULLSCREEN)
        pygame.display.set_caption('Maze v1')

        self.screen = pygame.Surface((self.res_x, self.res_y))
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 10)
        self.score_font = pygame.font.SysFont("consolas", 10)

        self.color_dict={
            "white": (255, 255, 255),
            "yellow": (255, 240, 31), #(255, 255, 102),
            "orange": (255,165,0),#(255, 200, 50),
            "purple": (102, 0, 204),
            "pink": (255, 16, 240),
            "black": (0, 0, 0),
            "soft_red": (213, 50, 80),
            "red":(255,0,0),
            "green": (0, 255, 0),
            "soft_blue": (50, 153, 213),
            "blue": (0,0,255),
            "gray": (150,150,150),
            "light_gray": (200,200,200)
            }
        self.open_color = self.color_dict["light_gray"]

    def score_generator(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.color_dict["white"])
        self.screen.blit(value, [0, 0]) # Draw the score onto the screen at these coordinates.

    def path_plotter(self, path, finish_bool):
        path_color = self.path_colors[0]
        if finish_bool:
            path_color = self.path_colors[1]

        self.screen.fill(self.color_dict["black"])

    
        #first, plot the maze; Note maze dimensions must match resolution
        open_spaces = []
        for y in range(self.res_y):
            for x in range(self.res_x):
                if self.maze[y][x] == 0: #Open space; walls to be left black
                    open_spaces.append([y,x])

        for pixel in open_spaces:
            pygame.draw.rect(self.screen, self.open_color, [pixel[1], pixel[0], 1, 1])

        for pixel in path:
            pygame.draw.rect(self.screen, path_color, [pixel[1], pixel[0], 1, 1])

        self.dis.blit(pygame.transform.scale(self.screen, self.dis.get_rect().size), (0, 0))
        pygame.display.update()

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        #self.screen.blit(mesg, [int(self.res_x / 6), int(self.res_y / 3)])
        self.screen.blit(mesg, [0, int(self.res_y / 3)])

    def gameLoop(self):
        self.game_close, terminal_bool = False, False
        #setup the start of each game:
        self.path_colors = [self.color_dict["green"],self.color_dict["soft_blue"],self.color_dict["orange"], 
                    self.color_dict["purple"], self.color_dict["pink"], self.color_dict["yellow"]
                    ]
        random.shuffle(self.path_colors)
        rand = np.random.randint(3)
        self.py_ai.f_mode = rand #change the search mode randomly
        pygame.display.set_caption(f'Maze v1   f-Mode: {self.modes[rand]}')
        self.maze, self.start, self.finish = self.maze_generator.generator()

        #Main game loop
        for path_list, finish_bool in self.py_ai.astar_path(self.maze, self.start, self.finish):

            #First process user quit command if preset.
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminal_bool = True
                        pygame.quit()
                        quit()
                        return terminal_bool
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print('Exiting Now')
                            terminal_bool = True
                            pygame.quit()
                            quit()
                            return terminal_bool

            #now run the AI stuff
            self.path_plotter(path_list, finish_bool)

            if finish_bool:
                self.game_close = True
                break

            self.clock.tick(self.game_speed)
            self.cycle += 1
            #pygame.image.save(self.dis,"screenshot.png")

        time.sleep(1.5)
        # Exit Sequence
        if self.game_close == True:
            while self.game_close == True:
                if self.ai_control:
                    return terminal_bool

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminal_bool = True
                            return terminal_bool
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                print('Exiting Now')
                                terminal_bool = True
                                return terminal_bool
        

        pygame.quit()
        quit()

    def color_generator(self):
        return (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256))


def main():
    snek = SnakeGame()
    while 1:
        snek.gameLoop()

if __name__ == "__main__":
    main()