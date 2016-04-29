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

#define MAT_MODEL		0
#define MAT_VIEW		1
#define MAT_PROJECTION 	2

static double
	near = .1,
	far = 300,
	aspect,

	tempVert1[4] = 	{0,0,0,1},
	tempVert2[4] = 	{0,0,0,1},
	tempVert3[4] = 	{0,0,0,1},
	viewMat[16] = 	{1,0,0,0, 
					 0,1,0,0,	
					 0,0,1,0, 
					 0,0,0,1},
	projMat[16] = 	{1,0,0,0, 
					 0,1,0,0,
					 0,0,1,0, 
					 0,0,0,1},
	modelMat[16] = 	{1,0,0,0,
					 0,1,0,0, 
					 0,0,1,0, 
					 0,0,0,1},
	completeMat[16] = 	{1,0,0,0, 
						 0,1,0,0, 
						 0,0,1,0,
						 0,0,0,1};
static int 
	doFog = 0,
	doDepthTest = 1,
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


/************************** VARIOUS MATH FUNCTIONS ************************************/

static double epoch() {
	return time(NULL);
}	
	
static double contain(double mi, double x, double ma) {
	return (x < mi) ? mi : ((x > ma) ? ma : x);
}




/******************************* RGBA INT FUNCTIONS ************************************/

static int convertRGBA2Int(int r, int g, int b, int a) {
	return (a&0x0ff) << 24 | (r&0x0ff) << 16 | (g&0x0ff) << 8 | (b&0x0ff);
}
static int convertRGB2Int(int r, int g, int b) {
	return (255&0x0ff) << 24 | (r&0x0ff) << 16 | (g&0x0ff) << 8 | (b&0x0ff);
}

static void convertInt2RGBA(int argb, int *r, int *g, int *b, int *a) {
	*r = (argb>>16) & 0xFF;
	*g = (argb>>8) & 0xFF;
	*b = (argb) & 0xFF;
	*a = (argb>>24) & 0xFF;
}



/*********************************** OBJ LOADING ************************************/

typedef struct mtl {
	double ns;
	double* ka;
	double* kd;
	double* ks;
	double ni;
	double d;
} mtl;

typedef struct obj {
	int vNum;
	double* vertices;
	int uvNum;
	double* uvs;	
	int nNum;
	double* normals;
	int fNum;
	int* faces;
	
	mtl **mtls;
} obj;

static obj **modelArray;
int modelNum = 0;

static obj* getObj(int id) {
	return modelArray[id];
}


	
/***************************** LINEAR ALGEBRA FUNCTIONS **********************************/

static double cosd(double deg) {return cos(deg * D2R);}
static double sind(double deg) {return sin(deg * D2R);}
static double tand(double deg) {return tan(deg * D2R);}



double calculateLength(double* vec4) {
	return sqrt(vec4[0]*vec4[0] + vec4[1]*vec4[1] + vec4[2]*vec4[2] + vec4[3]*vec4[3]);
}

static double* getMat(int matType) {
	switch(matType) {
		case MAT_MODEL:			return modelMat;
		case MAT_VIEW:			return viewMat;
		case MAT_PROJECTION:	return projMat;
		default:				return NULL;
	}
}

static void printVec(double* vec4) {
	printf("<%lf,%lf,%lf,%lf>\n", vec4[0],vec4[1],vec4[2],vec4[3]);
}

static void printMat(double* mat) {
	printf("|%lf,%lf,%lf,%lf|\n", mat[0],mat[1],mat[2],mat[3]);
	printf("|%lf,%lf,%lf,%lf|\n", mat[4],mat[5],mat[6],mat[7]);
	printf("|%lf,%lf,%lf,%lf|\n", mat[8],mat[9],mat[10],mat[11]);
	printf("|%lf,%lf,%lf,%lf|\n", mat[12],mat[13],mat[14],mat[15]);
}


static double* setMatIdentity(double *mat) {
	return set16(mat,  
		1,0,0,0,  
		0,1,0,0,
		0,0,1,0,
		0,0,0,1);
}
static PyObject* pySetMatIdentity(PyObject *self, PyObject *args) {
	int matType;
	if(!PyArg_ParseTuple(args, "i", &matType))
      return NULL;
  
	setMatIdentity(getMat(matType));
	Py_RETURN_NONE;
}



