// http://www.tutorialspoint.com/python/python_further_extensions.htm

#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include "math2.h"
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include "obj.h"
#include "linalg.h"

#define MAT_MODELVIEW		0
#define MAT_PROJECTION		1
#define MAT_TRANSFORM 	    2

static double
	near = .1,
	pseudoNear,
	far = 300,
	aspect,

	tempVert1[4] = 	{0,0,0,1},
	tempVert2[4] = 	{0,0,0,1},
	tempVert3[4] = 	{0,0,0,1},
	modelviewMat[16] = {1,0,0,0, 
					 0,1,0,0,	
					 0,0,1,0, 
					 0,0,0,1},
	projMat[16] = 	{1,0,0,0, 
					 0,1,0,0,
					 0,0,1,0, 
					 0,0,0,1},
	transMat[16] = 	{1,0,0,0,
					 0,1,0,0, 
					 0,0,1,0, 
					 0,0,0,1},
   completeMat[16] = 	{1,0,0,0, 
				 0,1,0,0, 
				 0,0,1,0,
					 0,0,0,1},
  gCameraEye[4] = {0, 0, 0, 1},
  gCameraAt[4] = {0, 0, -1, 1},
  gCameraUp[4] = {0, 1, 0, 0};


static int 
	doFog = 0,
	doDepthTest = 1,
	doTexture = 1,
	
	RESOLUTION_WIDTH, 
	RESOLUTION_HEIGHT,
	PIXEL_NUMBER,
	CLEAR_PIXEL,
	RGBA,
	R, G, B, A,
	*pixels,
	*depths,
	*texture,
	textureWidth,
	textureHeight;
	
	
static void setRGB(int r, int g, int b);
static void clip(double w1, double w2, double w3, double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3);
static void drawTriangle0(double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3);
static void drawTriangle(double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3, int tries);
static void drawQuad0(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4);
static void drawQuad(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4, int tries);




static double* getMat(int matType) {
	switch(matType) {
		case MAT_MODELVIEW:			return modelviewMat;
		case MAT_PROJECTION:			return projMat;
	        case MAT_TRANSFORM:	                return transMat;
		default:				return NULL;
	}
}

static PyObject* pySetMatIdentity(PyObject *self, PyObject *args) {
	int matType;
	if(!PyArg_ParseTuple(args, "i", &matType))
      return NULL;
  
	setMatIdentity(getMat(matType));
	Py_RETURN_NONE;
}

static PyObject* pySetMatTranslation(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &x,&y,&z))
      return NULL;
  
	setMatTranslation(getMat(matType), x,y,z);
	Py_RETURN_NONE;
}
static PyObject* pyAddMatTranslation(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &x,&y,&z))
      return NULL;
  
	addMatTranslation(getMat(matType), x,y,z);
	Py_RETURN_NONE;
}
	
static PyObject* pySetMatScale(PyObject *self, PyObject *args) {
	int matType;
	double sx,sy,sz;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &sx, &sy, &sz))
      return NULL;
  
	setMatScale(getMat(matType), sx, sy, sz);
	Py_RETURN_NONE;
}
static PyObject* pyAddMatScale(PyObject *self, PyObject *args) {
	int matType;
	double sx,sy,sz;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &sx, &sy, &sz)) {
		printf("Failed to parse pyAddMatScale tuple!\n");
		return NULL;
	}
	
	addMatScale(getMat(matType), sx, sy, sz);
	Py_RETURN_NONE;
}

static PyObject* pySetMatRotationX(PyObject *self, PyObject *args) {
	int matType;
	double degX;
	if(!PyArg_ParseTuple(args, "id", &matType, &degX))
      return NULL;
  
	setMatRotationX(getMat(matType), degX);
	Py_RETURN_NONE;
}
static PyObject* pyAddMatRotationX(PyObject *self, PyObject *args) {
	int matType;
	double degX;
	if(!PyArg_ParseTuple(args, "id", &matType, &degX))
      return NULL;
  
	addMatRotationX(getMat(matType), degX);
	Py_RETURN_NONE;
}
		
static PyObject* pySetMatRotationY(PyObject *self, PyObject *args) {
	int matType;
	double degY;	
	if(!PyArg_ParseTuple(args, "id", &matType, &degY))
      return NULL;
  
	setMatRotationY(getMat(matType), degY);		
	Py_RETURN_NONE;
}	
static PyObject* pyAddMatRotationY(PyObject *self, PyObject *args) {
	int matType;
	double degY;	
	if(!PyArg_ParseTuple(args, "id", &matType, &degY))
      return NULL;
  
	addMatRotationY(getMat(matType), degY);		
	Py_RETURN_NONE;
}

static PyObject* pySetMatRotationZ(PyObject *self, PyObject *args) {
	int matType;
	double degZ;
	if(!PyArg_ParseTuple(args, "id", &matType, &degZ))
      return NULL;
  
	setMatRotationZ(getMat(matType), degZ);
	Py_RETURN_NONE;
}
static PyObject* pyAddMatRotationZ(PyObject *self, PyObject *args) {
	int matType;
	double degZ;
	if(!PyArg_ParseTuple(args, "id", &matType, &degZ))
      return NULL;
  
	addMatRotationZ(getMat(matType), degZ);
	Py_RETURN_NONE;
}

	
static double* setMatPerspective(double *mat, double fov) {
	// http://stackoverflow.com/questions/6060169/is-this-a-correct-perspective-fov-matrix
	
	double ys = 1. / tand(fov/2.);
	double xs = ys*aspect;
	
	set16(mat,
		xs,0,0,0,
		0,ys,0,0,
		0,0,(far+near)/(near-far),2*far*near/(near-far),
		0,0,-1,0);
	
	return mat;	
}
static PyObject* pySetMatPerspective(PyObject *self, PyObject *args) {
	int matType;
	double fov;	
	if(!PyArg_ParseTuple(args, "id", &matType, &fov))
      return NULL;
  
	setMatPerspective(getMat(matType), fov);		
	Py_RETURN_NONE;
}


