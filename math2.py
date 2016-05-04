# Jacob Kassman & Ryan McGrail
# math2.py
# Includes a variety of useful math functions.


import math
import random
import time


PI = 3.14159265
r2d = 180/PI
d2r = 1/r2d


# Calculating distance between 2 points
def ptDis(x1,y1, x2,y2):
	dy = y2-y1
	dx = x2-x1
	return math.sqrt(dx*dx + dy*dy)

	
# Calculating direction between 2 points (in degrees!!)
def ptDir(x1,y1, x2,y2):
	return math.atan2(-(y2-y1), x2-x1) * r2d

	
# Calculating smallest distance between 2 angles (in degrees!!)
def angDiff(ang1, ang2):
	a = (ang1 - ang2) % (2*360)
	b = (ang2 - ang1) % (2*360)
	return -a if a < b else b

	
# Calculating x/y component along (distance in degrees, direction)
def lenX(dis, dir):
	return dis * cosr(dir * d2r)
def lenY(dis, dir):
	return -dis * sinr(dir * d2r)

	
# Trig functions (w/ radians)	
def cosr(rad):
	return math.cos(rad)
def sinr(rad):
	return math.sin(rad)

	
# Trig functions (w/ degrees)
def cosd(dir):
	return cosr(dir * d2r)
def sind(dir):
	return sinr(dir * d2r)



# Simpler method for return current epoch
def epoch():
	return time.time()	

	
# Short version of random.random()
def rnd():
	return random.random()

	
# Finding square of number	
def sqr(x):
	return x * x


# Containing value between min and max value
def contain(mi, x, ma):
	return max(mi, min(x, ma) )


# Square root of #
def sqrt(x):
	return x**.5