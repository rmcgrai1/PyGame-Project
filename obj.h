#include "loadbmp.h"
#include "math2.h" 	

int* loadBMP(char *fileName, int *w, int *h) {
	//Uses Function from Library from netghost.narod.ru/gff/sample/code/micbmp/

	int r, c,
		width, height,
		pR, pG, pB,
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
	
	//Allocate Space for Image
	int* texPixels = (int *) malloc(height*width * sizeof(int));

	
	printf("\ttop-left pixel: (%d, %d, %d)\n", bitmapData[0], bitmapData[1], bitmapData[2]);

	// Compress bitmap data into single ints
	for(r = 0; r < height; r++)
		for(c = 0; c < width; c++) {
			texPixels[r*width + c] = convertRGB2Int(bitmapData[k], bitmapData[k+1], bitmapData[k+2]);
			k += 3;
		}
	
	//Free original array and header
	free(bitmapData);
	
	//Return Image Struct
	return texPixels;
}


/*********************************** OBJ LOADING ************************************/

typedef struct mtl_ {
	char* name;
	double* kd;
	int* map_Kd;
	int map_Kd_width, map_Kd_height;
} mtl;

typedef struct obj_ {
	double* vertices;
	int vNum;
	double* uvs;	
	int uvNum;
	int* faces;
	int fNum;
	mtl **mtls;
	int mNum;
} obj;

static obj **modelArray;
int modelNum = 0;

static obj* getObj(int id) {
	return modelArray[id];
}