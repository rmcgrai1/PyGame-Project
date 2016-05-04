import canv3d
from mat import *

class Asteroid(object):
    """A very simple class that loads the object from the file and draws the asteroids at the same position and orientation every time."""
    MOD_ASTEROID = None;
    

    def __init__(self, a_id, size, x, y, z, rotX, rotY, rotZ):
        if Asteroid.MOD_ASTEROID == None:
            Asteroid.MOD_ASTEROID = canv3d.loadObj("asteroid.obj")
        self.scale = size * 0.0075;
        self.a_id = a_id;
        self.x = x;
        self.y = y;
        self.z = z;
        self.rotX = rotX;
        self.rotY = rotY;
        self.rotZ = rotZ;


    def draw(self, screen):
        canv3d.setMatTranslation(MAT_T, self.x, self.y, self.z)
        canv3d.addMatRotationX(MAT_T, self.rotX)
        canv3d.addMatRotationX(MAT_T, self.rotY)
        canv3d.addMatRotationX(MAT_T, self.rotZ) 
        canv3d.addMatScale(MAT_T, self.scale, self.scale, self.scale)
        canv3d.compileMats()
        canv3d.drawObj(Asteroid.MOD_ASTEROID)

    def tick(self, input):
        pass;