static double* addMatPerspective(double *mat, double fov) {
	setMatPerspective(tempMatPersp, fov);
	return multMatMat(mat, tempMatPersp, mat);
}
static PyObject* pyAddMatPerspective(PyObject *self, PyObject *args) {
	int matType;
	double fov;
	if(!PyArg_ParseTuple(args, "id", &matType, &fov))
      return NULL;
  
	addMatPerspective(getMat(matType), fov);
	Py_RETURN_NONE;
}


double magnitude(double* vec, int length)
{
  int i;
  double sumTotal = 0;
  for (i = 0; i < length; i++)
    {
      sumTotal += vec[i] * vec[i];
    }
  return sqrt(sumTotal);
}

double * normalizeModify(double* vec, int length)
{
  double mag = magnitude(vec, length);
  int i;
  for (i = 0; i < length; i++)
      vec[i] = vec[i] / mag;
  return vec;
}

	
static double* setMatLook(double *mat, double x,double y,double z, double atX,double atY,double atZ, double upx,double upy,double upz) { 
	// Calculate front vector
	double
		nx = x-atX,
		ny = y-atY,
		nz = z-atZ,
		l = sqrt(nx*nx + ny*ny + nz*nz);
	nx /= l;
	ny /= l;
	nz /= l;	
  
	// Calculate side vector, then normalize
	double
		sx = upy*nz - ny*upz,
		sy = -upx*nz + nx*upz,
		sz = upx*ny - nx*upy;
	l = sqrt(sx*sx + sy*sy + sz*sz);
	sx /= l;
	sy /= l;
	sz /= l;

	// Calculate new up vector (doesn't need to be normalized b/c product of 2 normal vectors)
	upx = ny*sz - sy*nz;
	upy = -nx*sz + sx*nz;
	upz = nx*sy - sx*ny;

	// Calculate Translation
	double 
		sd = -(sx*x + sy*y + sz*z),
		upd = -(upx*x + upy*y + upz*z),
		nd = -(nx*x + ny*y + nz*z);

	return set16(mat, 
		sx,	sy,	sz,	sd,
		upx,upy,upz,upd,
		nx,	ny,	nz, nd,
		0,	0,	0,	1);
}

static PyObject* pySetMatLook(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z, nx,ny,nz, upx,upy,upz;
	if(!PyArg_ParseTuple(args, "iddddddddd", &matType, &x,&y,&z, &nx,&ny,&nz, &upx,&upy,&upz))
      return NULL;
  
	setMatLook(getMat(matType), x,y,z, nx,ny,nz, upx,upy,upz);		
	Py_RETURN_NONE;
}




static double* addMatLook(double* mat, double x,double y,double z, double nx,double ny,double nz, double upx,double upy,double upz) {
	setMatLook(tempMatPersp, x,y,z, nx,ny,nz, upx,upy,upz);
	return multMatMat(mat, tempMatPersp, mat);
}
static PyObject* pyAddMatLook(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z, nx,ny,nz, upx,upy,upz;
	if(!PyArg_ParseTuple(args, "iddddddddd", &matType, &x,&y,&z, &nx,&ny,&nz, &upx,&upy,&upz))
		return NULL;

	addMatLook(getMat(matType), x,y,z, nx,ny,nz, upx,upy,upz);
	Py_RETURN_NONE;
}



static double* setMatAntiLook(double* mat, double x,double y,double z, double nx,double ny,double nz, double upx,double upy,double upz) {
	return transpose(setMatLook(mat, x,y,z, nx,ny,nz, upx,upy,upz));
}
static PyObject* pySetMatAntiLook(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z, nx,ny,nz, upx,upy,upz;
	if(!PyArg_ParseTuple(args, "iddddddddd", &matType, &x,&y,&z, &nx,&ny,&nz, &upx,&upy,&upz))
		return NULL;

	setMatAntiLook(getMat(matType), x,y,z, nx,ny,nz, upx,upy,upz);
	Py_RETURN_NONE;
}

static double* addMatAntiLook(double* mat, double x,double y,double z, double nx,double ny,double nz, double upx,double upy,double upz) {
	setMatAntiLook(tempMatAdd, x,y,z, nx,ny,nz, upx,upy,upz);
	return multMatMat(mat, tempMatAdd, mat);
}
static PyObject* pyAddMatAntiLook(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z, nx,ny,nz, upx,upy,upz;
	if(!PyArg_ParseTuple(args, "iddddddddd", &matType, &x,&y,&z, &nx,&ny,&nz, &upx,&upy,&upz))
		return NULL;

	addMatAntiLook(getMat(matType), x,y,z, nx,ny,nz, upx,upy,upz);
	Py_RETURN_NONE;
}



//axis is an array of length 3
//angle is in degrees
//code adapted from Fall 2015 Computer Graphics
static double* rotateAboutAxis(double *mat, double angle, double* axis) {
  double x, y, z, c, omc, s;
  double normAxis[3];
  normAxis[0] = axis[0];
  normAxis[1] = axis[1];
  normAxis[2] = axis[2];

  normalizeModify(normAxis, 3);

  c = cosd( angle );
  omc = 1.0 - c;
  s = sind( angle );

  x = normAxis[0];
  y = normAxis[1];
  z = normAxis[2];
   
  mat[0] = x*x*omc + c; 
  mat[1] = x*y*omc - z*s;
  mat[2] = x*z*omc + y*s;
  mat[3] = 0;
  
  mat[4] = x*y*omc + z*s;
  mat[5] = y*y*omc + c;
  mat[6] = y*z*omc - x*s;
  mat[7] = 0;
  
  mat[8] = x*z*omc - y*s;
  mat[9] = y*z*omc + x*s;
  mat[10] = z*z*omc + c;
  mat[11] = 0;
  
  mat[12] = mat[13] = mat[14] = 0;
  mat[15] = 1;
    
    return mat;
}


