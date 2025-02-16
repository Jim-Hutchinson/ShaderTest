import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np

import engine

class App:
    def __init__(self):
        self.Width = 1600
        self.Height = 900
        self.pygamesetup()

        self.engine = engine.Engine(self.Width, self.Height)

        self.timersetup()

        self.mainloop()

def pygamesetup(self):
    # copilot setup of pygame for OpenGL 4.5
    pg.init()
    pg.display.gl_get_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
    pg.display.gl_get_attribute(pg.GL_CONTEXT_MINOR_VERSION, 5)
    pg.display.gl_get_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    pg.display.set_mode((self.Width, self.Height), pg.OPENGL | pg.DOUBLEBUF)
    pg.display.set_caption("Ray Tracer")

def timersetup(self):
    self.clock = pg.time.Clock()
    self.fps = 60

def mainloop(self):

    run = True
    while run:
        self.clock.tick(self.fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        self.engine.render()

        pg.display.flip()

def framerate(self):
    self.clock.tick(self.fps)

def quit(self):
    pg.quit()