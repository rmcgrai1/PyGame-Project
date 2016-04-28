import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from pygame.gfxdraw	import *
from math2		import *
from drawable 		import Drawable


def createVec4(x,y,z,w):
	return [x,y,z,w]

def createVecPoint(x,y,z):
	return createVec4(x,y,z,1)

def createVecNormal(x,y,z):
	return createVec4(x,y,z,0)


def createMat16(a1, a2, a3, a4, b1, b2, b3, b4, c1, c2, c3, c4, d1, d2, d3, d4):
	return [a1, a2, a3, a4, b1, b2, b3, b4, c1, c2, c3, c4, d1, d2, d3, d4]


def set3(vec4, x,y,z):
	vec4[0] = x
	vec4[1] = y
	vec4[2] = z
	return vec4

def set4(vec4, x,y,z,w):
	vec4[0] = x
	vec4[1] = y
	vec4[2] = z
	vec4[3] = w
	return vec4

def set16(mat, a1, a2, a3, a4, b1, b2, b3, b4, c1, c2, c3, c4, d1, d2, d3, d4):
	mat[0] = a1
	mat[1] = a2
	mat[2] = a3
	mat[3] = a4
	mat[4] = b1
	mat[5] = b2
	mat[6] = b3
	mat[7] = b4
	mat[8] = c1
	mat[9] = c2
	mat[10] = c3
	mat[11] = c4
	mat[12] = d1
	mat[13] = d2
	mat[14] = d3
	mat[15] = d4
	return mat


def calculateLength(vec4):
	return sqrt(vec4[0]*vec4[0] + vec4[1]*vec4[1] + vec4[2]*vec4[2] + vec4[3]*vec4[3])

#def normalize(vec4):


def setMatIdentity(mat):
	return set16(mat,  1,0,0,0,  0,1,0,0,  0,0,1,0,  0,0,0,1)

def setMatTranslation(mat, x, y, z):
	return set16(mat,  1,0,0,x,  0,1,0,y,  0,0,1,z,  0,0,0,1)
def addMatTranslation(mat, x, y, z):
	setMatTranslation(tempMatAdd, x,y,z)
	return multMatMat(mat,tempMatAdd, mat)

def setMatScale(mat, sx, sy, sz):
	return set16(mat,  sx,0,0,0,  0,sy,0,0,  0,0,sz,0,  0,0,0,1)
def addMatScale(mat, sx, sy, sz):
	setMatScale(tempMatAdd, sx,sy,sz)
	return multMatMat(mat,tempMatAdd, mat)

def setMatRotationX(mat, degX):
	co = cosd(degX)
	si = sind(degX)
	return set16(mat,  1,0,0,0,  0,co,-si,0,  0,si,co,0,  0,0,0,1)
def addMatRotationX(mat, degX):
	setMatRotationX(tempMatAdd, degX)
	return multMatMat(mat,tempMatAdd, mat)
	
def setMatRotationY(mat, degY):
	co = cosd(degY)
	si = sind(degY)
	return set16(mat,  co,0,si,0,  0,1,0,0,  -si,0,co,0,  0,0,0,1)
def addMatRotationY(mat, degY):
	setMatRotationY(tempMatAdd, degY)
	return multMatMat(mat,tempMatAdd, mat)
	
def setMatRotationZ(mat, degZ):
	co = cosd(degZ)
	si = sind(degZ)
	return set16(mat,  co,si,0,0,  -si,co,0,0,  0,0,1,0,  0,0,0,1)
def addMatRotationZ(mat, degZ):
	setMatRotationZ(tempMatAdd, degZ)
	return multMatMat(mat,tempMatAdd, mat)


def copyVec(srcVec, dstVec):
	dstVec[0] = srcVec[0]
	dstVec[1] = srcVec[1]
	dstVec[2] = srcVec[2]
	dstVec[3] = srcVec[3]
	
	return dstVec