static void rotateVecAboutAxis(double* vec, double angle, double* axis) {
	//http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/
		
	double
		a = 0,
		b = 0,
		c = 0,
		x = vec[0],
		y = vec[1],
		z = vec[2],
		u = axis[0],
		v = axis[1],
		w = axis[2],
		L = u*u + v*v + w*w,
		sqL = sqrt(L),
		co = cosd(angle),
		si = sind(angle),
		uxvywz = -u*x - v*y - w*z;
		
	vec[0] = (( -u*uxvywz )*(1-co) + L*x*co + sqL*(-w*y + v*z)*si) / L;
	vec[1] = (( -v*uxvywz )*(1-co) + L*y*co + sqL*(w*x - u*z)*si) / L;
	vec[2] = (( -w*uxvywz )*(1-co) + L*z*co + sqL*(-v*x + u*y)*si) / L;
}
static PyObject* pyRotateVecAboutAxis(PyObject *self, PyObject *args) {	
	int offset;
	PyArrayObject *vecArray, *axisArray;
	double angle;		
	if(!PyArg_ParseTuple(args, "O!idO!", &PyArray_Type,&vecArray, &offset, &angle, &PyArray_Type,&axisArray)) {
		printf("Failed to parse pyRotateVecAboutAxis tuple!\n");
		return NULL;
	}
	
	rotateVecAboutAxis((double*)(vecArray->data)+offset, angle, (double*)(axisArray->data));
	Py_RETURN_NONE;
}




//deltaX and deltaY are in degrees
static void turn(double *eyeVec, double *atVec, double *upVec, double deltaX, double deltaY) {
  //The idea is to have the camera swivel left when you move the mouse left, and swivel up and down when you move the mouse up and down, without gimbol locking.
  //We accomplish this by having at-eye and up be perpendicular to each other, and keep track of the up orientation outside of this function.
	double upDownRotate[16];
	double leftRightRotate[16];
	double toTransform[16];

	double sideAxis[4] = {0,0,0,0};

	//get sideAxis from up and at (all three should be perpendicular)
	mcross(
		upVec[0],upVec[1],upVec[2],
		atVec[0]-eyeVec[0],atVec[1]-eyeVec[1],atVec[2]-eyeVec[2],
		&sideAxis[0],&sideAxis[1],&sideAxis[2]);
  
	rotateAboutAxis(upDownRotate, deltaY, sideAxis);
    
	setMatTranslation(toTransform, eyeVec[0],eyeVec[1],eyeVec[2]);
	multMatMat(toTransform, upDownRotate, toTransform);
	addMatTranslation(toTransform, -eyeVec[0],-eyeVec[1],-eyeVec[2]);
	multMatVec3(toTransform, atVec, atVec, 1);

	multMatVec3(upDownRotate, upVec,upVec, 0);

	////printf("ud: (%.1lf,%.1lf,%.1lf), ca: (%.1lf,%.1lf,%.1lf) cu: (%.1lf,%.1lf,%.1lf)\n", globalUpDownAxis[0], globalUpDownAxis[1], globalUpDownAxis[2], gCameraAt[0], gCameraAt[1], gCameraAt[2], gCameraUp[0], gCameraUp[1], gCameraUp[2]);

	rotateAboutAxis(leftRightRotate, deltaX, upVec);

	setMatTranslation(toTransform, eyeVec[0],eyeVec[1],eyeVec[2]);
	multMatMat(toTransform, leftRightRotate, toTransform);
	addMatTranslation(toTransform, -eyeVec[0],-eyeVec[1],-eyeVec[2]);
	multMatVec3(toTransform, atVec, atVec, 1);
}
static PyObject* pyTurn(PyObject *self, PyObject *args) {
	PyArrayObject *eyeArray, *atArray, *upArray;
	double deltaX, deltaY;
	int eyeOffset, atOffset, upOffset;	
	if(!PyArg_ParseTuple(args, "O!iO!iO!idd", &PyArray_Type,&eyeArray,&eyeOffset,  &PyArray_Type,&atArray,&atOffset,  &PyArray_Type,&upArray,&upOffset,  &deltaX, &deltaY)) {
		printf("Failed to parse pyTurn tuple!\n");
		return NULL;
	}  
	
	turn((double*)(eyeArray->data)+eyeOffset, (double*)(atArray->data)+atOffset, (double*)(upArray->data)+upOffset, deltaX, deltaY);
	Py_RETURN_NONE;
}

static double* setMatCamera(double* mat) {
	return setMatLook(mat, gCameraEye[0], gCameraEye[1], gCameraEye[2], gCameraAt[0], gCameraAt[1], gCameraAt[2], gCameraUp[0], gCameraUp[1], gCameraUp[2]);
}
static PyObject* pySetMatCamera(PyObject *self, PyObject *args) {
	int matType;
	if(!PyArg_ParseTuple(args, "i", &matType)) {
		printf("Failed to parse pySetMatCamera tuple!\n");
		return NULL;
	}
	
	setMatCamera(getMat(matType));
	Py_RETURN_NONE;
}



static void camera(double eyeX, double eyeY, double eyeZ, double atX, double atY, double atZ, double upX, double upY, double upZ) {
	gCameraEye[0] = eyeX;
	gCameraEye[1] = eyeY;
	gCameraEye[2] = eyeZ;

	gCameraAt[0] = atX;
	gCameraAt[1] = atY;
	gCameraAt[2] = atZ;
	
	gCameraUp[0] = upX;
	gCameraUp[1] = upY;
	gCameraUp[2] = upZ;
}
static PyObject* pyCamera(PyObject *self, PyObject *args) {
	double
		eyeX, eyeY, eyeZ,
		atX, atY, atZ,
		upX, upY, upZ;
	if(!PyArg_ParseTuple(args, "ddddddddd", &eyeX,&eyeY,&eyeZ, &atX,&atY,&atZ, &upX,&upY,&upZ)) {
		printf("Failed to parse pyCamera tuple!\n");
		return NULL;
	}

	camera(
		eyeX, eyeY, eyeZ,
		atX, atY, atZ,
		upX, upY, upZ);
	Py_RETURN_NONE;
}


static double* addMatCamera(double* mat) {
	setMatCamera(tempMatAdd);
	return multMatMat(mat,tempMatAdd, mat);
}
static PyObject* pyAddMatCamera(PyObject *self, PyObject *args) {
	int id;
	if(!PyArg_ParseTuple(args, "i", &id))
		return NULL;
	
	addMatCamera(getMat(id));
	Py_RETURN_NONE;
}


