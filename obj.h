#include "loadbmp.h"
#include "math2.h" 	

int* loadBMP(char *fileName, int *w, int *h) {
	//Uses Function from Library from netghost.narod.ru/gff/sample/code/micbmp/

	int r, c,
		width, height,
		k = 0;

	//Load BMP Image
	BITMAPINFOHEADER bitmapInfoHeader;
	unsigned char *bitmapData;
	bitmapData = LoadBitmapFile(fileName,&bitmapInfoHeader);
	
	//The Array of Pixels the Function Loaded is 1x(W*H), So We Should Convert it To
	//A Matrix of Dimensions WxH.
	////////////////////////////////////////////////////////////////////////////////

	*w = width = bitmapInfoHeader.biWidth;
	*h = height = bitmapInfoHeader.biHeight;
	
	int size =  bitmapInfoHeader.biSizeImage;
	
	
	//Allocate Space for Image
	int* texPixels = (int *) malloc(height*width * sizeof(int));

	int pR, pG, pB;
	
	for(r = 0; r < height; r++) {
		//Loop Through Each RGB Struct
		
		for(c = 0; c < width; c++) {
			//Copy RGB of Array to Matrix
			texPixels[r*width + c] = convertRGB2Int(bitmapData[k], bitmapData[k+1], bitmapData[k+2]);
			k += 3;
		}
	}
	
	//Free Space Taken Up by the Original Array
	free(bitmapData);
	
	//Return Image Struct
	return texPixels;
}


/*********************************** OBJ LOADING ************************************/

typedef struct mtl {
	char* name;
	
	double ns;
	double* ka;
	double* kd;
	double* ks;
	double ni;
	double d;
	
	int* map_Kd;
	int map_Kd_width, map_Kd_height;
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