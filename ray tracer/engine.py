from common import *
import buffers
import scrnQuad
import materials
import scene
import texture

class Engine:

    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height

        self.targetFPS = 60
        self.FPSmargin = 10

        self.buildAssets()

    def buildAssets(self):
        self.screen = scrnQuad.ScreenQuad()

        self.colBuffer = materials.Material(self.width, self.height)

        self.makeNoiseTexture()
        self.makeMegaTexture()

        self.sphereBuffer = buffers.Buffer(size = 1024, binding = 1, floatCount = 8)
        self.planeBuffer = buffers.Buffer(size = 1024, binding = 2, floatCount = 20)

        # Update the paths to the correct locations of the shader files
        self.shader = self.buildShader("ray tracer/shaders/frameBufferVert.glsl", "ray tracer/shaders/frameBufferFrag.glsl")
        self.rayTracer = self.buildComputeShader("ray tracer/shaders/rayTracer.glsl")

    def makeNoiseTexture(self):
        self.noise = np.zeros(self.height * self.width * 4)

        for i in range (self.width * self.height * 4):
            radius = np.random.uniform(low = 0.0, high = 0.99)
            theta = np.random.uniform(low = 0.0, high = 2*np.pi)
            phi = np.random.uniform(low = 0.0, high = np.pi)
            deviation = np.array(
                [
                    radius * np.cos(theta) * np.cos(phi), 
                    radius * np.sin(theta) * np.cos(phi), 
                    radius * np.sin(phi)
                ], dtype=np.float32
            )
            self.noise[4*i:4*i+3] = deviation[:]

        self.noiseTexture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.noiseTexture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    
        glTexImage2D(
            GL_TEXTURE_2D,0,GL_RGBA32F, 
            4 * self.width,self.height,
            0,GL_RGBA,GL_FLOAT,bytes(self.noiseData)
        )

    def makeMegaTexture(self):
        filenames = [
            "AlienArchitecture", "AlternatingColumnsConcreteTile", "BiomechanicalPlumbing", 
            "CarvedStoneFloorCheckered", "ChemicalStrippedConcrete", "ClayBrick",
            "CrumblingBrickWall", "DiamondSquareFlourishTiles", "EgyptianHieroglyphMetal"
        ] #change to real names

        self.texture = texture.texture(filenames)


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