static double* setMatCameraPosition(double *mat) {
  setMatIdentity(mat);
  setMatTranslation(mat, gCameraEye[0], gCameraEye[1], gCameraEye[2]);
  return mat;
}
static PyObject* pySetMatCameraPosition(PyObject *self, PyObject *args) {
  int matType;
  if(!PyArg_ParseTuple(args, "i", &matType))
    return NULL;
  
  setMatCameraPosition(getMat(matType));
  Py_RETURN_NONE;
}

static double* addMatCameraPosition(double *mat) {
	setMatCameraPosition(tempMatAdd);
	return multMatMat(mat,tempMatAdd, mat);
}
static PyObject* pyAddMatCameraPosition(PyObject *self, PyObject *args) {
  int matType;
  if(!PyArg_ParseTuple(args, "i", &matType))
    return NULL;
  
  addMatCameraPosition(getMat(matType));
  Py_RETURN_NONE;
}



static double* setMatCameraRotation(double *mat) {
	setMatIdentity(mat);
	setMatLook(mat, 0,0,0, (gCameraAt[0]-gCameraEye[0]),(gCameraAt[1]-gCameraEye[1]),(gCameraAt[2]-gCameraEye[2]), gCameraUp[0],gCameraUp[1],gCameraUp[2]);
	return mat;
}
static PyObject* pySetMatCameraRotation(PyObject *self, PyObject *args) {
  int matType;
  if(!PyArg_ParseTuple(args, "i", &matType))
    return NULL;
  
  setMatCameraRotation(getMat(matType));
  Py_RETURN_NONE;
}

static double* addMatCameraRotation(double *mat) {
	setMatCameraRotation(tempMatAdd);
	return multMatMat(mat,tempMatAdd, mat);
}
static PyObject* pyAddMatCameraRotation(PyObject *self, PyObject *args) {
  int matType;
  if(!PyArg_ParseTuple(args, "i", &matType))
    return NULL;
  
  addMatCameraRotation(getMat(matType));
  Py_RETURN_NONE;
}




static double* setMatCameraAntiRotation(double *mat) {
	setMatIdentity(mat);
	setMatAntiLook(mat, 0,0,0, (gCameraAt[0]-gCameraEye[0]),(gCameraAt[1]-gCameraEye[1]),(gCameraAt[2]-gCameraEye[2]), gCameraUp[0],gCameraUp[1],gCameraUp[2]);
	return mat;
}
static PyObject* pySetMatCameraAntiRotation(PyObject *self, PyObject *args) {
  int matType;
  if(!PyArg_ParseTuple(args, "i", &matType))
    return NULL;
  
  setMatCameraAntiRotation(getMat(matType));
  Py_RETURN_NONE;
}


static double* addMatCameraAntiRotation(double *mat) {
	setMatCameraAntiRotation(tempMatAdd);
	return multMatMat(mat,tempMatAdd, mat);
}
static PyObject* pyAddMatCameraAntiRotation(PyObject *self, PyObject *args) {
  int matType;
  if(!PyArg_ParseTuple(args, "i", &matType))
    return NULL;
  
  addMatCameraAntiRotation(getMat(matType));
  Py_RETURN_NONE;
}


static void init(int resW, int resH, double n, double f, int dFog, int* pixs) {
	RESOLUTION_WIDTH = resW;
	RESOLUTION_HEIGHT = resH;
	PIXEL_NUMBER = resW*resH;
	
	srand(time(NULL));
	
	aspect = 1. * resW / resH;
	
	near = n;
	pseudoNear = near + 5;
	far = f;
	doFog = dFog;
	
	CLEAR_PIXEL = convertRGBA2Int(0, 0, 0, 255);

	pixels = pixs; //(int*) malloc(PIXEL_NUMBER * sizeof(int));
	depths = (int*) malloc(PIXEL_NUMBER * sizeof(int));
	
	int i;
	for(i = 0; i < PIXEL_NUMBER; i++)
		pixels[i] = 0;	
}
static PyObject* pyInit(PyObject *self, PyObject *args) {
	//http://scipy-cookbook.readthedocs.io/items/C_Extensions_NumPy_arrays.html
	int resW, resH, doFog;
	PyArrayObject *arrayin;
	double n, f;
	if(!PyArg_ParseTuple(args, "iiddiO!", &resW,&resH,&n,&f,&doFog, &PyArray_Type,&arrayin))
	    return NULL;
  
	init(resW,resH,n,f,doFog, (int*) (arrayin->data));
	Py_RETURN_NONE;
}



static void setTexture(int* texPixs, int w, int h) {
	texture = texPixs;
	textureWidth = w;
	textureHeight = h;
}
static PyObject* pySetTexture(PyObject *self, PyObject *args) {
	PyArrayObject *arrayin;
	int w, h;
	if(!PyArg_ParseTuple(args, "O!ii", &PyArray_Type,&arrayin, &w, &h)) {
	    return NULL;
	}
  
	setTexture((int*) (arrayin->data), w, h);
	Py_RETURN_NONE;
}


static void unsetTexture() {
	texture = NULL;
	textureWidth = -1;
	textureHeight = -1;
}
static PyObject* pyUnsetTexture(PyObject *self) {
	unsetTexture();
	Py_RETURN_NONE;
}


/************************  DRAWING FUNCTIONS  *****************************/

// Loop through each pixel & clear screen
static void clear(void) {
	int i;
	for(i = 0; i < PIXEL_NUMBER; i++) {
		pixels[i] = CLEAR_PIXEL;
		depths[i] = far;
	}
}
static PyObject* pyClear(PyObject *self) {  
	clear();
	Py_RETURN_NONE;
}


