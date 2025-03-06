from common import *

class Texture:
    def __init__(self, files):

        textureResolution = 1024        #textures are squares of N*N
        textureCount = len(files)       #files is a list of filenames of textures
        width = 5 * textureResolution   #5 textures
        height = textureResolution      #store textures as a single strip of 1 * N

        imageTypes = ("albedo", "emissive", "glossiness", "normal")     #PBR material properties

        textureLayers = [Image.new(mode = "RGBA", size = (width, height)) for _ in range(textureCount)]
        for i in range(textureCount):
            for j, imageType in enumerate(imageTypes):
                with Image.open(f"textures\{files[i]}\{files[i]}_{imageType}.png", mode = "r") as img:
                    #this line is barely readable god help me
                    img.convert("RGBA")
                    textureLayers[i].paste(img, (j * textureResolution, 0))

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexStorage3D(GL_TEXTURE_2D_ARRAY, 1, GL_RGBA32F,width, height,textureCount)
        #nah wtf copilot

        for i in range(textureCount):
            imgData = bytes(textureLayers[i].tobytes())
            glTexSubImage3D(GL_TEXTURE_2D_ARRAY,0,0,0,i,width, height, 1,GL_RGBA,GL_UNSIGNED_BYTE,imgData)

    def destroy(self):
        glDeleteTextures(1, self.texture)

