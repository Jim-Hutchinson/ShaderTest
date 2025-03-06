from common import *
import sphere
import plane

class Buffer:
    def __init__(self, size: int, binding: int, floatCount: int):

        self.size = size
        self.binding = binding
        self.floatCount = floatCount

        # (cx cy cz r) (r g b _)
        self.hostMemory = np.zeros(floatCount * size, dtype=np.float32)

        self.deviceMemory = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.deviceMemory)
        glBufferStorage(
            GL_SHADER_STORAGE_BUFFER, self.hostMemory.nbytes, 
            self.hostMemory, GL_DYNAMIC_STORAGE_BIT)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding, self.deviceMemory)
        self.elements_updated = 0

    def planeRecord(self, i: int, _plane: plane.Plane):

        if i >= self.size:
            return
        
        baseIndex = self.floatCount * i
        self.hostMem[baseIndex:baseIndex+3] = _plane.center[:]
        self.hostMem[baseIndex+3] = _plane.uMin

        self.hostMem[baseIndex+4:baseIndex+7] = _plane.tangent[:]
        self.hostMem[baseIndex+7] = _plane.uMax

        self.hostMem[baseIndex+8:baseIndex+11] = _plane.bitangent[:]
        self.hostMem[baseIndex+11] = _plane.vMin

        self.hostMem[baseIndex+12:baseIndex+15] = _plane.normal[:]
        self.hostMem[baseIndex+15] = _plane.vMax

        self.hostMem[baseIndex+16:baseIndex+19] = _plane.color[:]
        self.elements_written += 1

    def sphereRecord(self, i: int, _sphere: sphere.Sphere):

        if i >= self.size:
            return
        
        baseIndex = self.floatCount * i
        self.hostMem[baseIndex:baseIndex+3] = _sphere.center[:]
        self.hostMem[baseIndex+3] = _sphere.radius
        self.hostMem[baseIndex+4:baseIndex+7] = _sphere.color[:]
        self.elements_written += 1

    def read(self):
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.deviceMem)
        glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, self.floatCount * 4 * self.elements_written, self.hostMem)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, self.binding, self.deviceMem)
        self.elements_written = 0

    def destroy(self):
        glDeleteBuffers(1, (self.deviceMem,))