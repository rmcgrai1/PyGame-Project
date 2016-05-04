// Jacob Kassman & Ryan McGrail
// obj.h
// Defines obj & mtl loading functions and their structs.


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


// Add object to array
static int createObj(void) {
	int id = modelNum++;
	
	// Allocate new array
	obj** oldModelArray = modelArray;
	modelArray = (obj**) malloc(modelNum * sizeof(obj*));
	
	// Move over old elements
	int i;
	for(i = 0; i < modelNum-1; i++)
		modelArray[i] = oldModelArray[i];
	
	// Allocate newest element
	modelArray[id] = (obj*) malloc(sizeof(obj));

	// Free old array
	if(id > 0)
		free(oldModelArray);
	
	return id;
}


static mtl** loadMtl(char* filename) {
	int* tex;
		
	FILE *fp;
	char lines[200][200], line[200], *type, *substr, c, cc[2];
	int l = 0, lLen = 0, lNum = 0, mNum = 0;
	
	printf("\tLoading mtls from %s...\n", filename);
       
	// Attempt to open file
	if((fp = fopen(filename, "r")) == NULL) {
	    printf("Invalid Filename %s\n", filename);
	    return NULL;
	}
	
	cc[1] = '\0';
	lines[0][0] = '\0';
	
	// Load file into string array
	while(!feof(fp)) {
		cc[0] = fgetc(fp);
		
		// Read to end of line, and then start next line
		if(cc[0] == '\r') {}
		else if(cc[0] == '\n') {
			if(lLen > 0) {
				lines[++lNum][0] = '\0';
				lLen = 0;
			}
		}
		
		// Concatenate read characters to end of line
		else {
			strcat(lines[lNum], cc);
			lLen++;
		}
	}
	// Close file
	fclose(fp);

	
	int i;
	// Loop through File Once to Get # of each
	for(l = 0; l < lNum; l++) {
		strcpy(line, lines[l]);	
		
		// If type is "newmtl", another material to create!
		if(!strcmp(strtok(line, " "), "newmtl"))
			mNum++;
	}

	// Allocate array of materials.
	int mi = 0;
	mtl *m = NULL,
		**mtls = (mtl**) malloc(mNum * sizeof(mtl*));
	
	// Loop through File Second Time
	for(l = 0; l < lNum; l++) {
		strcpy(line, lines[l]);	
		type = strtok(line, " ");
				
		// Create new material
		if(!strcmp(type,"newmtl")) {
			substr = strtok(NULL, " ");

			// Allocate new material
			printf("\tAdding new material %s!\n", substr);
			m = mtls[mi++] = (mtl*) malloc(sizeof(mtl));			

			// Copy its name
			m->name = malloc((strlen(substr)+1) * sizeof(char));
			strcpy(m->name, substr);

			// Create diffuse color array in material
			m->kd = (double*) malloc(3 * sizeof(double));
		}
		
		// Set diffuse color of material
		else if(!strcmp(type,"Kd")) {
			for(i = 0; i < 3; i++) {
				substr = strtok(NULL, " ");				
				m->kd[i] = atof(substr);				
			}
		}
		
		// Load texture for material
		else if(!strcmp(type,"map_Kd")) {
			substr = strtok(NULL, " ");
			
			printf("\tLoading .bmp from %s...\n", substr);
		    m->map_Kd = loadBMP(substr, &m->map_Kd_width, &m->map_Kd_height);
		}
	}
	
	printf("\tDone loading mtls!\n");
	
	return mtls;
}


static void loadObj(char* filename, int id) {	
	FILE *fp;
	char lines[1000][150], line[150], *type, *substr, c, cc[2];
	int l = 0, lNum = 0, mNum = 0, lLen = 0;
	
	printf("Loading \"%s\"...\n", filename);

	// Attempt to Open file
	if((fp = fopen(filename, "r")) == NULL) {
	  printf("File %s does not exist!\n", filename);
	  return;
	}
	
	cc[1] = '\0';	
	lines[0][0] = '\0';
	
	// Load file into string array
	while(!feof(fp)) {
		cc[0] = fgetc(fp);
		
		// Jump to new line if at end of current line
		if(cc[0] == '\r') {}
		else if(cc[0] == '\n') {
			if(lLen > 0) {
				lines[++lNum][0] = '\0';
				lLen = 0;
			}
		}
		
		// Otherwise append to end of line
		else {
			strcat(lines[lNum], cc);
			lLen++;
		}
	}
	
	// Close file
	fclose(fp);
	
	printf("\tDone reading file into memory!\n");

	int i, vNum = 0, fNum = 0, uvNum = 0;

	// Loop through file once to get # of each type of part
	for(l = 0; l < lNum; l++) {
		strcpy(line, lines[l]);	
		type = strtok(line, " ");
		
		if(!strcmp(type,"v"))
			vNum++;
		else if(!strcmp(type,"vt"))
			uvNum++;
		else if(!strcmp(type, "f"))
			fNum++;
		else if(!strcmp(type, "usemtl")) {
			fNum++;
			mNum++;
		}
	}
	
	// Access object to be loaded into.
	obj* o = modelArray[id];

	// Create arrays to store lists in obj
	int
		ii, f = 0, v = 0, vt = 0,
		*faces = (int*) malloc(9 * fNum * sizeof(int));
	double
		*vertices = (double*) malloc(3 * vNum * sizeof(double)),
		*uvs = (double*) malloc(2 * uvNum * sizeof(double));

	
	mtl **mtls = NULL; // *m;
	
	// Loop through File Second Time
	for(l = 0; l < lNum; l++) {
		strcpy(line, lines[l]);	
		type = strtok(line, " ");
				
		// Load vertex
		if(!strcmp(type,"v")) {
			for(i = 0; i < 3; i++) {
				substr = strtok(NULL, " ");
				vertices[3*v + i] = atof(substr);
			}
			v++;
		}
		
		// Load UV
		else if(!strcmp(type,"vt")) {
			for(i = 0; i < 2; i++) {
				substr = strtok(NULL, " ");
								
				uvs[2*vt + i] = atof(substr);
			}
			vt++;
		}
		
		// Load mtl library
		else if(!strcmp(type,"mtllib"))
			mtls = loadMtl(strtok(NULL, " "));

		// Enable material at point in model
		else if(!strcmp(type,"usemtl")) {
			
			// Set -1 at face index to mark material
			faces[9*f] = -1;

			// Get material index
			ii = -1;
			substr = strtok(NULL, " ");
			for(i = 0; i < mNum; i++)
				if(!strcmp(substr,mtls[i]->name)) {
					ii = i;
					break;
				}
				
			// If did not find proper index, report error
			if(ii == -1)
				printf("Invalid material name: %s\n", substr);

			// Set v2 to index
			faces[9*f + 3] = ii;
			
			f++;
		}
		
		// Load face
		else if(!strcmp(type, "f")) {
			
			// Read v/vt/vn indices
			for(ii = 0; ii < 3; ii++) {
				for(i = 0; i < 3; i++) {
					substr = strtok(NULL , (i<2)?"/":" ");
					faces[9*f + 3*ii + i] = atoi(substr)-1;
				}
			}
			f++;
		}
	}
			
	// Set variables in obj
	o->vNum = vNum;
	o->uvNum = uvNum;
	o->fNum = fNum;
	o->faces = faces;
	o->uvs = uvs;
	o->vertices = vertices;
	o->mtls = mtls;
	o->mNum = mNum;
}