static void clipTriangle(double x1,double y1,double z1,double u1,double v1,double w1,	double x2,double y2,double z2,double u2,double v2,double w2,  double x3,double y3,double z3,double u3,double v3, double w3) {
	//http://www.cubic.org/docs/3dclip.htm
		
	double 
		s12 = w1/(w1-w2),
		s13 = w1/(w1-w3),
		
		x01 = x1 + s12 * (x2 - x1),
		y01 = y1 + s12 * (y2 - y1),
		z01 = z1 + s12 * (z2 - z1),
		u01 = u1 + s12 * (u2 - u1),
		v01 = v1 + s12 * (v2 - v1),
		x02 = x1 + s13 * (x3 - x1),
		y02 = y1 + s13 * (y3 - y1),
		z02 = z1 + s13 * (z3 - z1),
		u02 = u1 + s13 * (u3 - u1),
		v02 = v1 + s13 * (v3 - v1);
		
	drawTriangle(
		x1,y1,z1,u1,v1,
		x01,y01,z01,u01,v01,
		x02,y02,z02,u02,v02,1);
}

static void clipQuad(double x1,double y1,double z1,double u1,double v1,double w1,	double x2,double y2,double z2,double u2,double v2,double w2,  double x3,double y3,double z3,double u3,double v3, double w3) {
	//http://www.cubic.org/docs/3dclip.htm
	
	double 
		s12 = w1/(w1-w2),
		s13 = w1/(w1-w3),
		
		x01 = x1 + s12 * (x2 - x1),
		y01 = y1 + s12 * (y2 - y1),
		z01 = z1 + s12 * (z2 - z1),
		u01 = u1 + s12 * (u2 - u1),
		v01 = v1 + s12 * (v2 - v1),
		
		x02 = x1 + s13 * (x3 - x1),
		y02 = y1 + s13 * (y3 - y1),
		z02 = z1 + s13 * (z3 - z1),
		u02 = u1 + s13 * (u3 - u1),
		v02 = v1 + s13 * (v3 - v1);
	
	drawTriangle(
		x01,y01,z01,u01,v01,
		x2,y2,z2,u2,v2,
		x3,y3,z3,u3,v3, 1);
	drawTriangle(
		x3,y3,z3,u3,v3,
		x2,y2,z2,u2,v2,
		x02,y02,z02,u02,v02, 1);
}

static void clip(double x1,double y1,double z1,double u1,double v1,double w1,  double x2,double y2,double z2,double u2,double v2,double w2,  double x3,double y3,double z3,double u3,double v3,double w3) {
	//TODO: FIX CLIPPING ERROR

	int w1N = w1 < pseudoNear,
		w2N = w2 < pseudoNear,
		w3N = w3 < pseudoNear;
			
	if(w1N && !w2N && !w3N) {
		clipQuad(x1,y1,z1,u1,v1,w1,
			x2,y2,z2,u2,v2,w2,
			x3,y3,z3,u3,v3,w3);
	}
	else if(!w1N && w2N && !w3N) {
		clipQuad(x2,y2,z2,u2,v2,w2,
			x3,y3,z3,u3,v3,w3,
			x1,y1,z1,u1,v1,w1);
	}
	else if(!w1N && !w2N && w3N) {
		clipQuad(x3,y3,z3,u3,v3,w3,
			x1,y1,z1,u1,v1,w1,
			x2,y2,z2,u2,v2,w2);
	}
	else if(!w1N) {
		clipTriangle(x1,y1,z1,u1,v1,w1,
			x2,y2,z2,u2,v2,w2,
			x3,y3,z3,u3,v3,w3);
	}
	else if(!w2N) {
		clipTriangle(x2,y2,z2,u2,v2,w2,
			x3,y3,z3,u3,v3,w3,
			x1,y1,z1,u1,v1,w1);
	}
	else if(!w3N) {
		clipTriangle(x3,y3,z3,u3,v3,w3,
			x1,y1,z1,u1,v1,w1,
			x2,y2,z2,u2,v2,w2);
	}
}

