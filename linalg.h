static void printVec(double* vec4);
static void printMat(double* mat);
static double* set4(double *vec4, double x, double y, double z, double w);
static double* set16(double* mat, 	double a1,double a2,double a3,double a4,	double b1,double b2,double b3,double b4,	double c1,double c2,double c3,double c4,	double d1,double d2,double d3,double d4);
static double* copyVec(double* srcVec, double* dstVec);
static double* copyMat(double *srcMat, double *dstMat);
static double* multMatMat(double* mat1, double* mat2, double* dstMat);
static double* multMatVec(double* mat, double* vec, double* dstVec);
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
	tempMatMult[0] = mat1[0]*mat2[0] + mat1[1]*mat2[4] + mat1[2]*mat2[8] + mat1[3]*mat2[12];
	tempMatMult[1] = mat1[0]*mat2[1] + mat1[1]*mat2[5] + mat1[2]*mat2[9] + mat1[3]*mat2[13];
	tempMatMult[2] = mat1[0]*mat2[2] + mat1[1]*mat2[6] + mat1[2]*mat2[10] + mat1[3]*mat2[14];
	tempMatMult[3] = mat1[0]*mat2[3] + mat1[1]*mat2[7] + mat1[2]*mat2[11] + mat1[3]*mat2[15];
	
	tempMatMult[4] = mat1[4]*mat2[0] + mat1[5]*mat2[4] + mat1[6]*mat2[8] + mat1[7]*mat2[12];
	tempMatMult[5] = mat1[4]*mat2[1] + mat1[5]*mat2[5] + mat1[6]*mat2[9] + mat1[7]*mat2[13];
	tempMatMult[6] = mat1[4]*mat2[2] + mat1[5]*mat2[6] + mat1[6]*mat2[10] + mat1[7]*mat2[14];
	tempMatMult[7] = mat1[4]*mat2[3] + mat1[5]*mat2[7] + mat1[6]*mat2[11] + mat1[7]*mat2[15];

	tempMatMult[8] = mat1[8]*mat2[0] + mat1[9]*mat2[4] + mat1[10]*mat2[8] + mat1[11]*mat2[12];
	tempMatMult[9] = mat1[8]*mat2[1] + mat1[9]*mat2[5] + mat1[10]*mat2[9] + mat1[11]*mat2[13];
	tempMatMult[10] = mat1[8]*mat2[2] + mat1[9]*mat2[6] + mat1[10]*mat2[10] + mat1[11]*mat2[14];
	tempMatMult[11] = mat1[8]*mat2[3] + mat1[9]*mat2[7] + mat1[10]*mat2[11] + mat1[11]*mat2[15];

	tempMatMult[12] = mat1[12]*mat2[0] + mat1[13]*mat2[4] + mat1[14]*mat2[8] + mat1[15]*mat2[12];
	tempMatMult[13] = mat1[12]*mat2[1] + mat1[13]*mat2[5] + mat1[14]*mat2[9] + mat1[15]*mat2[13];
	tempMatMult[14] = mat1[12]*mat2[2] + mat1[13]*mat2[6] + mat1[14]*mat2[10] + mat1[15]*mat2[14];
	tempMatMult[15] = mat1[12]*mat2[3] + mat1[13]*mat2[7] + mat1[14]*mat2[11] + mat1[15]*mat2[15];

	return copyMat(tempMatMult, dstMat);
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






static double mdot(double x1, double y1, double z1, double x2, double y2, double z2) {
	return x1*x2 + y1*y2 + z1*z2;
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