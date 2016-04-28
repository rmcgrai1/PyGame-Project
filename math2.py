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


SIN_BITS = 12
SIN_MASK = ~(-1 << SIN_BITS)
SIN_COUNT = SIN_MASK+1

RAD_FULL = PI*2
DEG_FULL = 360

RAD_TO_INDEX = SIN_COUNT/RAD_FULL
DEG_TO_INDEX = SIN_COUNT/DEG_FULL

SIN_ARRAY = [None]*SIN_COUNT
COS_ARRAY = [None]*SIN_COUNT
print("MATH")
for i in range(0,SIN_COUNT):
	SIN_ARRAY[i] = math.sin( float(i + 0.5) / SIN_COUNT * RAD_FULL);
	COS_ARRAY[i] = math.cos( float(i + 0.5) / SIN_COUNT * RAD_FULL);

	
def cosr(rad):
	return math.cos(rad)#COS_ARRAY[ int(rad * RAD_TO_INDEX) & SIN_MASK]
def sinr(rad):
	return math.sin(rad)#SIN_ARRAY[ int(rad * RAD_TO_INDEX) & SIN_MASK]
	
def cosd(dir):
	return cosr(dir * d2r)
def sind(dir):
	return sinr(dir * d2r)



# Simpler method for return current epoch
def epoch():
	return time.time()	


def rnd():
	return random.random()


# Containing value between min and max value
def contain(mi, x, ma):
	return max(mi, min(x, ma) )



# Getting sign (for raycasting function)	
def sgn(x):
	if x < 0:
		return -1
	else:
		return 1


# Raycasting intersection point from a point to circle boundary!!
def raycastCircle(rX,rY,rDir, cX,cY,cR):
	# If point inside circle, return original point
	if ptDis(cX,cY, rX,rY) <= cR:
		return (rX, rY)

	r = cR;

	x1 = rX - cX
	y1 = rY - cY

	dx = lenX(1,rDir)
	dy = lenY(1,rDir)

	x2 = x1 + dx
	y2 = y1 + dy
	
	dr2 = dx*dx + dy*dy
	
	D = x1*y2 - x2*y1
	
	# Calculate discriminant for determining how many intersections there will be
	disc = r*r * dr2 - D*D


	# No intersection
	if disc < 0:
		return False
		
	# Tangent
	elif disc == 0:
		x0 = cX + D*dy/dr2
		y0 = cY -D*dx/dr2

		if math.fabs(angDiff(ptDir(rX,rY,x0,y0), rDir)) < 2:
			return (x0, y0)
		else:
			return False
	
	# 2 Points--we want the closer point, the FIRST point of insersection!
	else:
		discSqr = math.sqrt(disc)
	
		# Point one
		x01 = ( D * dy + sgn(dy) * dx * discSqr ) / dr2
		y01 = ( -D * dx + math.fabs(dy) * discSqr ) / dr2

		# Point two
		x02 = ( D * dy - sgn(dy) * dx * discSqr ) / dr2
		y02 = ( -D * dx - math.fabs(dy) * discSqr ) / dr2
		
		d1 = ptDis(x1,y1, x01,y01)		
		d2 = ptDis(x1,y1, x02,y02)

		# Ensure the raycast direction and direction to the point are roughly equal--do NOT return points 180 degrees away from raycast direction!
		if d1 < d2 and math.fabs(angDiff(ptDir(rX,rY,cX+x01,cY+y01), rDir)) < 2:
			return (cX + x01, cY + y01)
		elif math.fabs(angDiff(ptDir(rX,rY,cX+x02,cY+y02), rDir)) < 2:
			return (cX + x02, cY + y02)
		else:
			return False

			
def sqrt(x):
	return x**.5

if __name__ == "__main__":
	t1 = 0
	t2 = 0

	for x in range(0,500000):
		ts = epoch()
		t1 += epoch()-ts

		ts = epoch()
		t2 += epoch()-ts
	
	print(t1)
	print(t2)