static void drawTriangle0(double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3) {
	drawTriangle(x1,y1,z1,u1,v1,
			x2,y2,z2,u2,v2,
			x3,y3,z3,u3,v3, 0);
}


	
static void drawTriangle(double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3, int tries) {
	set4(tempVert1, x1,y1,z1,1);
	set4(tempVert2, x2,y2,z2,1);
	set4(tempVert3, x3,y3,z3,1);

	multMatVec(completeMat, tempVert1, tempVert1);
	multMatVec(completeMat, tempVert2, tempVert2);
	multMatVec(completeMat, tempVert3, tempVert3);

	
	double oz1 = z1, oz2 = z2, oz3 = z3;
	
	double w1, w2, w3,
		miX, miY, maX, maY,
	        //x01, y01, z01,
	        x21, y21, z21,
	        x31, y31, z31,
	        //x32, y32, z32,
		az, bz, c,
	        //au, bu,
		//av, bv,
		area,
		s, t,
		depth;
		
	int x,y, u,v, miXi,miYi,maXi,maYi;
	//double ow1, ow2, ow3;
	
	
	
	/*ow1 = */w1 = tempVert1[3];	
	z1 = tempVert1[2]; ///w1;

	/*ow2 = */w2 = tempVert2[3];				
	z2 = tempVert2[2]; ///w2;
	
	/*ow3 = */w3 = tempVert3[3];
	z3 = tempVert3[2]; ///w3;

	// Completely outside of the frustem
	if(tries == 0) {
		if((z1 < near && z2 < near && z3 < near) || (z1 > far && z2 > far && z3 > far)) {
			////printf("offscreen...\n");
			return;
		}

		//Partially outside, need to clip
		if(z1 < pseudoNear || z2 < pseudoNear || z3 < pseudoNear) {		
			//printf("CLIP!\n");
			clip(x1,y1,oz1,u1,v1,	z1,
				x2,y2,oz2,u2,v2,	z2,
				x3,y3,oz3,u3,v3,	z3);
			return;
		}
	}
	
	//printf("ws <%lf, %lf, %lf>\n", w1, w2, w3);	

	w1 = fabs(w1);
	x1 = tempVert1[0]/-w1;
	y1 = tempVert1[1]/-w1;

	w2 = fabs(w2);
	x2 = tempVert2[0]/-w2;
	y2 = tempVert2[1]/-w2;
	
	w3 = fabs(w3);
	x3 = tempVert3[0]/-w3;
	y3 = tempVert3[1]/-w3;

	/*printf("--------------------------\n");	
	printf("ws <%lf, %lf, %lf>\n", w1, w2, w3);	
	printf("pt1 <%lf, %lf, %lf>\n", x1, y1, z1);
	printf("pt2 <%lf, %lf, %lf>\n", x2, y2, z2);
	printf("pt3 <%lf, %lf, %lf>\n", x3, y3, z3);
	printf("--------------------------\n");	
	printf("\n");*/
	
	
	miX = (x1 < x2) ? ((x1 < x3) ? x1 : x3) : ((x2 < x3) ? x2 : x3);
	miY = (y1 < y2) ? ((y1 < y3) ? y1 : y3) : ((y2 < y3) ? y2 : y3);
	maX = (x1 > x2) ? ((x1 > x3) ? x1 : x3) : ((x2 > x3) ? x2 : x3);
	maY = (y1 > y2) ? ((y1 > y3) ? y1 : y3) : ((y2 > y3) ? y2 : y3);

	miXi = (int) ((miX < 0) ? 0 : miX);
	miYi = (int) ((miY < 0) ? 0 : miY);
	maXi = (int) ((maX < RESOLUTION_WIDTH) ? maX : RESOLUTION_WIDTH);
	maYi = (int) ((maY < RESOLUTION_HEIGHT) ? maY : RESOLUTION_HEIGHT);

	x21 = x2-x1;
	y21 = y2-y1;
	z21 = z2-z1;

	x31 = x3-x1;
	y31 = y3-y1;
	z31 = z3-z1;
	
	/*
	x32 = x3-x2;
	y32 = y3-y2;
	z32 = z3-z2;
	*/

	az = y21*z31 - y31*z21;
	bz = -x21*z31 + x31*z21;
	c = x21*y31 - x31*y21;

	area = .5*(-y2*x3 + y1*(-x2+x3) + x1*(y2-y3) + x2*y3);
	
	if(area == 0)
		return;

	
	double b1, b2, b3, 
		bDenom = -1./((y2-y3)*x31 + (x3-x2)*y31);

	int index, dRGBA=0, 
		dR=0, dG=0, dB=0, dA=0,
		pR=0, pG=0, pB=0, pA=0;
	double val = 1, wp, up, vp, fr;						
	for(x = miXi; x < maXi; x++) {
		for(y = miYi; y < maYi; y++) {
			s = 1/(2*area)*(y1*x3 - x1*y3 + y31*x - x31*y);
			t = 1/(2*area)*(x1*y2 - y1*x2 - y21*x + x21*y);
			
			if(0 <= s && s <= 1 && 0 <= t && t <= 1 && s+t <= 1) {
				depth = (z1 + (az*(x-x1) + bz*(y-y1))/-c);
			
				b1 = ((y2-y3)*(x-x3) + (x3-x2)*(y-y3)) * bDenom;
				b2 = ((y3-y1)*(x-x3) + (x1-x3)*(y-y3)) * bDenom;
				b3 = 1. - b1 - b2;
								
				if(!doDepthTest || (depth >= near && depth <= far)) {
					index = y*RESOLUTION_WIDTH + x;

					if(!doDepthTest || (depth < depths[index])) {
						depths[index] = depth;
						
						if(texture == NULL || !doTexture) {
							if(!doFog)
								pixels[index] = RGBA;
							else {
								val = contain(0, (far-depth)/(far-near), 1);
								pixels[index] = convertRGB2Int((int)(R*val),(int)(G*val),(int)(B*val));
							}
						}
						else {
							wp = ( 1 / w1 ) * b1 + ( 1 / w2 ) * b2 + ( 1 / w3 ) * b3;
							up = ( ( u1 / w1 ) * b1 + ( u2 / w2 ) * b2 + ( u3 / w3 ) * b3 ) / wp;
							vp = ( ( v1 / w1 ) * b1 + ( v2 / w2 ) * b2 + ( v3 / w3 ) * b3 ) / wp;
						
							if(up < 0 || up > 1)
								up = fabs(fmod(up,1));
							if(vp < 0 || vp > 1)
								vp = fabs(fmod(vp,1));
						
							u = (int)(textureWidth * up);
							v = (int)(textureHeight * vp);

							
							dRGBA = texture[textureWidth*v + u];
							convertInt2RGBA(dRGBA, &dR,&dG,&dB,&dA);
							
							dR = (int) (dR/255. * R);
							dG = (int) (dG/255. * G);
							dB = (int) (dB/255. * B);
							dA = (int) (dA/255. * A);
							
							if(dA == 0)
								continue;
							
							dRGBA = convertRGBA2Int(dR,dG,dB,dA);
						
							
							if(!doFog) {
								if(dA == 255)
									pixels[index] = dRGBA;
								else if (dA > 0) {
									convertInt2RGBA(pixels[index], &pR,&pG,&pB,&pA);
									
									fr = dA/255.;

									// Colors have to be squared!
									pR = sqrt((1-fr)*pR*pR + fr*dR*dR);
									pG = sqrt((1-fr)*pG*pG + fr*dG*dG);
									pB = sqrt((1-fr)*pB*pB + fr*dB*dB);
									
									pixels[index] = convertRGB2Int((int)(pR),(int)(pG),(int)(pB));	
								}
							}
							else {
								val = contain(0, (far-depth)/(far-near), 1);
								
								if(dA == 1)
									pixels[index] = convertRGB2Int((int)(dR*val),(int)(dG*val),(int)(dB*val));
								else {
									convertInt2RGBA(pixels[index], &pR,&pG,&pB,&pA);
									pixels[index] = convertRGB2Int((int)(dR*val),(int)(dG*val),(int)(dB*val));									
								}									
							}
						}
					}
				}
			}
		}
	}
}
static PyObject* pyDrawTriangle(PyObject *self, PyObject *args) {
	double x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3;
	if(!PyArg_ParseTuple(args, "ddddddddddddddd", &x1,&y1,&z1,&u1,&v1,  &x2,&y2,&z2,&u2,&v2,  &x3,&y3,&z3,&u3,&v3))
      return NULL;
  
	drawTriangle0(x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3);		
	Py_RETURN_NONE;
}


