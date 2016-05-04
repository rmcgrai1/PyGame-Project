static void printVec(double* vec4);
static void printMat(double* mat);
static double* set4(double *vec4, double x, double y, double z, double w);
static double* set16(double* mat, 	double a1,double a2,double a3,double a4,	double b1,double b2,double b3,double b4,	double c1,double c2,double c3,double c4,	double d1,double d2,double d3,double d4);
static double* copyVec(double* srcVec, double* dstVec);
static double* copyMat(double *srcMat, double *dstMat);
static double* multMatMat(double* mat1, double* mat2, double* dstMat);
static double* multMatVec(double* mat, double* vec, double* dstVec);
static double* multMatVec3(double* mat, double* vec, double* dstVec, double slot4);
static double* setMatIdentity(double *mat);




static double
	tempVec[4] = {0,0,0,1},
	tempMatMult[16] = {1,0,0,0, 
					 0,1,0,0,	
					 0,0,1,0, 
					 0,0,0,1},
	tempMatAdd[16] = {1,0,0,0,
					 0,1,0,0,
					 0,0,1,0, 
					 0,0,0,1},
	tempMatTrans[16] = {1,0,0,0, 
					 0,1,0,0,
					 0,0,1,0, 
					 0,0,0,1},
	tempMatPersp[16] = {1,0,0,0, 
					 0,1,0,0, 
					 0,0,1,0,
					 0,0,0,1};
					 

static void printVec(double* vec4) {
	printf("<%lf,%lf,%lf,%lf>\n", vec4[0],vec4[1],vec4[2],vec4[3]);
}

static void printMat(double* mat) {
	printf("|%lf,%lf,%lf,%lf|\n", mat[0],mat[1],mat[2],mat[3]);
	printf("|%lf,%lf,%lf,%lf|\n", mat[4],mat[5],mat[6],mat[7]);
	printf("|%lf,%lf,%lf,%lf|\n", mat[8],mat[9],mat[10],mat[11]);
	printf("|%lf,%lf,%lf,%lf|\n", mat[12],mat[13],mat[14],mat[15]);
}

static double* set4(double *vec4, double x, double y, double z, double w) {
	vec4[0] = x;
	vec4[1] = y;
	vec4[2] = z;
	vec4[3] = w;
	
	return vec4;
}

static double* set16(double* mat, 	double a1,double a2,double a3,double a4,	double b1,double b2,double b3,double b4,	double c1,double c2,double c3,double c4,	double d1,double d2,double d3,double d4) {
	//printf("> set16()\n");
	mat[0] = a1;
	mat[1] = a2;
	mat[2] = a3;
	mat[3] = a4;
	mat[4] = b1;
	mat[5] = b2;
	mat[6] = b3;
	mat[7] = b4;
	mat[8] = c1;
	mat[9] = c2;
	mat[10] = c3;
	mat[11] = c4;
	mat[12] = d1;
	mat[13] = d2;
	mat[14] = d3;
	mat[15] = d4;
	//printf("< set16()\n");
	return mat;
}

static double* copyVec(double* srcVec, double* dstVec) {
	dstVec[0] = srcVec[0];
	dstVec[1] = srcVec[1];
	dstVec[2] = srcVec[2];
	dstVec[3] = srcVec[3];
	
	return dstVec;
}
	
static double* copyMat(double *srcMat, double *dstMat) {
	dstMat[0] = srcMat[0];
	dstMat[1] = srcMat[1];
	dstMat[2] = srcMat[2];
	dstMat[3] = srcMat[3];
	dstMat[4] = srcMat[4];
	dstMat[5] = srcMat[5];
	dstMat[6] = srcMat[6];
	dstMat[7] = srcMat[7];
	dstMat[8] = srcMat[8];
	dstMat[9] = srcMat[9];
	dstMat[10] = srcMat[10];
	dstMat[11] = srcMat[11];
	dstMat[12] = srcMat[12];
	dstMat[13] = srcMat[13];
	dstMat[14] = srcMat[14];
	dstMat[15] = srcMat[15];

	return dstMat;
}

static double* transpose(double *mat) {
	copyMat(mat, tempMatTrans);
	
	int x,y;
	for(y = 0; y < 4; y++)
		for(x = 0; x < 4; x++)
			mat[4*y + x] = tempMatTrans[4*x + y];
	return mat;
}

