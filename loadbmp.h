//http://stackoverflow.com/questions/14279242/read-bitmap-file-into-structure

typedef char			INT8;
typedef short			INT16;
typedef int				INT32;
typedef unsigned char	UINT8;
typedef unsigned short	UINT16;
typedef unsigned int	UINT32;



#pragma pack(push, 1)

typedef struct tagBITMAPFILEHEADER {
    UINT16 bfType;  //specifies the file type
    UINT32 bfSize;  //specifies the size in bytes of the bitmap file
    UINT16 bfReserved1;  //reserved; must be 0
    UINT16 bfReserved2;  //reserved; must be 0
    UINT32 bOffBits;  //species the offset in bytes from the bitmapfileheader to the bitmap bits
} BITMAPFILEHEADER;

#pragma pack(pop)



#pragma pack(push, 1)

typedef struct tagBITMAPINFOHEADER {
    UINT32 biSize;  //specifies the number of bytes required by the struct
    int biWidth;  //specifies width in pixels
    int biHeight;  //species height in pixels
    UINT16 biPlanes; //specifies the number of color planes, must be 1
    UINT16 biBitCount; //specifies the number of bit per pixel
    UINT32 biCompression;//spcifies the type of compression
    UINT32 biSizeImage;  //size of image in bytes
    int biXPelsPerMeter;  //number of pixels per meter in x axis
    int biYPelsPerMeter;  //number of pixels per meter in y axis
    UINT32 biClrUsed;  //number of colors used by th ebitmap
    UINT32 biClrImportant;  //number of colors that are important
} BITMAPINFOHEADER;

#pragma pack(pop)




unsigned char *LoadBitmapFile(char *filename, BITMAPINFOHEADER *bitmapInfoHeader) {
    FILE *filePtr; //our file pointer
    BITMAPFILEHEADER bitmapFileHeader; //our bitmap file header
    unsigned char *bitmapImage;  //store image data
    int imageIdx=0;  //image index counter
    unsigned char tempRGB;  //our swap variable
    size_t read_result = 0;
	
	printf("Size of fileheader:%lu, infoHeader:%lu\n", sizeof(BITMAPFILEHEADER), sizeof(BITMAPINFOHEADER));

    //open filename in read binary mode
    filePtr = fopen(filename,"rb");
    if (filePtr == NULL) {
		printf("File \"%s\" does not exist!\n", filename);
        return NULL;
	}

    //read the bitmap file header
    read_result = fread(&bitmapFileHeader, sizeof(BITMAPFILEHEADER),1,filePtr);
    if(read_result != 1) {
      printf("Error reading from bitmapHeader of %s, %s\n", filename, strerror(errno));
    }

    //verify that this is a bmp file by check bitmap id
    if (bitmapFileHeader.bfType !=0x4D42) {
		printf("File \"%s\" is invalid bmp!\n", filename);
        fclose(filePtr);
        return NULL;
    }

    //read the bitmap info header
    read_result = fread(bitmapInfoHeader, sizeof(BITMAPINFOHEADER),1,filePtr); // small edit. forgot to add the closing bracket at sizeof
    if (read_result != 1) {
		printf("Error reading from bitmapHeader of %s, %s\n", filename, strerror(errno));
		return NULL;
	}
	printf("\tsize (in bytes): %d\n", bitmapInfoHeader->biSizeImage);
	printf("\tresolution: %d x %d\n", bitmapInfoHeader->biWidth, bitmapInfoHeader->biHeight);

    //move file point to the begging of bitmap data
    fseek(filePtr, bitmapFileHeader.bOffBits, SEEK_SET);

    //allocate enough memory for the bitmap image data
	printf("\tAllocating %d bytes for the image.\n", bitmapInfoHeader->biSizeImage);
    bitmapImage = (unsigned char*) malloc(bitmapInfoHeader->biSizeImage);

    //verify memory allocation
    if(!bitmapImage) {
		printf("Failed to allocate memory for %s!\n", filename);
        free(bitmapImage);
        fclose(filePtr);
        return NULL;
    }

    //read in the bitmap image data
    read_result = fread(bitmapImage, bitmapInfoHeader->biSizeImage,1, filePtr);
    if(read_result != 1) {
		printf("Error reading from bitmapHeader of %s\n", filename);
		return NULL;
    }
    //make sure bitmap image data was read
    if(bitmapImage == NULL) {
		printf("Failed to read image %s!\n", filename);
        fclose(filePtr);
        return NULL;
    }

    //swap the r and b values to get RGB (bitmap is BGR)
    for(imageIdx = 0; imageIdx < bitmapInfoHeader->biSizeImage; imageIdx+=3) {
        tempRGB = bitmapImage[imageIdx];
        bitmapImage[imageIdx] = bitmapImage[imageIdx + 2];
        bitmapImage[imageIdx + 2] = tempRGB;
    }

    //close file and return bitmap iamge data
    fclose(filePtr);
    return bitmapImage;
}
