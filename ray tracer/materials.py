from common import *
class Material:

    def __init__(self, width:int, height:int):
        
        self.texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGBA, GL_FLOAT, None)

    def write(self):
        glActiveTexture(GL_TEXTURE0)
        glBindImageTexture(0, self.texture, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)

    def read(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, self.texture)

#PBR Materials for later implementation
class PBRMaterial(Material):

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.albedo = glGenTextures(1)
        self.metallic = glGenTextures(1)
        self.roughness = glGenTextures(1)
        self.ao = glGenTextures(1)
        self._setup_texture(self.albedo, width, height)
        self._setup_texture(self.metallic, width, height)
        self._setup_texture(self.roughness, width, height)
        self._setup_texture(self.ao, width, height)

    def _setup_texture(self, texture, width, height):
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, width, height, 0, GL_RGBA, GL_FLOAT, None)

    def write(self):
        super().write()
        glBindImageTexture(1, self.albedo, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
        glBindImageTexture(2, self.metallic, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
        glBindImageTexture(3, self.roughness, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
        glBindImageTexture(4, self.ao, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)

    def read(self):
        super().read()
        glBindTexture(GL_TEXTURE_2D, self.albedo)
        glBindTexture(GL_TEXTURE_2D, self.metallic)
        glBindTexture(GL_TEXTURE_2D, self.roughness)
        glBindTexture(GL_TEXTURE_2D, self.ao)

    def destroy(self):
        super().destroy()
        glDeleteTextures(1, self.albedo)
        glDeleteTextures(1, self.metallic)
        glDeleteTextures(1, self.roughness)
        glDeleteTextures(1, self.ao)