static double* setMatTranslation(double* mat, double x, double y, double z) {
	return set16(mat,  1,0,0,x,  0,1,0,y,  0,0,1,z,  0,0,0,1);
}
static PyObject* pySetMatTranslation(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &x,&y,&z))
      return NULL;
  
	setMatTranslation(getMat(matType), x,y,z);
	Py_RETURN_NONE;
}

static double* addMatTranslation(double* mat, double x, double y, double z) {
	setMatTranslation(tempMatAdd, x,y,z);
	return multMatMat(mat,tempMatAdd, mat);
}
static PyObject* pyAddMatTranslation(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &x,&y,&z))
      return NULL;
  
	addMatTranslation(getMat(matType), x,y,z);
	Py_RETURN_NONE;
}
	
	
	
static double* setMatScale(double* mat, double sx, double sy, double sz) {
	return set16(mat,  sx,0,0,0,  0,sy,0,0,  0,0,sz,0,  0,0,0,1);
}
static PyObject* pySetMatScale(PyObject *self, PyObject *args) {
	int matType;
	double sx,sy,sz;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &sx, &sy, &sz))
      return NULL;
  
	setMatScale(getMat(matType), sx, sy, sz);
	Py_RETURN_NONE;
}

static double* addMatScale(double* mat, double sx, double sy, double sz) {
	setMatScale(tempMatAdd, sx,sy,sz);
	return multMatMat(mat,tempMatAdd, mat);
}
static PyObject* pyAddMatScale(PyObject *self, PyObject *args) {
	int matType;
	double sx,sy,sz;
	if(!PyArg_ParseTuple(args, "iddd", &matType, &sx, &sy, &sz))
      return NULL;
  
	addMatScale(getMat(matType), sx, sy, sz);
	Py_RETURN_NONE;
}

		
	
static double* setMatRotationX(double* mat, double degX) {
	double 
		co = cosd(degX),
		si = sind(degX);
	return set16(mat,  1,0,0,0,  0,co,-si,0,  0,si,co,0,  0,0,0,1);
}
static PyObject* pySetMatRotationX(PyObject *self, PyObject *args) {
	int matType;
	double degX;
	if(!PyArg_ParseTuple(args, "id", &matType, &degX))
      return NULL;
  
	setMatRotationX(getMat(matType), degX);
	Py_RETURN_NONE;
}

static double* addMatRotationX(double* mat, double degX) {
	setMatRotationX(tempMatAdd, degX);
	return multMatMat(mat,tempMatAdd, mat);
}
static PyObject* pyAddMatRotationX(PyObject *self, PyObject *args) {
	int matType;
	double degX;
	if(!PyArg_ParseTuple(args, "id", &matType, &degX))
      return NULL;
  
	addMatRotationX(getMat(matType), degX);
	Py_RETURN_NONE;
}
	
	
	
static double* setMatRotationY(double* mat, double degY) {
	double
		co = cosd(degY),
		si = sind(degY);
	return set16(mat,
		co,0,si,0,
		0,1,0,0,
		-si,0,co,0,
		0,0,0,1);
}
static PyObject* pySetMatRotationY(PyObject *self, PyObject *args) {
	int matType;
	double degY;	
	if(!PyArg_ParseTuple(args, "id", &matType, &degY))
      return NULL;
  
	setMatRotationY(getMat(matType), degY);		
	Py_RETURN_NONE;
}

static double* addMatRotationY(double* mat, double degY) {
	setMatRotationY(tempMatAdd, degY);
	return multMatMat(mat,tempMatAdd, mat);
}	
static PyObject* pyAddMatRotationY(PyObject *self, PyObject *args) {
	int matType;
	double degY;	
	if(!PyArg_ParseTuple(args, "id", &matType, &degY))
      return NULL;
  
	addMatRotationY(getMat(matType), degY);		
	Py_RETURN_NONE;
}
	
	
	
