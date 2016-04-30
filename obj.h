int* loadBMP(char *fileName) {
	//Uses Function from Library from netghost.narod.ru/gff/sample/code/micbmp/

	FILE * fp;
	RGB *argb, **argbA;
	int width, height;	
	int r, c, k = 0;

	//Load BMP Image
	fp = fopen(fileName, "r");
	readSingleImageBMP(fp, &argb, &width, &height);
	fclose(fp);

	//The Array of Pixels the Function Loaded is 1x(W*H), So We Should Convert it To
	//A Matrix of Dimensions WxH.
	////////////////////////////////////////////////////////////////////////////////

	//Allocate Space for Image
	argbA = (RGB **) malloc(height * sizeof(RGB *));

	for(r = 0; r < height; r++) {
		//Allocate Space for Row in Image
		argbA[r] = (RGB *) malloc(sizeof(RGB)*width);

		//Loop Through Each RGB Struct
		for(c = 0; c < width; c++) {
			//Copy RGB of Array to Matrix
			argbA[r][c].red = argb[k].red;
			argbA[r][c].blue = argb[k].blue;
			argbA[r][c].green = argb[k].green;

			//Go to Next Spot in Array
			k++;
		}
	}

	//Set Bitmap's Width, Height, and Pixel Arrays
	out.width = width;
	out.height = height;
	out.argb = argbA;

	
	//Free Space Taken Up by the Original Array
	free(argb);

	//Return Image Struct
	return out;
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