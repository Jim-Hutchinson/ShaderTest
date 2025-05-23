import elements
from elements import *
import camera
import geometry

class Scene:
    """
        Holds pointers to all objects in the scene
    """

    def __init__(self):
        """
            Set up scene objects.
        """
        # Map data for a single large room
        self.wall_geometry = [
            [6, 6, 6, 7, 7, 6, 6, 6],
            [6, 0, 0, 0, 0, 0, 0, 6],
            [6, 0, 0, 0, 0, 0, 0, 6],
            [8, 0, 0, 0, 0, 8, 8, 8],
            [8, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 6],
            [6, 0, 0, 0, 0, 0, 0, 6],
            [6, 6, 6, 7, 7, 6, 6, 6]
        ]
        self.floor_geometry = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 4, 0],
            [0, 4, 4, 4, 4, 4, 4, 0],
            [0, 4, 4, 4, 4, 4, 4, 0],
            [0, 4, 4, 4, 4, 4, 4, 0],
            [0, 4, 4, 4, 4, 4, 4, 0],
            [0, 4, 4, 4, 4, 4, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.ceiling_geometry = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.spheres = []  # No spheres in this scene

        # Multiple light sources in the room
        self.lights = [
            elements.Light(
                position=(2, 2, 0.5),
                color=(1, 0, 0),
                strength=1,
                axis=(0, 0, 1),
                radius=0,
                velocity=0
            ),
            elements.Light(
                position=(5, 2, 0.5),
                color=(0, 1, 0),
                strength=1,
                axis=(0, 0, 1),
                radius=0,
                velocity=0
            ),
            elements.Light(
                position=(2, 5, 0.5),
                color=(0, 0, 1),
                strength=1,
                axis=(0, 0, 1),
                radius=0,
                velocity=0
            ),
            elements.Light(
                position=(5, 5, 0.5),
                color=(1, 1, 0),
                strength=1,
                axis=(0, 0, 1),
                radius=0,
                velocity=0
            )
        ]

        self.rooms = []
        self.doors = []
        self.planes = []
        self.room_lookup = {}
        self.vertices = []
        self.vertexCount = 0

        self.camera = camera.Camera(
            posArray=[4, 4, 0.5]
        )

        self.outDated = True

        self.make_level()
        self.send_objects_to_rooms()
        self.finalize()

    def make_level(self):
        geometry.buildRooms(
            walls=self.wall_geometry, doors=self.doors, rooms=self.rooms
        )

        wall_mask = geometry.getLumpedGeometry(self.wall_geometry)

        for _room in self.rooms:
            for coordinate in _room.coordinates:
                row, col = coordinate
                self.room_lookup[coordinate] = _room
                geometry.getGeometryAtPoint(
                    row, col, _room,
                    self.wall_geometry, self.floor_geometry, self.ceiling_geometry, wall_mask
                )

            for coordinate in _room.internalCoordinates:
                row, col = coordinate
                self.room_lookup[coordinate] = _room
                geometry.getGeometryAtPoint(
                    row, col, _room,
                    self.wall_geometry, self.floor_geometry, self.ceiling_geometry, wall_mask
                )

        edges = geometry.getEdges(wall_mask)
        geometry.classifyEdges(edges)

        for _edge in edges:
            target = self.room_lookup[_edge.point_a]
            geometry.sendEdge(_edge, target)

        self.active_rooms = [self.rooms[0], ]

    def send_objects_to_rooms(self):
        while len(self.lights) > 0:
            _light = self.lights.pop()
            coordinate = (int(_light.position[1]), int(_light.position[0]))
            _room = self.room_lookup[coordinate]
            _room.add_light(_light)

    def finalize(self):
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        offset = 0
        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        # texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 8
        # tangent
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        # bitangent
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12
        # normal
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, 56, ctypes.c_void_p(offset))
        offset += 12

        for _room in self.rooms:
            _room.finalize()
            for _door in _room.doors:
                _door.finalize()

    def move_player(self, forwardsSpeed, rightSpeed):
        """
        attempt to move the player with the given speed
        """
        empty_blocks = (0, "d")
        dPos = forwardsSpeed * self.camera.forwards + rightSpeed * self.camera.right
        dx, dy = (dPos[0], dPos[1])

        row = int(self.camera.posArray[1] + 10 * dy)
        col = int(self.camera.posArray[0])
        if (self.wall_geometry[row][col] in empty_blocks):
            self.camera.posArray[1] += dy

        row = int(self.camera.posArray[1])
        col = int(self.camera.posArray[0] + 10 * dx)
        if (self.wall_geometry[row][col] in empty_blocks):
            self.camera.posArray[0] += dx

    def spin_player(self, dAngle):
        """
            shift the player's direction by the given amount, in degrees
        """
        self.camera.theta += dAngle[0]
        if (self.camera.theta < 0):
            self.camera.theta += 360
        elif (self.camera.theta > 360):
            self.camera.theta -= 360

        self.camera.phi += dAngle[1]
        if (self.camera.phi < -89):
            self.camera.phi = -89
        elif (self.camera.phi > 89):
            self.camera.phi = 89

        self.camera.recalculateCameraVectors()

    def update(self, rate):
        row = int(self.camera.posArray[1])
        col = int(self.camera.posArray[0])
        coordinate = (row, col)

        self.active_rooms = []

        for room in self.rooms:
            if coordinate in room.internalCoordinates:
                self.active_rooms.append(room)

                for _light in room.lights:
                    _light.update(rate)

        self.outDated = True