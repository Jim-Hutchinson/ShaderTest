from common import *

"""
    Classes for common scene elements. Camera and edges stored separately for easier management.
"""

class Sphere:
    """
        Represents a sphere in the scene
    """

    def __init__(self, center, radius, color, roughness, axis, motion_radius, velocity):
        """
            Create a new sphere

            Parameters:
                center (array [3,1])
                radius (float)
                color (array [3,1])
        """

        self.center = np.array(center,dtype=np.float32)
        self.radius = radius
        self.color = np.array(color, dtype=np.float32)
        self.roughness = roughness
        self.t = 0
        self.motion_center = np.array(center, dtype=np.float32)
        self.axis = np.array(axis, dtype=np.float32)
        self.motion_radius = motion_radius
        self.velocity = velocity
    
    def update(self, rate):

        self.t += rate
        self.center = self.motion_center + self.motion_radius * self.axis * np.sin(self.velocity * self.t)

class Plane:
    """
        Represents a plane in the scene
    """


    def __init__(self, normal, tangent, bitangent, uMin, uMax, vMin, vMax, center, material_index):
        """
            Create a new plane

            Parameters:
                normal (array [3,1])
                tangent (array [3,1])
                bitangent (array [3,1])
                uMin,uMax,vMin,vMax (float) constraints, u: tangent, v: bitangent
                center (array [3,1])
                material_index int
        """

        self.normal = np.array(normal, dtype=np.float32)
        self.tangent = np.array(tangent, dtype=np.float32)
        self.bitangent = np.array(bitangent, dtype=np.float32)
        self.uMin = uMin
        self.uMax = uMax
        self.vMin = vMin
        self.vMax = vMax
        self.center = np.array(center, dtype=np.float32)
        self.material_index = material_index

class Light:
    """
        Represents a light in the scene
    """


    def __init__(self, position, color, strength, axis, radius, velocity):
        """
            Create a new plane

            Parameters:
                position (array [3,1])
                color (array [3,1])
                strength float
        """

        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.strength = strength
        self.t = 0
        self.center = np.array(position, dtype=np.float32)
        self.axis = np.array(axis, dtype=np.float32)
        self.radius = radius
        self.velocity = velocity
    
    def update(self, rate):

        self.t += rate
        self.position = self.center + self.radius * self.axis * np.sin(self.velocity * self.t)

class Door:

    """
        A door in the scene, links two rooms
    """


    def __init__(self, coordinate):
        """
            Create a new door.

            Parameters:
                coordinate (tuple (row,col)) grid coordinate on which the door sits
        """

        self.coordinate = coordinate
        self.planes = []
        self.vertices = []
        self.vertexCount = 0

        self.finalized = False
    
    def finalize(self):

        if self.finalized:
            return
        self.finalized = True

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        offset = 0
        #position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        #texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 8
        #tangent
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        #bitangent
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        #normal
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12

class Room:
    """
        Room object: holds a set of planes and doors
    """


    def __init__(self):

        self.planes = []
        self.spheres = []
        self.lights = []
        self.coordinates = []
        self.internalCoordinates = []
        self.doors = []

        self.vertices = []
        self.vertexCount = 0
    
    def add_light(self, light):

        if light not in self.lights:
            self.lights.append(light)
    
    def add_sphere(self, sphere):

        if sphere not in self.spheres:
            self.spheres.append(sphere)
    
    def finalize(self):

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        offset = 0
        #position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        #texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 8
        #tangent
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        #bitangent
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        #normal
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12