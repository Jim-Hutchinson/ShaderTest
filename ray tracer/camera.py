from common import *

class Camera:
    """
        Represents a camera in the scene
    """

    def __init__(self, posArray):
        """
            Create a new camera at the given posArray facing in the given direction.

            Parameters:
                posArray (array [3,1])
                direction (array [3,1])
        """

        self.posArray = np.array(posArray, dtype=np.float32)
        self.theta = 0
        self.phi = 0
        self.recalculateCameraVectors()
    
    def recalculateCameraVectors(self):

        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)), 
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)), 
                np.sin(np.deg2rad(self.phi))
            ], dtype=np.float32
        )

        self.right = pyrr.vector.normalize(
            pyrr.vector3.cross(self.forwards, np.array([0,0,1],dtype=np.float32))
        )

        self.up = pyrr.vector.normalize(
            pyrr.vector3.cross(self.right, self.forwards)
        )