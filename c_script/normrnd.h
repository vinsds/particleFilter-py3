#ifndef NORMRND_H
#define NORMRND_H

#include <stdlib.h>
#include <math.h>
#include <limits.h>

const float pi = 3.14159265;
const float e  = 2.71828183;

/************************************************/
/* Reference: M.Matsumoto and T.Nishimura, "Mersenne Twister: A
   623 - Dimensionally Equidistributed Uniform Pseudo - Random Number Generator",
   ACM Transactions on Modeling and Computer Simulation, Vol. 8, No. 1,
   January 1998, pp 3--30.
*/
/****************************************************************************
*
* Mersenne Twister code:
*/
void init_genrand(unsigned long s);


/* Inizializzazione */
void init_by_array(unsigned long init_key[], unsigned long key_length);

/* genera numeri random sull'intervallo [0,0xffffffff]*/
unsigned long genrand_int32(void);

/* genera numeri random sull'intervallo (0,1)*/
double genrand_real3(void);

double normRND(double mu, double sigma);

#endif
