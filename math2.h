static double cosd(double deg);
static double sind(double deg);
static double tand(double deg);
static double epoch();	
static double contain(double mi, double x, double ma);

static double
	D2R = M_PI / 180;


static double cosd(double deg) {
	return cos(deg * D2R);
}
static double sind(double deg) {
	return sin(deg * D2R);
}
static double tand(double deg) {
	return tan(deg * D2R);
}

static double epoch() {
	return time(NULL);
}	
	
static double contain(double mi, double x, double ma) {
	return (x < mi) ? mi : ((x > ma) ? ma : x);
}