def copyMat(srcMat, dstMat):
	dstMat[0] = srcMat[0]
	dstMat[1] = srcMat[1]
	dstMat[2] = srcMat[2]
	dstMat[3] = srcMat[3]
	dstMat[4] = srcMat[4]
	dstMat[5] = srcMat[5]
	dstMat[6] = srcMat[6]
	dstMat[7] = srcMat[7]
	dstMat[8] = srcMat[8]
	dstMat[9] = srcMat[9]
	dstMat[10] = srcMat[10]
	dstMat[11] = srcMat[11]
	dstMat[12] = srcMat[12]
	dstMat[13] = srcMat[13]
	dstMat[14] = srcMat[14]
	dstMat[15] = srcMat[15]

	return dstMat

def multMatMat(mat1, mat2, dstMat):
	# Very ugly, but more efficient!!
	tempMatMult[0] = mat1[0]*mat2[0] + mat1[1]*mat2[4] + mat1[2]*mat2[8] + mat1[3]*mat2[12]
	tempMatMult[1] = mat1[0]*mat2[1] + mat1[1]*mat2[5] + mat1[2]*mat2[9] + mat1[3]*mat2[13]
	tempMatMult[2] = mat1[0]*mat2[2] + mat1[1]*mat2[6] + mat1[2]*mat2[10] + mat1[3]*mat2[14]
	tempMatMult[3] = mat1[0]*mat2[3] + mat1[1]*mat2[7] + mat1[2]*mat2[11] + mat1[3]*mat2[15]
	
	tempMatMult[4] = mat1[4]*mat2[0] + mat1[5]*mat2[4] + mat1[6]*mat2[8] + mat1[7]*mat2[12]
	tempMatMult[5] = mat1[4]*mat2[1] + mat1[5]*mat2[5] + mat1[6]*mat2[9] + mat1[7]*mat2[13]
	tempMatMult[6] = mat1[4]*mat2[2] + mat1[5]*mat2[6] + mat1[6]*mat2[10] + mat1[7]*mat2[14]
	tempMatMult[7] = mat1[4]*mat2[3] + mat1[5]*mat2[7] + mat1[6]*mat2[11] + mat1[7]*mat2[15]

	tempMatMult[8] = mat1[8]*mat2[0] + mat1[9]*mat2[4] + mat1[10]*mat2[8] + mat1[11]*mat2[12]
	tempMatMult[9] = mat1[8]*mat2[1] + mat1[9]*mat2[5] + mat1[10]*mat2[9] + mat1[11]*mat2[13]
	tempMatMult[10] = mat1[8]*mat2[2] + mat1[9]*mat2[6] + mat1[10]*mat2[10] + mat1[11]*mat2[14]
	tempMatMult[11] = mat1[8]*mat2[3] + mat1[9]*mat2[7] + mat1[10]*mat2[11] + mat1[11]*mat2[15]

	tempMatMult[12] = mat1[12]*mat2[0] + mat1[13]*mat2[4] + mat1[14]*mat2[8] + mat1[15]*mat2[12]
	tempMatMult[13] = mat1[12]*mat2[1] + mat1[13]*mat2[5] + mat1[14]*mat2[9] + mat1[15]*mat2[13]
	tempMatMult[14] = mat1[12]*mat2[2] + mat1[13]*mat2[6] + mat1[14]*mat2[10] + mat1[15]*mat2[14]
	tempMatMult[15] = mat1[12]*mat2[3] + mat1[13]*mat2[7] + mat1[14]*mat2[11] + mat1[15]*mat2[15]

	return copyMat(tempMatMult, dstMat)

	
def multMatMatSafe(mat1, mat2, dstMat):
	if len(mat1) != 16 or len(mat2) != 16 or len (dstMat) != 16:
		print("INVALID MATS!")
		exit()

	for y in range(0,4):
		for x in range(0,4):
			cell = 0
			for i in range(0,4):
				cell += mat1[4*y + i]*mat2[4*i + x]
			tempMatMult[4*y + x] = cell

	return copyMat(tempMatMult, dstMat)