static double* setMatRotationZ(double* mat, double degZ) {
	double
		co = cosd(degZ),
		si = sind(degZ);
	return set16(mat,
		co,si,0,0,  
		-si,co,0,0,  
		0,0,1,0,  
		0,0,0,1);
}
static PyObject* pySetMatRotationZ(PyObject *self, PyObject *args) {
	int matType;
	double degZ;
	if(!PyArg_ParseTuple(args, "id", &matType, &degZ))
      return NULL;
  
	setMatRotationZ(getMat(matType), degZ);
	Py_RETURN_NONE;
}

static double* addMatRotationZ(double* mat, double degZ) {
	setMatRotationZ(tempMatAdd, degZ);
	return multMatMat(mat,tempMatAdd, mat);
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
	
	fov = .5;
	double ys = 1. / tand(fov/2.);
	double xs = ys*aspect;
	
	/*set16(mat,
		xscale,0,0,0,  
		0,yscale,0,0, 
		0,0,(f+n)/(n-f),-1,
		0,0,2*f*n/(n-f),0)
	*/
	
	/*set16(mat,
		xs,0,0,0,
		0,ys,0,0,
		0,0,(far+near)/(near-far),2*far*near/(near-far),
		0,0,-1,0);*/
	set16(mat,
		xs,0,0,0,
		0,ys,0,0,
		0,0,(far+near)/(near-far),2*far*near/(near-far),
		0,0,-1,0);
		
	/*set16(mat,
		3.07292, 0.0, 0.0, 0.0, 
		0.0, 4.5107083, 0.0, 0.0,
		0.0, 0.0, -1.0100503, -1.0,
		0.0, 0.0, -1.0050251, 0.0);*/
		
	//transpose(mat);
	//printf("\n");
	
	return mat;	
	/*return set16(mat,
		sc,0,0,0,
		0,sc,0,0,
		0,0,(far+near)/(near-far),-1,
		0,0,2*far*near/(near-far),0);*/
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

	
static double* setMatLook(double *mat, double x,double y,double z, double nx,double ny,double nz, double upx,double upy,double upz) {
	double 
		sx = ny*upz - upy*nz,
		sy = -nx*upz + upx*nz,
		sz = nx*upy - upx*ny,
		l = sqrt(sx*sx + sy*sy + sz*sz);
	sx /= l;
	sy /= l;
	sz /= l;

	upx = sy*nz - ny*sz;
	upy = -sx*nz + nx*sz;
	upz = sx*ny - nx*sy;

	set16(mat, 
		sx,upx,-nx,0,
		sy,upy,-ny,0,
		sz,upz,-nz,0,
		0,0,0,1);
	return transpose(mat);
	/*return set16(mat, 
		sx,sy,sz,0,
		upx,upy,upz,0,
		-nx,-ny,-nz,0,
		0,0,0,1);*/
}
static PyObject* pySetMatLook(PyObject *self, PyObject *args) {
	int matType;
	double x,y,z, nx,ny,nz, upx,upy,upz;
	if(!PyArg_ParseTuple(args, "idddd", &matType, &x,&y,&z, &nx,&ny,&nz, &upx,&upy,&upz))
      return NULL;
  
	setMatLook(getMat(matType), x,y,z, nx,ny,nz, upx,upy,upz);		
	Py_RETURN_NONE;
}
	


static void init(int resW, int resH, double n, double f, int dFog, int* pixs) {
	RESOLUTION_WIDTH = resW;
	RESOLUTION_HEIGHT = resH;
	PIXEL_NUMBER = resW*resH;
	
	srand(time(NULL));
	
	aspect = 1. * resW / resH;
	
	near = n;
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
	if(!PyArg_ParseTuple(args, "iiddiO!", &resW,&resH,&n,&f,&doFog, &PyArray_Type,&arrayin)) {
	    return NULL;
	}
  
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


static void clear() {
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

static void clearStatic(self) {
	int i, val;
	for(i = 0; i < PIXEL_NUMBER; i++) {
		val = rand() % 255;
		
		pixels[i] = convertRGB2Int(val,val,val);
		depths[i] = near;
	}
}
static PyObject* pyClearStatic(PyObject *self) {  
	clearStatic();
	Py_RETURN_NONE;
}


	
static void drawTriangle(double x1,double y1,double z1,double u1,double v1,  double x2,double y2,double z2,double u2,double v2,  double x3,double y3,double z3,double u3,double v3) {
	//printf("> drawTriangle()\n");

	set4(tempVert1, x1,y1,z1,1);
	set4(tempVert2, x2,y2,z2,1);
	set4(tempVert3, x3,y3,z3,1);

	multMatVec(completeMat, tempVert1, tempVert1);
	multMatVec(completeMat, tempVert2, tempVert2);
	multMatVec(completeMat, tempVert3, tempVert3);
	
	//printVec(tempVert1);
	//printVec(tempVert2);
	//printVec(tempVert3);
	//printf("\n");
	
	double w1, w2, w3,
		miX, miY, maX, maY,
		x21, x31, y21, y31, z21, z31,
		az, bz, c,
		au, bu,
		av, bv,
		area,
		s, t,
		depth;
		
	int x,y, u,v, miXi,miYi,maXi,maYi;
	double ow1, ow2, ow3;
		
	ow1 = w1 = tempVert1[3];	
	w1 = fabs(w1);
	x1 = tempVert1[0]/-w1;
	y1 = tempVert1[1]/-w1;
	z1 = tempVert1[2]; ///w1;

	ow2 = w2 = tempVert2[3];				
	w2 = fabs(w2);
	x2 = tempVert2[0]/-w2;
	y2 = tempVert2[1]/-w2;
	z2 = tempVert2[2]; ///w2;
	
	ow3 = w3 = tempVert3[3];
	w3 = fabs(w3);
	x3 = tempVert3[0]/-w3;
	y3 = tempVert3[1]/-w3;
	z3 = tempVert3[2]; ///w3;
	
	if((-ow1 < near && -ow2 < near && -ow3 < near) || (-ow1 > far && -ow2 > far && -ow3 > far)) {
		//printf("X drawTriangle()\n");
		return;	
	}
		
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

	az = y21*(z3-z1) - y31*(z2-z1);
	bz = -x21*(z3-z1) + x31*(z2-z1);
	c = x21*y31 - x31*y21;
	
	au = y21*(u3-u1) - y31*(u2-u1);
	bu = -x21*(u3-u1) + x31*(u2-u1);
	av = y21*(v3-v1) - y31*(v2-v1);
	bv = -x21*(v3-v1) + x31*(v2-v1);

	area = .5*(-y2*x3 + y1*(-x2+x3) + x1*(y2-y3) + x2*y3);
	
	if(area == 0)
		return;

	
	//v0 = 2-1
	//v1 = 3-1/
	//v2 = p - 1
	
    double d00, d01, d11, d20, d21;
	double b1, b2, b3;
	
	double x01,y01,z01;
	
	d00 = x21*x21 + y21*y21 + z21*z21;
	d01 = x21*x31 + y21*y31 + z21*z31;
	d11 = x31*x31 + y31*y31 + z31*z31;

	double denom = d00 * d11 - d01 * d01;

	int index, dRGBA, dR, dG, dB, dA;
	double val = 1, wp, up, vp;						
	for(x = miXi; x < maXi; x++) {
		for(y = miYi; y < maYi; y++) {
			s = 1/(2*area)*(y1*x3 - x1*y3 + y31*x - x31*y);
			t = 1/(2*area)*(x1*y2 - y1*x2 - y21*x + x21*y);
			
			if(0 <= s && s <= 1 && 0 <= t && t <= 1 && s+t <= 1) {
				depth = (z1 + (az*(x-x1) + bz*(y-y1))/-c);
			
				x01 = x-x1;
				y01 = y-y1;
				z01 = depth-z1;
									
				d20 = x01*x21 + y01*y21 + z01*z21;
				d21 = x01*x31 + y01*y31 + z01*z31;

				b2 = (d11 * d20 - d01 * d21) / denom;
				b3 = (d00 * d21 - d01 * d20) / denom;
				b1 = 1. - b3 - b2;
								
				if(!doDepthTest || (depth >= near && depth <= far)) {
					index = y*RESOLUTION_WIDTH + x;

					if(!doDepthTest || (depth < depths[index])) {
						depths[index] = depth;
						
						if(texture == NULL) {
							if(!doFog)
								pixels[index] = RGBA;
							else {
								val = contain(0, (far-depth)/(far-near), 1);
								pixels[index] = convertRGB2Int((int)(R*val),(int)(G*val),(int)(B*val));
							}
						}
						else {
							/*wp = ( 1 / w1 ) * b1 + ( 1 / w2 ) * b2 + ( 1 / w3 ) * b3;
							up = ( u1 / w1 ) * b1 + ( u2 / w2 ) * b2 + ( u3 / w3 ) * b3;
							vp = ( v1 / w1 ) * b1 + ( v2 / w2 ) * b2 + ( v3 / w3 ) * b3;
							
							u = (int)(textureWidth * up / wp);
							v = (int)(textureHeight * vp / wp);*/
							
							up = u1 * b1 + u2 * b2 + u3 * b3;
							vp = v1 * b1 + v2 * b2 + v3 * b3;
							
							u = (int)(textureWidth * up);
							v = (int)(textureHeight * vp);
						
						
							//printf("%d, %d\n", u, v);
						
							if(u >= 0 && u < textureWidth && v >= 0 && v < textureHeight) {
								dRGBA = texture[textureHeight*v + u];
								convertInt2RGBA(dRGBA, &dR,&dG,&dB,&dA);
								
								dR = (int) (dR/255. * R);
								dG = (int) (dG/255. * G);
								dB = (int) (dB/255. * B);
								dA = (int) (dA/255. * A);
								
								dRGBA = convertRGBA2Int(dR,dG,dB,dA);
							}
							
							if(!doFog)
								pixels[index] = dRGBA;
							else {
								val = contain(0, (far-depth)/(far-near), 1);
								pixels[index] = convertRGB2Int((int)(dR*val),(int)(dG*val),(int)(dB*val));
							}
						}
					}
				}
			}
		}
	}
	
	//printf("< drawTriangle()\n");
}
static PyObject* pyDrawTriangle(PyObject *self, PyObject *args) {
	double x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3;
	
	if(!PyArg_ParseTuple(args, "ddddddddddddddd", &x1,&y1,&z1,&u1,&v1,  &x2,&y2,&z2,&u2,&v2,  &x3,&y3,&z3,&u3,&v3))
      return NULL;
  
	drawTriangle(x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3);		
	Py_RETURN_NONE;
}



static void drawQuad(double x1,double y1,double z1,double u1,double v1,	double x2,double y2,double z2,double u2,double v2,	double x3,double y3,double z3,double u3,double v3,	double x4,double y4,double z4,double u4,double v4) {
	drawTriangle(x1,y1,z1,u1,u1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3);
	drawTriangle(x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4,  x1,y1,z1,u1,v1);
}
static PyObject* pyDrawQuad(PyObject *self, PyObject *args) {
	double x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4;
	
	if(!PyArg_ParseTuple(args, "dddddddddddddddddddd", &x1,&y1,&z1,&u1,&v1,  &x2,&y2,&z2,&u2,&v2,  &x3,&y3,&z3,&u3,&v3,  &x4,&y4,&z4,&u4,&v4))
      return NULL;
  
	drawQuad(x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4);
	Py_RETURN_NONE;
}


static PyObject* pySetRGB(PyObject *self, PyObject *args) {
	int r,g,b;
	if(!PyArg_ParseTuple(args, "iii", &r,&g,&b))
      return NULL;
  
	RGBA = convertRGB2Int(r,g,b);
	R = r;
	G = g;
	B = b;
	A = 255;
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


static void drawPolygon(double x, double y, double r, int n) {
	int i;
	double d, xi,yi, xf,yf;
	
	for(i = 0; i < n; i++) {
		xi = xf;
		yi = yf;
		
		d = i*360./(n-1);
		xf = x + r*cosd(d);
		yf = y - r*sind(d);

		if(i > 0)
			drawTriangle(xi,yi,1,0,0, xf,yf,1,0,0, x,y,1,0,0);
	}
}

static void draw3dFloor(double x1, double y1, double x2, double y2, double z) {
	drawQuad(x1,y1,z,0,0,  x2,y1,z,1,0,  x2,y2,z,1,1,  x1,y2,z,0,1);
}
static PyObject* pyDraw3dFloor(PyObject *self, PyObject *args) {
	double x1,y1,x2,y2,z;
	if(!PyArg_ParseTuple(args, "ddddd", &x1,&y1,&x2,&y2,&z))
      return NULL;
  
	draw3dFloor(x1,y1,x2,y2,z);
	Py_RETURN_NONE;
}

static void draw3dWall(double x1, double y1, double z1, double x2, double y2, double z2) {
	drawQuad(x1,y1,z1,0,0,  x2,y2,z1,1,0,  x2,y2,z2,1,1,  x1,y1,z2,0,1);
}
static PyObject* pyDraw3dWall(PyObject *self, PyObject *args) {
	double x1,y1,z1, x2,y2,z2;
	if(!PyArg_ParseTuple(args, "dddddd", &x1,&y1,&z1, &x2,&y2,&z2))
      return NULL;
  
	draw3dWall(x1,y1,z1, x2,y2,z2);
	Py_RETURN_NONE;
}

					
static void compileMats() {
	setMatIdentity(completeMat);
	multMatMat(completeMat, projMat,	completeMat);
	multMatMat(completeMat, viewMat,	completeMat);
	multMatMat(completeMat, modelMat,	completeMat);
}
static PyObject* pyCompileMats(PyObject *self) {
	compileMats();
    Py_RETURN_NONE;
}


static int createObj() {
	int id = modelNum++;
	
	obj** oldModelArray = modelArray;
	modelArray = (obj**) malloc(modelNum * sizeof(obj*));
	
	int i;
	for(i = 0; i < modelNum-1; i++)
		modelArray[i] = oldModelArray[i];
	
	modelArray[id] = (obj*) malloc(sizeof(obj));
	
	if(id > 0)
		free(oldModelArray);
	
	return id;
}

static mtl** loadMtl(char* filename) {
	
}

static void loadObj(char* filename, int id) {	
	obj* o = modelArray[id];
	
	FILE *fp;
	char lines[200][200], line[200], *type, *substr, c, cc[2];
	size_t len = 0;
	ssize_t read;
	int l = 0, lNum = 0;
	
	if((fp = fopen(filename, "r")) == NULL)
		return;
	
	cc[1] = '\0';
	
	lines[0][0] = '\0';
	
	// Load file into string array
	while(!feof(fp)) {
		cc[0] = fgetc(fp);
		
		if(cc[0] != '\n')
			strcat(lines[lNum], cc);
		else
			lines[++lNum][0] = '\0';
	}
	lNum--;
	
	fclose(fp);

	int i, vNum = 0, vnNum = 0, vtNum = 0, fNum = 0;
	// Loop through File Once to Get # of each
	for(l = 0; l < lNum; l++) {
		strcpy(line, lines[l]);	

		type = strtok(line, " ");
		
		if(!strcmp(type,"v"))
			vNum++;
		else if(!strcmp(type, "f") || !strcmp(type, "usemtl"))
			fNum++;
	}

	int
		ii, f = 0, v = 0,
		*faces = (int*) malloc(9 * fNum * sizeof(int));
	double
		*vertices = (double*) malloc(3 * vNum * sizeof(double));
	
	mtl* m;
	
	// Loop through File Second Time
	for(l = 0; l < lNum; l++) {
		strcpy(line, lines[l]);	
		type = strtok(line, " ");
				
		if(!strcmp(type,"v")) {
			for(i = 0; i < 3; i++) {
				substr = strtok(NULL , " ");
				vertices[3*v + i] = atof(substr);
			}
			v++;
		}
		else if(!strcmp(type, "usemtl")) {
			//m = 
		}
		else if(!strcmp(type, "f")) {
			for(ii = 0; ii < 3; ii++) {
				for(i = 0; i < 3; i++) {
					substr = strtok(NULL , (i<2)?"/":" ");
					faces[9*f + 3*ii + i] = atoi(substr);
				}
			}
			f++;
		}
	}
		
	
	o->vNum = vNum;
	o->fNum = fNum;
	o->faces = faces;
	o->vertices = vertices;
	//o->mtls = mtls;
}
static PyObject* pyLoadObj(PyObject *self, PyObject *args) {
	char* filename;
	
	if(!PyArg_ParseTuple(args, "s", &filename))
      return NULL;

	int id = createObj();
	loadObj(filename, id);
	return Py_BuildValue("i", id);
}



static void drawObj(obj* o) {	
	int
		*faces = o->faces,
		f,
		v1, v2, v3,
		fNum = o->fNum;
	double
		*vertices = o->vertices;
	mtl *currentMtl;
	
	int 
		tRGBA = RGBA,
		tR = R,
		tG = G,
		tB = B,
		tA = A;
		
	// Loop through Faces
	for(f = 0; f < fNum; f++) {	
		// Get vertices
		v1 = o->faces[9*f];
		v2 = o->faces[9*f+3];
		v3 = o->faces[9*f+6];
		
		if(v1 == -1) {
			currentMtl = o->mtls[v2];
			R = (int) (255 * currentMtl->kd[0]);
			G = (int) (255 * currentMtl->kd[1]);
			B = (int) (255 * currentMtl->kd[2]);
		}
		else {	
			// Draw triangle btwn vertices
			drawTriangle(
				vertices[3*v1],vertices[3*v1+1],vertices[3*v1+2],0,0,
				vertices[3*v2],vertices[3*v2+1],vertices[3*v2+2],0,0,
				vertices[3*v3],vertices[3*v3+1],vertices[3*v3+2],0,0);
		}
	}
	
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

	

static double timer;
static PyObject* pyTest(PyObject *self, PyObject *args) {
	PyArrayObject *arrayin;
	
	if(!PyArg_ParseTuple(args, "O!", &PyArray_Type,&arrayin)) {
		printf("FAILED TO PARSE!\n");
	    return NULL;
	}    
	//init(resW,resH,n,f,doFog, (int*) (pixs->data));
	Py_RETURN_NONE;


	/*setMatIdentity(modelMat);
	//setMatIdentity(viewMat);
	//setMatIdentity(projMat);
	setMatIdentity(completeMat);
	clear();
	
	addMatTranslation(modelMat, 200,100,-30);
	addMatTranslation(modelMat, 0,20*cosd(10*(timer++)),0);
	addMatRotationZ(modelMat, 20*cosd(8*(timer++)));
	
	compileArrays();
	
	drawPolygon(0,0, 100, 10, 0);*/
	
    //Py_RETURN_NONE;
}		
		
////////////////////////////////////////////////////////////////////////////////////////

static PyMethodDef canv3d_funcs[29] = {
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

	{"loadObj", (PyCFunction) pyLoadObj, METH_VARARGS, NULL},
	{"drawObj", (PyCFunction) pyDrawObj, METH_VARARGS, NULL},

	{"init", (PyCFunction) pyInit, METH_VARARGS, NULL },
	{"setTexture", (PyCFunction) pySetTexture, METH_VARARGS, NULL },
	{"drawTriangle", (PyCFunction) pyDrawTriangle, METH_VARARGS, NULL },
	{"drawQuad", (PyCFunction) pyDrawQuad, METH_VARARGS, NULL },
	{"draw3dWall", (PyCFunction) pyDraw3dWall, METH_VARARGS, NULL },
	{"draw3dFloor", (PyCFunction) pyDraw3dFloor, METH_VARARGS, NULL },
	{"compileMats", (PyCFunction) pyCompileMats, METH_NOARGS, NULL },
	{"clear", (PyCFunction) pyClear, METH_NOARGS, NULL },
	{"clearStatic", (PyCFunction) pyClearStatic, METH_NOARGS, NULL },
	{"setRGB", (PyCFunction) pySetRGB, METH_VARARGS, NULL },
	{"getXY", (PyCFunction) pyGetXY, METH_VARARGS, NULL },

	{"test", (PyCFunction) pyTest, METH_VARARGS, NULL },

    {NULL}
};

void initcanv3d(void) {
	import_array();
    Py_InitModule3("canv3d", canv3d_funcs, "Extension module example!");
}

////////////////////////////////////////////////////////////////////////////////////////
