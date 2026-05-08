/* SIMONUTTI MATTIA SM3201292 */

#include <stdlib.h>
#include <stdio.h>
#include "mandelbrot.h"
#include <math.h>

#define RADIUM_SQUARED 4


/* La funzione mandelbrot implementata sotto, restituisce il numero di iterazioni della formula F(z) = z^2 +c eseguite prima che
il modulo di tale F(z) risultasse maggiore di un raggio r pari a 2 (F(z), z e c sono numeri complessi);
Se viene raggiunto il numero massimo di iterazioni possibili, viene restituito quel valore.
La funzione prende in input x0 , y0 e maxite, che sono le coordinate del punto di cui verificare l'appartenenza al mandelbrot set e il 
numero massimo di iterazioni da compiere.
*/

int mandelbrot(float x0, float y0, int maxite){
    float x2= 0;
    float y2= 0;
    float xold = 0;
    float yold = 0;
    int period = 0;
    float x = 0;
    float y = 0;
    int iteration = 0;

    /* Controllo appartenenza dei punti al cardoide o al bulpo di periodo 2, ritorna direttamente il numero di iterazioni massime*/
    /*(https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set)*/
    float p = (x0 -0.25)*(x0 - 0.25) + y0*y0; 
    if((p*(p+(x0-0.25))<= 0.25*x0*x0) && ((x0+1)*(x0+1) + y0*y0 <= 1/16)){   
        return maxite;
    }

    /*Il ciclo che controlla che il modulo del numero (e i moduli generati reiterando la funzione F(z) = z^2 + c)
    aggiorna i valori di x e y (valori del punto dato in input aggiornati in seguito all'applicazione della funzione F(z)), 
    rispettivamente parte reale e immaginaria del numero z, e incrementa il numero di iterazioni eseguite; */

    while ((x2 + y2) <= RADIUM_SQUARED && iteration < maxite) { 
        y = 2 * x * y + y0;
        x = x2 - y2 + x0;
        x2 = x * x;
        y2 = y * y;
        iteration++;

    /* Verifica della periodicità, viene fatto un controllo aggiuntivo per vedere 
    se iterando sul punto attuale ritroviamo un punto precedentemente incontrato 
    e conoscendo il comportamento del punto incontarto in precedenza ritorniamo 
    il valore maxite (numero massimo di iterazioni) garantendo di non eseguire 
    iterazioni extra per un punto di cui conosciamo già il comportamento.
    (queso metodo è indicato assieme all'altro al link indicato sopra)*/

        if(x == xold && y == yold){ 
            return maxite;
        }
        period++;
        if(period > 10){
            period = 0;
            xold = x;
            yold = y;
        }


        }
    return iteration;
  }

/*Funzione che prende in input una matrice di dimenione ncols*nrows, nrows, ncols e M numero massimo di iterazioni, riempie 
la matrice con i colori dei pixel ricavati applicando la funzione Mandelbrot  */

void color_matrix(int * Matrix,int nrows, int ncols, int M){

    if(nrows % 2 != 0){
        printf("nrows indicato è dispari, sommo 1 per renderlo pari\n");
        nrows = nrows +1;
    }
    float step_h = 2.0f/(nrows); /*passo in altezza, (distanza valori asse immaginario)/nrows*/
    float step_w = 3.0f/(ncols); /*passo in larghezza, (distanza valori asse reale)/ncols*/
    int cost = 255/log(M);


  /*possiamo dimezzare il lavoro poichè l'immagine è simmetrica rispetto all'asse dei reali, dunque vale lo stesso per la matrice dei colori*/
  #pragma omp parallel for schedule(dynamic)
  for (int y = 0; y < nrows/2; y++) {
    for (int x = 0; x < ncols; x++) {

        /*applichiamo direttamente la formula fornita per il colore del pixel al risultato della funzione mandelbrot
        applicata al punto sul piano di Gauss e salviamo il risultato in una matrice, salvando anche il valore simmetrico; 
        Facciamo (x*step_w - 2) per ottenere la parte reale delle coordinate del pixel nel piano di Gauss, mentre
        facciamo (1 - y*step_h) per ottenere la componente immaginaria delle coordinate del pixel*/
      
        Matrix[y*ncols + x] = (cost*log(mandelbrot((x*step_w - 2),(1- y*step_h),M)));
        Matrix[(nrows -y -1)*ncols+x] =  Matrix[y*ncols + x];
     
      }
  } 
}