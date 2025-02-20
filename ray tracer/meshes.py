from common import *

class Mesh:

    def __init__(self):
        self.vertCount = 0

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertCount)

    def destroy(self):
        glDeleteBuffers(1, self.vbo)
        glDeleteVertexArrays(1, self.vao)
