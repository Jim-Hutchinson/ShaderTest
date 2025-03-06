from common import *
class Material:

    def __init__(self, minDetail: int, maxDetail: int):
        
        self.detaiLevel = 0
        size = minDetail
        self.textures: list[int] = []
        self.sizes: list[int] = []

        while size < maxDetail:
            newTexture = glGenTextures(GL_TEXTURE0)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, newTexture)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA32F, size, size)
            self.textures.append(newTexture)
            self.sizes.append(size)
            size *=2


    def write(self):
        glActiveTexture(GL_TEXTURE0)
        glBindImageTexture(0, self.texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)

    def read(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, self.texture)

    def upscale(self):
        self.detaiLevel = min(len(self.textures)-1, self.detaiLevel+1)

    def downscale(self):
        self.detaiLevel = max(0, self.detaiLevel-1)