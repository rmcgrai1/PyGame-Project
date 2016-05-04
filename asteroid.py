import canv3d
from mat import *

class Asteroid(object):
    MOD_ASTEROID = None;
    

    def __init__(self, size, x, y, z, rotX, rotY, rotZ):
        if Asteroid.MOD_ASTEROID == None:
            Asteroid.MOD_ASTEROID = canv3d.loadObj("asteroid.obj")
        self.size = size;
        self.x = x;
        self.y = y;
        self.z = z;
        self.rotX = rotX;
        self.rotY = rotY;
        self.rotZ = rotZ;


    def draw(self, screen):
        #canv3d.setMatIdentity(MAT_T)
		canv3d.setMatTranslation(MAT_T, self.x, self.y, self.z)
		canv3d.addMatRotationX(MAT_T, self.rotX)
		canv3d.addMatRotationX(MAT_T, self.rotY)
		canv3d.addMatRotationX(MAT_T, self.rotZ) 
		canv3d.addMatScale(MAT_T, 1, 1, 1)
		canv3d.compileMats()
		canv3d.drawObj(Asteroid.MOD_ASTEROID)

    def tick(self, input):
        pass;
