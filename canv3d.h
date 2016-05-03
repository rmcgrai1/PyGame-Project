// http://www.tutorialspoint.com/python/python_further_extensions.htm

#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include "hashmap.h"

#include "linalg.h"

static void setRGB(int r, int g, int b);

/************************** VARIOUS MATH FUNCTIONS ************************************/

static double epoch();
	
static double contain(double mi, double x, double ma);

/******************************* RGBA INT FUNCTIONS ************************************/

static int convertRGBA2Int(int r, int g, int b, int a) ;
static int convertRGB2Int(int r, int g, int b);
static void convertInt2RGBA(int argb, int *r, int *g, int *b, int *a);


/*********************************** OBJ LOADING ************************************/

static obj* getObj(int id);
	
/***************************** LINEAR ALGEBRA FUNCTIONS **********************************/

static double cosd(double deg);
static double sind(double deg);
static double tand(double deg);


double calculateLength(double* vec4);

static double* getMat(int matType);

static PyObject* pySetMatIdentity(PyObject *self, PyObject *args);

static double* setMatTranslation(double* mat, double x, double y, double z);

static PyObject* pySetMatTranslation(PyObject *self, PyObject *args);

static double* addMatTranslation(double* mat, double x, double y, double z);

static PyObject* pyAddMatTranslation(PyObject *self, PyObject *args);
	
static double* setMatScale(double* mat, double sx, double sy, double sz);

static PyObject* pySetMatScale(PyObject *self, PyObject *args);

static double* addMatScale(double* mat, double sx, double sy, double sz);

static PyObject* pyAddMatScale(PyObject *self, PyObject *args);
	
static double* setMatRotationX(double* mat, double degX);

static PyObject* pySetMatRotationX(PyObject *self, PyObject *args);

static double* addMatRotationX(double* mat, double degX);

static PyObject* pyAddMatRotationX(PyObject *self, PyObject *args);
	
static double* setMatRotationY(double* mat, double degY);

static PyObject* pySetMatRotationY(PyObject *self, PyObject *args);

static double* addMatRotationY(double* mat, double degY);

static PyObject* pyAddMatRotationY(PyObject *self, PyObject *args);
	
static double* setMatRotationZ(double* mat, double degZ);

static PyObject* pySetMatRotationZ(PyObject *self, PyObject *args);

static double* addMatRotationZ(double* mat, double degZ);

static PyObject* pyAddMatRotationZ(PyObject *self, PyObject *args);
	
static double* setMatPerspective(double *mat, double fov);

static PyObject* pySetMatPerspective(PyObject *self, PyObject *args);

static double* addMatPerspective(double *mat, double fov);

static PyObject* pyAddMatPerspective(PyObject *self, PyObject *args);

double magnitude(double* vec, int length);

double * normalizeModify(double* vec, int length);

double * normalizeCopy(double* vecSource, double* vecDest, int length);

double* subtractVecCopy(double *vec1, double *vec2, double* vecDest, int length);

double* crossVec3Copy(double *u, double *v, double* vecDest);

//dot product
double dot(double *u, double *v, int length);
	
static double* setMatLook(double *mat, double x,double y,double z, double nx,double ny,double nz, double upx,double upy,double upz);

static PyObject* pySetMatLook(PyObject *self, PyObject *args);

//axis is an array of length 3
//angle is in degrees
static double* rotateAboutAxis(double *mat, double angle, const double* axis);

double* mat4MultVec3(double *m, double *v, double* destVec);

//deltaX and deltaY are in degrees
static void cameraTurn(double deltaX, double deltaY);

static PyObject* pyCameraTurn(PyObject *self, PyObject *args);

//distance is in...pixels?
static void cameraForwards(double distance);

static PyObject* pyCameraForwards(PyObject *self, PyObject *args);

static double* setMatCamera(double* mat);

static PyObject* pySetMatCamera(PyObject *self, PyObject *args);

static PyObject* pyAddMatCamera(PyObject *self, PyObject *args);

static double* setMatCameraPosition(double *mat);

static PyObject* pySetMatCameraPosition(PyObject *self, PyObject *args);

static void init(int resW, int resH, double n, double f, int dFog, int* pixs);

static PyObject* pyInit(PyObject *self, PyObject *args);

static void setTexture(int* texPixs, int w, int h);

static PyObject* pySetTexture(PyObject *self, PyObject *args);

static void clear();

static PyObject* pyClear(PyObject *self);

static void clearStatic(self);

static PyObject* pyClearStatic(PyObject *self);

static void drawTriangle0(double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3);
static void drawTriangle(double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3, int tries);
static void drawQuad0(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4);
static void drawQuad(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4, int tries);

static void clipTriangle(double x1,double y1,double z1,double u1,double v1,double w1,	double x2,double y2,double z2,double u2,double v2,double w2,  double x3,double y3,double z3,double u3,double v3, double w3);

static void clipQuad(double x1,double y1,double z1,double u1,double v1,double w1,	double x2,double y2,double z2,double u2,double v2,double w2,  double x3,double y3,double z3,double u3,double v3, double w3);

static void clip(double x1,double y1,double z1,double u1,double v1,double w1,  double x2,double y2,double z2,double u2,double v2,double w2,  double x3,double y3,double z3,double u3,double v3,double w3);

static PyObject* pyDrawTriangle(PyObject *self, PyObject *args);

static void drawQuad0(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4);

static PyObject* pyDrawQuad(PyObject *self, PyObject *args);

static void setRGB(int r, int g, int b);

static PyObject* pySetRGB(PyObject *self, PyObject *args);

static PyObject* pyGetXY(PyObject *self, PyObject *args);

static void drawPolygon(double x, double y, double r, int n);

static void draw3dFloor(double x1, double y1, double x2, double y2, double z);

static PyObject* pyDraw3dFloor(PyObject *self, PyObject *args);

static void draw3dWall(double x1, double y1, double z1, double x2, double y2, double z2);

static PyObject* pyDraw3dWall(PyObject *self, PyObject *args);
					
static void compileMats();

static PyObject* pyCompileMats(PyObject *self);

static int createObj();

static mtl** loadMtl(char* filename);

static void loadObj(char* filename, int id);

static PyObject* pyLoadObj(PyObject *self, PyObject *args);

static void drawObj(obj* o);

static PyObject* pyDrawObj(PyObject *self, PyObject *args);

static double timer;

static PyObject* pyTest(PyObject *self, PyObject *args);
		
////////////////////////////////////////////////////////////////////////////////////////

void initcanv3d(void);

////////////////////////////////////////////////////////////////////////////////////////