static double* multMatMat(double* mat1, double* mat2, double* dstMat) {
	// Very ugly, but more efficient!!
	double* dst;
	
	if(mat1 == dstMat || mat2 == dstMat)
		dst = tempMatMult;
	else
		dst = dstMat;
	
	dst[0] = mat1[0]*mat2[0] + mat1[1]*mat2[4] + mat1[2]*mat2[8] + mat1[3]*mat2[12];
	dst[1] = mat1[0]*mat2[1] + mat1[1]*mat2[5] + mat1[2]*mat2[9] + mat1[3]*mat2[13];
	dst[2] = mat1[0]*mat2[2] + mat1[1]*mat2[6] + mat1[2]*mat2[10] + mat1[3]*mat2[14];
	dst[3] = mat1[0]*mat2[3] + mat1[1]*mat2[7] + mat1[2]*mat2[11] + mat1[3]*mat2[15];
	
	dst[4] = mat1[4]*mat2[0] + mat1[5]*mat2[4] + mat1[6]*mat2[8] + mat1[7]*mat2[12];
	dst[5] = mat1[4]*mat2[1] + mat1[5]*mat2[5] + mat1[6]*mat2[9] + mat1[7]*mat2[13];
	dst[6] = mat1[4]*mat2[2] + mat1[5]*mat2[6] + mat1[6]*mat2[10] + mat1[7]*mat2[14];
	dst[7] = mat1[4]*mat2[3] + mat1[5]*mat2[7] + mat1[6]*mat2[11] + mat1[7]*mat2[15];

	dst[8] = mat1[8]*mat2[0] + mat1[9]*mat2[4] + mat1[10]*mat2[8] + mat1[11]*mat2[12];
	dst[9] = mat1[8]*mat2[1] + mat1[9]*mat2[5] + mat1[10]*mat2[9] + mat1[11]*mat2[13];
	dst[10] = mat1[8]*mat2[2] + mat1[9]*mat2[6] + mat1[10]*mat2[10] + mat1[11]*mat2[14];
	dst[11] = mat1[8]*mat2[3] + mat1[9]*mat2[7] + mat1[10]*mat2[11] + mat1[11]*mat2[15];

	dst[12] = mat1[12]*mat2[0] + mat1[13]*mat2[4] + mat1[14]*mat2[8] + mat1[15]*mat2[12];
	dst[13] = mat1[12]*mat2[1] + mat1[13]*mat2[5] + mat1[14]*mat2[9] + mat1[15]*mat2[13];
	dst[14] = mat1[12]*mat2[2] + mat1[13]*mat2[6] + mat1[14]*mat2[10] + mat1[15]*mat2[14];
	dst[15] = mat1[12]*mat2[3] + mat1[13]*mat2[7] + mat1[14]*mat2[11] + mat1[15]*mat2[15];

	if(dst != dstMat)
		return copyMat(tempMatMult, dstMat);
	else
		return dst;
}
	
static double* multMatVec(double* mat, double* vec, double* dstVec) {
	int x, y;
	double cell;
	for(y = 0; y < 4; y++) {
		cell = 0;
		for(x = 0; x < 4; x++)
			cell += mat[4*y + x]*vec[x];
		tempVec[y] = cell;
	}
	
	return copyVec(tempVec, dstVec);
}

static double* multMatVec3(double* mat, double* vec, double* dstVec, double slot4) {
	double* dst = tempVec;
	
	dst[0] = mat[0]*vec[0] + mat[1]*vec[1] + mat[2]*vec[2] + mat[3]*slot4;
	dst[1] = mat[4]*vec[0] + mat[5]*vec[1] + mat[6]*vec[2] + mat[7]*slot4;
	dst[2] = mat[8]*vec[0] + mat[9]*vec[1] + mat[10]*vec[2] + mat[11]*slot4;

	dstVec[0] = dst[0];
	dstVec[1] = dst[1];
	dstVec[2] = dst[2];
	
	return dstVec;
}



static double* setMatIdentity(double *mat) {
	return set16(mat,  
		1,0,0,0,  
		0,1,0,0,
		0,0,1,0,
		0,0,0,1);
}

static double* setMatTranslation(double* mat, double x, double y, double z) {
	return set16(mat,  1,0,0,x,  0,1,0,y,  0,0,1,z,  0,0,0,1);
}
static double* addMatTranslation(double* mat, double x, double y, double z) {
	setMatTranslation(tempMatAdd, x,y,z);
	return multMatMat(mat,tempMatAdd, mat);
}

static double* setMatScale(double* mat, double sx, double sy, double sz) {
	return set16(mat,  sx,0,0,0,  0,sy,0,0,  0,0,sz,0,  0,0,0,1);
}
static double* addMatScale(double* mat, double sx, double sy, double sz) {
	setMatScale(tempMatAdd, sx,sy,sz);
	return multMatMat(mat,tempMatAdd, mat);
}

static double* setMatRotationX(double* mat, double degX) {
	double 
		co = cosd(degX),
		si = sind(degX);
	return set16(mat,  1,0,0,0,  0,co,-si,0,  0,si,co,0,  0,0,0,1);
}
static double* addMatRotationX(double* mat, double degX) {
	setMatRotationX(tempMatAdd, degX);
	return multMatMat(mat,tempMatAdd, mat);
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
static double* addMatRotationY(double* mat, double degY) {
	setMatRotationY(tempMatAdd, degY);
	return multMatMat(mat,tempMatAdd, mat);
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
static double* addMatRotationZ(double* mat, double degZ) {
	setMatRotationZ(tempMatAdd, degZ);
	return multMatMat(mat,tempMatAdd, mat);
}



static void mcross(double x1, double y1, double z1, double x2, double y2, double z2, double *x3, double *y3, double *z3) {
	*x3 = y1*z2 - y2*z1;
	*y3 = -x1*z2 + x2*z1;
	*z3 = x1*y2 - x2*y1;
}

static void mnormalize(double* x, double* y, double* z) {
	double
		xx = *x,
		yy = *y,
		zz = *z,
		len = sqrt(xx*xx + yy*yy + zz*zz);
		
	*x /= len;
	*y /= len;
	*z /= len;
}