static void drawQuad(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4, int tries) {
	drawTriangle(x1,y1,z1,u1,u1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3, tries);
	drawTriangle(x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4,  x1,y1,z1,u1,v1, tries);
}
static void drawQuad0(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4) {
	drawQuad(x1,y1,z1,u1,u1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3, x4,y4,z4,u4,v4, 0);
}
static PyObject* pyDrawQuad(PyObject *self, PyObject *args) {
	double x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4;
	
	if(!PyArg_ParseTuple(args, "dddddddddddddddddddd", &x1,&y1,&z1,&u1,&v1,  &x2,&y2,&z2,&u2,&v2,  &x3,&y3,&z3,&u3,&v3,  &x4,&y4,&z4,&u4,&v4))
      return NULL;
  
	drawQuad0(x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4);
	Py_RETURN_NONE;
}

static void setRGB(int r, int g, int b) {
	RGBA = convertRGB2Int(r,g,b);
	R = r;
	G = g;
	B = b;
	A = 255;
}
static PyObject* pySetRGB(PyObject *self, PyObject *args) {
	int r,g,b;
	if(!PyArg_ParseTuple(args, "iii", &r,&g,&b))
      return NULL;
  
	setRGB(r,g,b);
	Py_RETURN_NONE;
}


static void setRGBA(int r, int g, int b, int a) {
	RGBA = convertRGBA2Int(r,g,b,a);
	R = r;
	G = g;
	B = b;
	A = a;
}
static PyObject* pySetRGBA(PyObject *self, PyObject *args) {
	int r,g,b,a;
	if(!PyArg_ParseTuple(args, "iiii", &r,&g,&b,&a))
      return NULL;
  
	setRGBA(r,g,b,a);
	Py_RETURN_NONE;
}


static PyObject* pyGetXY(PyObject *self, PyObject *args) {
	int x,y;
	
	if(!PyArg_ParseTuple(args, "ii", &x,&y))
      return NULL;
  
	int index = y*RESOLUTION_WIDTH + x;
	
	int r,g,b,a;
	convertInt2RGBA(pixels[index], &r,&g,&b,&a);	
	return Py_BuildValue("iii",r,g,b);
}


static void drawPolygon(double x,double y,double z, double r, int n) {
	int i;
	double d, xi,yi, xf,yf;
	
	for(i = 0; i < n; i++) {
		xi = xf;
		yi = yf;
		
		d = i*360./(n-1);
		xf = x + r*cosd(d);
		yf = y - r*sind(d);

		if(i > 0)
			drawTriangle0(xi,yi,z,0,0, xf,yf,z,0,0, x,y,z,0,0);
	}
}
static PyObject* pyDrawPolygon(PyObject *self, PyObject *args) {
	double x,y,z,r;
	int n;
	if(!PyArg_ParseTuple(args, "ddddi", &x,&y,&z,&r,&n))
      return NULL;
  
	drawPolygon(x,y,z,r,n);
	Py_RETURN_NONE;
}

static void draw3dFloor(double x1, double y1, double x2, double y2, double z) {
	drawQuad0(x1,y1,z,0,0,  x2,y1,z,1,0,  x2,y2,z,1,1,  x1,y2,z,0,1);
}
static PyObject* pyDraw3dFloor(PyObject *self, PyObject *args) {
	double x1,y1,x2,y2,z;
	if(!PyArg_ParseTuple(args, "ddddd", &x1,&y1,&x2,&y2,&z))
      return NULL;
  
	draw3dFloor(x1,y1,x2,y2,z);
	Py_RETURN_NONE;
}

static void draw3dWall(double x1, double y1, double z1, double x2, double y2, double z2) {
	drawQuad0(x1,y1,z1,0,0,  x2,y2,z1,1,0,  x2,y2,z2,1,1,  x1,y1,z2,0,1);
}
static PyObject* pyDraw3dWall(PyObject *self, PyObject *args) {
	double x1,y1,z1, x2,y2,z2;
	if(!PyArg_ParseTuple(args, "dddddd", &x1,&y1,&z1, &x2,&y2,&z2))
      return NULL;
  
	draw3dWall(x1,y1,z1, x2,y2,z2);
	Py_RETURN_NONE;
}

					
static void compileMats(void) {
	setMatIdentity(completeMat);
	multMatMat(completeMat, projMat,		completeMat);
	multMatMat(completeMat, modelviewMat,	completeMat);
	multMatMat(completeMat, transMat,		completeMat);
}
static PyObject* pyCompileMats(PyObject *self) {
	compileMats();
    Py_RETURN_NONE;
}



static PyObject* pyLoadObj(PyObject *self, PyObject *args) {
	char* filename;	
	if(!PyArg_ParseTuple(args, "s", &filename))
      return NULL;

	// Load obj & print info
	int id = createObj();
	loadObj(filename, id);
	printf("Loaded: %i\n", id);
	return Py_BuildValue("i", id);
}