def multMatVec(mat, vec, dstVec):
	if len(mat) != 16 or len(vec) != 4 or len (dstVec) != 4:
		print("INVALID MAT & VECS!")
		exit()

	for y in range(0,4):
		cell = 0
		for x in range(0,4):
			cell += mat[4*y + x]*vec[x]
		tempVec[y] = cell

	return copyVec(tempVec, dstVec)
	
def transpose(mat):
	copyMat(mat, tempMatTrans)
	for y in range(0,4):
		for x in range(0,4):
			mat[4*y + x] = tempMatTrans[4*x + y]
			
	return mat
	
def setMatPerspective2(mat, aspect, fov, f, n):
	#http://stackoverflow.com/questions/6060169/is-this-a-correct-perspective-fov-matrix
	
	print "FOV:", fov
	yscale = 1 / math.tan(fov/2 * d2r)
	xscale = yscale/aspect
	set16(mat,xscale,0,0,0,  0,yscale,0,0,  0,0,(f+n)/(n-f), -1,  0,0,2*f*n/(n-f),0)
	return transpose(mat)
def addMatPerspective2(mat, aspect, fov, f, n):
	setMatPerspective2(tempMatPersp, aspect, fov, f, n)
	return multMatMat(mat, tempMatPersp, mat)

def setMatPerspective(mat, l,r,t,b, f, n):
	set16(mat,2*n/(r-l),0,(r+l)/(r-l),0,  0,2*n/(t-b),(t+b)/(t-b),0,  0,0,-(f+n)/(f-n), -2*f*n/(f-n),  0,0,-1,0)
	return transpose(mat)
	
def setMatLook(mat, x,y,z, nx,ny,nz, upx,upy,upz):
	sx = ny*upz - upy*nz
	sy = -nx*upz + upx*nz
	sz = nx*upy - upx*ny
	l = math.sqrt(sx*sx + sy*sy + sz*sz)
	sx /= l
	sy /= l
	sz /= l

	upx = sy*nz - ny*sz
	upy = -sx*nz + nx*sz
	upz = sx*ny - nx*sy

	#print(str(upx) +", " + str(upy) + ", " + str(upz))
	
	set16(mat, sx,upx,-nx,0,  sy,upy,-ny,0,  sz,upz,-nz,0,  0,0,0,1)
	transpose(mat)
	
	return mat


def printVec(vec4):
	pass
	
	#print("<"+str(vec4[0]), end="")
	#for x in range(1,4):
	#	print(", "+str(vec4[x]), end="")
	#print(">")

def printMat(mat):
	pass
	# Get # of digits
	#curDigits = 0
	#maxDigits = 0	
	#for i in range(0,16):
	#	curDigits = len(str(mat[i]))
	#	if curDigits > maxDigits:
	#		maxDigits = curDigits			

	#curStr = ""
	#for y in range(0,4):
	#	print("|", end="")
	#	curStr = str(mat[4*y])
	#	print(" "*(maxDigits-len(curStr)), end="")
	#	print(curStr, end="")
	#	for x in range(1,4):
	#		curStr = str(mat[4*y + x])
	#		print(" "*(maxDigits-len(curStr)), end="")
	#		print(" "+curStr, end="")
	#	print("|")

tempVec = createVec4(0,0,0,0)
tempMatMult = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
tempMatAdd = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
tempMatTrans = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
tempMatPersp = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)

if __name__ == "__main__":

	matA = createMat16(1,2,3,4, 5,6,7,8, 9,10,11,12, 13,14,15,16)
	matB = createMat16(-20,21,-22,23, -24,25,26,-27, 28,-29,30,31, 32,33,34,-35)
	matAB = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
	vecA = createVec4(0,0,0,0)

	#setMatIdentity(matA)

	multMatMat(matA,matB, matAB)
	printMat(matAB)	
