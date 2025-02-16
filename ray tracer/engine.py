import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np

import scrnQuad
import materials

class Engine:

    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height

        self.buildAssets()

    def buildAssets(self):
        self.screen = scrnQuad.ScreenQuad()

        self.colBuffer = materials.Material(self.width, self.height)

        self.shader = self.buildShader("shaders/frameBufferVertex.glsl", "shaders/frameBufferFragment.glsl")
        self.rayTracer = self.buildComputeShader("shaders/rayTracer.glsl")

    def buildShader(self, vertex:str, fragment:str):
        with open(vertex, 'r') as file:
            vertexSource = file.readlines()

        with open(fragment, 'r') as file:
            fragmentSource = file.readlines()

        return (compileProgram(compileShader(vertexSource, GL_VERTEX_SHADER), compileShader(fragmentSource, GL_FRAGMENT_SHADER)))

    def buildComputeShader(self, compute:str):
        with open(compute, 'r') as file:
            computeSource = file.readlines()

        return (compileProgram(compileShader(computeSource, GL_COMPUTE_SHADER)))
    
    def render(self):
        # tune these for optimal performance. Different GPUs may prefer different group sizes.
        workGroupWidth = self.width // 16
        workGroupHeight = self.height // 16

        glUseProgram(self.rayTracer)
        self.colBuffer.write()

        glDispatchCompute(workGroupWidth, workGroupHeight, 1)
        glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        self.draw()

    def draw(self):
        glUseProgram(self.shader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        self.colBuffer.read()
        self.screen.draw()
        pg.display.flip()

    
    def destroy(self):
        glDeleteProgram(self.rayTracer)
        self.colBuffer.destroy()
        self.screen.destroy()
        glDeleteProgram(self.shader)