static void drawObj(obj* o) {	
	int
		*faces = o->faces,
		f,
		v1, v2, v3,
		vt1, vt2, vt3,
	    fNum = o->fNum,
		mNum = o->mNum,
		vNum = o->vNum,
		uvNum = o->uvNum;
	double
		*vertices = o->vertices,
		*uvs = o->uvs;
	mtl *currentMtl;
	
	// Backup drawing color for later
	int 
		tRGBA = RGBA,
		tR = R,
		tG = G,
		tB = B,
		tA = A;
				
	// Loop through Faces
	for(f = 0; f < fNum; f++) {	

		// Get vertices & uvs
		v1 = faces[9*f];
		vt1 = faces[9*f+1];		
		v2 = faces[9*f+3];
		vt2 = faces[9*f+4];		
		v3 = faces[9*f+6];		
		vt3 = faces[9*f+7];
				
		// If v1 is -1, then v2 is a material index
		if(v1 == -1) {
			if(v2 != -1) {
				
				// Set current material
				currentMtl = o->mtls[v2];

				// Set material color
				R = (int) (tR * currentMtl->kd[0]);
				G = (int) (tG * currentMtl->kd[1]);
				B = (int) (tB * currentMtl->kd[2]);
				A = tA;
				
				// Set texture
				setTexture(currentMtl->map_Kd, currentMtl->map_Kd_width, currentMtl->map_Kd_height);
			}
		}
		else
			// Draw triangle btwn vertices
			drawTriangle0(
				vertices[3*v1],vertices[3*v1+1],vertices[3*v1+2],	uvs[2*vt1],uvs[2*vt1+1],
				vertices[3*v2],vertices[3*v2+1],vertices[3*v2+2],	uvs[2*vt2],uvs[2*vt2+1],
				vertices[3*v3],vertices[3*v3+1],vertices[3*v3+2],	uvs[2*vt3],uvs[2*vt3+1]);
	}

	// Revert drawing color back to previous
	RGBA = tRGBA;
	R = tR;
	G = tG;
	B = tB;
	A = tA;		
}
static PyObject* pyDrawObj(PyObject *self, PyObject *args) {
	int id;
	if(!PyArg_ParseTuple(args, "i", &id))
      return NULL;
  
	drawObj(getObj(id));
	Py_RETURN_NONE;
}

		
		
/******************************  CREATE PYTHON METHODS *************************************/

static PyMethodDef canv3d_funcs[47] = {
	{"setMatIdentity", (PyCFunction) pySetMatIdentity, METH_VARARGS, NULL },
	{"setMatTranslation", (PyCFunction) pySetMatTranslation, METH_VARARGS, NULL },
	{"addMatTranslation", (PyCFunction) pyAddMatTranslation, METH_VARARGS, NULL },
	{"setMatScale", (PyCFunction) pySetMatScale, METH_VARARGS, NULL },
	{"addMatScale", (PyCFunction) pyAddMatScale, METH_VARARGS, NULL },
	{"setMatRotationX", (PyCFunction) pySetMatRotationX, METH_VARARGS, NULL },
	{"addMatRotationX", (PyCFunction) pyAddMatRotationX, METH_VARARGS, NULL },
	{"setMatRotationY", (PyCFunction) pySetMatRotationY, METH_VARARGS, NULL },
	{"addMatRotationY", (PyCFunction) pyAddMatRotationY, METH_VARARGS, NULL },
	{"setMatRotationZ", (PyCFunction) pySetMatRotationZ, METH_VARARGS, NULL },
	{"addMatRotationZ", (PyCFunction) pyAddMatRotationZ, METH_VARARGS, NULL },

	{"setMatPerspective", (PyCFunction) pySetMatPerspective, METH_VARARGS, NULL },
	{"addMatPerspective", (PyCFunction) pyAddMatPerspective, METH_VARARGS, NULL },
	{"setMatLook", (PyCFunction) pySetMatLook, METH_VARARGS, NULL },
	{"setMatAntiLook", (PyCFunction) pySetMatAntiLook, METH_VARARGS, NULL },
	{"addMatLook", (PyCFunction) pyAddMatLook, METH_VARARGS, NULL },
	{"addMatAntiLook", (PyCFunction) pyAddMatAntiLook, METH_VARARGS, NULL },

	{"loadObj", (PyCFunction) pyLoadObj, METH_VARARGS, NULL},
	{"drawObj", (PyCFunction) pyDrawObj, METH_VARARGS, NULL},

	{"init", (PyCFunction) pyInit, METH_VARARGS, NULL },
	{"setTexture", (PyCFunction) pySetTexture, METH_VARARGS, NULL },
	{"unsetTexture", (PyCFunction) pyUnsetTexture, METH_NOARGS, NULL },
	{"drawTriangle", (PyCFunction) pyDrawTriangle, METH_VARARGS, NULL },
	{"drawQuad", (PyCFunction) pyDrawQuad, METH_VARARGS, NULL },
	{"drawPolygon", (PyCFunction) pyDrawPolygon, METH_VARARGS, NULL },
	{"draw3dWall", (PyCFunction) pyDraw3dWall, METH_VARARGS, NULL },
	{"draw3dFloor", (PyCFunction) pyDraw3dFloor, METH_VARARGS, NULL },
	{"compileMats", (PyCFunction) pyCompileMats, METH_NOARGS, NULL },
	{"clear", (PyCFunction) pyClear, METH_NOARGS, NULL },
	{"setRGB", (PyCFunction) pySetRGB, METH_VARARGS, NULL },
	{"setRGBA", (PyCFunction) pySetRGBA, METH_VARARGS, NULL },
	{"getXY", (PyCFunction) pyGetXY, METH_VARARGS, NULL },
	
	{"camera", (PyCFunction) pyCamera, METH_VARARGS, NULL},
	{"turn", (PyCFunction) pyTurn, METH_VARARGS, NULL},
	{"rotateVecAboutAxis", (PyCFunction) pyRotateVecAboutAxis, METH_VARARGS, NULL},
	{"setMatCamera", (PyCFunction) pySetMatCamera, METH_VARARGS, NULL},
	{"addMatCamera", (PyCFunction) pyAddMatCamera, METH_VARARGS, NULL},
	{"setMatCameraPosition", (PyCFunction) pySetMatCameraPosition, METH_VARARGS, NULL},
	{"addMatCameraPosition", (PyCFunction) pyAddMatCameraPosition, METH_VARARGS, NULL},
	{"setMatCameraRotation", (PyCFunction) pySetMatCameraRotation, METH_VARARGS, NULL},
	{"addMatCameraRotation", (PyCFunction) pyAddMatCameraRotation, METH_VARARGS, NULL},

	{"setMatCameraAntiRotation", (PyCFunction) pySetMatCameraAntiRotation, METH_VARARGS, NULL},
	{"addMatCameraAntiRotation", (PyCFunction) pyAddMatCameraAntiRotation, METH_VARARGS, NULL},

    {NULL}
};

void initcanv3d(void) {
	import_array();
    Py_InitModule3("canv3d", canv3d_funcs, "Extension module example!");
}