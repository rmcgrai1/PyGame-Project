

//mat is 16 doubles long. eye, at, and up are 3 doubles long.
//Adapted from Chaoli Wang's Graphics class, MV.js
static double * lookAt(double* mat, double *eye, double *at, double *up )
{
  /*if ( !Array.isArray(eye) || eye.length != 3) {
        throw "lookAt(): first parameter [eye] must be an a vec3";
    }

    if ( !Array.isArray(at) || at.length != 3) {
        throw "lookAt(): first parameter [at] must be an a vec3";
    }

    if ( !Array.isArray(up) || up.length != 3) {
        throw "lookAt(): first parameter [up] must be an a vec3";
    }
  */
  //If eye equals at, return the identity matrix
  int i;
  for (i = 0; i < 3; i++)
    {
      if (eye[i] == at[i])
	{
	  return setMatIdentity(mat);
	}
    }
   
  int n[3];
  int u[3];
  int v[3];
  int temp[3];
  
  temp = subtractVecCopy(eye, at, temp, 3);
  n = normalizeCopy(temp, n, 3);
  temp = crossVec3Copy(up, n, temp);
  u = normalizeCopy(temp, u, 3);
  temp = crossVec3Copy(n, u, temp);
  v = normalizeCopy(temp, v, 3);

  mat[0] = u[0]; mat[1] = u[1]; mat[2] = u[2];
  mat[3] = -dot(u, eye);

  mat[4] = v[0]; mat[5] = v[1]; mat[6] = v[2];
  mat[7] = -dot(v, eye);

  mat[8] = n[0]; mat[9] = n[1]; mat[10] = n[2];
  mat[11] = -dot(n, eye);

  mat[12] = mat[13] = mat[14] = 0;
  mat[15] = 1;


  return mat;
  
		/*
    var n = normalize( subtract(eye, at));
    var u = normalize( cross(up, n));
    var v = normalize( cross(n, u));
    var result = mat4(
                      vec4( u, -dot(u, eye) ),
                      vec4( v, -dot(v, eye) ),
                      vec4( n, -dot(n, eye) ),
                      vec4()
                      );
		
    return result;
    */
}

double * normalizeModify(double* vec, int length)
{
  double mag = magnitude(vec, length);
  int i;
  for (i = 0; i < length; i++)
    {
      vec[i] = vec[i] / mag;
    }
  return vec;
}

double * normalizeCopy(double* vecSource, double* vecDest, int length)
{
  double mag = magnitude(vecSource, length);
  int i;
  for (i = 0; i < length; i++)
    {
      vecDest[i] = vecSource[i] / mag;
    }
  return vecDest;
}

double magnitude(double* vec, int length)
{
  int i;
  double sumTotal = 0;
  for (i = 0; i < length; i++)
    {
      sumTotal += vec[i] * vec[i]
    }
  return sqrt(sumTotal);
}

 double* subtractVecCopy(double *vec1, double *vec2, double* vecDest, int length)
 {
   int i;
   for (i = 0; i < length; i++)
     {
       vecDest[i] = vec1[i] - vec2[i];
     }
   return vecDest;
 }

double* crossVec3Copy(double *u, double *v, double* vecDest)
{
  vecDest[0] = (u[1]*v[2]) - (u[2]*v[1]);
  vecDest[1] = (u[2]*v[0]) - (u[0]*v[2]);
  vecDest[2] = (u[0]*v[1]) - (u[1]*v[0]);
  return vecDest;
}

double dot(double *u, double *v, int length)
{
  int i;
  double sumTotal = 0;
  for (i = 0; i < length; i++)
    {
      sumTotal += (u[i] * v[i])
    }
  return sumTotal;
}
