import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np

import meshes

class ScreenQuad(meshes.Mesh):

    def __init__(self):

        super().__init__()

        vertices = np.array(
            (1.0, 1.0,
             -1.0, 1.0,
             -1.0, -1.0,
             -1.0, -1.0,
             1.0, -1.0,
             1.0, 1.0),
             dtype=np.float32
        )
        
        self.vertCount = 6

        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
