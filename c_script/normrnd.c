#include "Python.h"
#include "normrnd.h"

/* See Knuth TAOCP Vol2. 3rd Ed. P.106 for multiplier. */
/* In the previous versions, MSBs of the seed affect   */
/* only MSBs of the array mt[].                        */
/* 2002/01/09 modified by Makoto Matsumoto             */

#define N 624
#define M 397
#define MATRIX_A 0x9908b0dfUL
#define UPPER_MASK 0x80000000UL
#define LOWER_MASK 0x7fffffffUL

static unsigned long mt[N]; /* vettore di stato  */
static int mti = N + 1; /* mti==N+1 significa che mt[N] non è inizializzato */

void init_genrand(unsigned long s)
{
	mt[0] = s & 0xffffffffUL;
	for (mti = 1; mti<N; mti++) {
		mt[mti] =
			(1812433253UL * (mt[mti - 1] ^ (mt[mti - 1] >> 30)) + mti);

		mt[mti] &= 0xffffffffUL;
		/* per macchine >32 bit */
	}
}

void init_by_array(unsigned long init_key[], unsigned long key_length)
{
	int i, j, k;
	init_genrand(19650218UL);
	i = 1; j = 0;
	k = (N>key_length ? N : key_length);
	for (; k; k--) {
		mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525UL))	+ init_key[j] + j; /* non linear */
		mt[i] &= 0xffffffffUL; /* per WORDSIZE > 32  */
		i++; j++;
		if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
		if (j >= key_length) j = 0;
	}
	for (k = N - 1; k; k--) {
		mt[i] = (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941UL)) - i;
		mt[i] &= 0xffffffffUL; /* per WORDSIZE > 32  */
		i++;
		if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
	}

	mt[0] = 0x80000000UL; /* MSB è 1; per non avere il registro iniziale completamente a 0 */
}

/* genera numeri random sull'intervallo [0,0xffffffff] */
unsigned long genrand_int32(void)
{
	unsigned long y;
	static unsigned long mag01[2] = { 0x0UL, MATRIX_A };
	/* mag01[x] = x * MATRIX_A  for x=0,1 */

	if (mti >= N) { /* genera N words alla volta */
		int kk;

		if (mti == N + 1)   /* nel caso dovessi inizializzare il seed */
			init_genrand(5489UL); /* valore di default del seed */

		for (kk = 0; kk<N - M; kk++) {
			y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
			mt[kk] = mt[kk + M] ^ (y >> 1) ^ mag01[y & 0x1UL];
		}
		for (; kk<N - 1; kk++) {
			y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
			mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
		}
		y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK);
		mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ mag01[y & 0x1UL];

		mti = 0;
	}

	y = mt[mti++];

	/* Tempering */
	y ^= (y >> 11);
	y ^= (y << 7) & 0x9d2c5680UL;
	y ^= (y << 15) & 0xefc60000UL;
	y ^= (y >> 18);

	return y;
}



double genrand_real3(void)
{
	return (((double)genrand_int32()) + 0.5)*(1.0 / 4294967296.0);
}

/*normrnd Box-Muller Transform*/
double normRND(double mu, double sigma)
{
	const double tau = 2.0*pi;

	static float z0, z1;

	//genrand_real3() genera la sequenza di numeri casuali come Matlab (comando RNG(0)) con seed = 0 twister, ma Matlab salta un valore

	double u1, u2, garb;

	u1 = genrand_real3();//u1 = rand() * (1.0 / RAND_MAX);
	garb = genrand_real3();//serve per saltare un valore come Matlab
	u2 = genrand_real3();//u2 = rand() * (1.0 / RAND_MAX);
	garb = genrand_real3();

	z0 = sqrt(-2.0 * log(u1)) * cos(tau * u2);
	z1 = sqrt(-2.0 * log(u1)) * sin(tau * u2);
	return z0 * sigma + mu;
}


static PyObject* rnd(PyObject* self, PyObject* args)
{
    double mu = 0.0;
    double sigma = 0.0;

    //dd double, double
    if (!PyArg_ParseTuple(args, "dd", &mu, &sigma))
        return NULL;

    // "d" return type value
    return Py_BuildValue("d", normRND(mu, sigma));
}

static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "Version 1.0");
}

static PyMethodDef myMethods[] = {
    {"normRND", rnd, METH_VARARGS, "normRND function."},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns the version."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef myNormrnd = {
	PyModuleDef_HEAD_INIT,
	"myNormrnd",
	"normRND",
	-1,
	myMethods
};

PyMODINIT_FUNC PyInit_myNormrnd(void)
{
    return PyModule_Create(&myNormrnd);
}