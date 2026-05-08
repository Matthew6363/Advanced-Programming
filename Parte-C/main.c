/* SIMONUTTI MATTIA SM3201292 */

#include <stdlib.h>
#include <stdio.h>
#include "pgm.h"
#include <string.h>





int main(int argc, char *argv[]) {

    int err = 0;
     if (argc < 4){
        err = -1;
        printf("Numero di argomenti passati insufficiente! Errore: %d", -err);
        return -err;
    }

    int nrows = atoi(argv[3]);
    int ncols = 1.5*nrows;
    int M = atoi(argv[2]);
    char * path = argv[1];
    int * Matrix = (int*)malloc(sizeof(int)*ncols*nrows);
    netpbm mandelbrot_img;
    
    int i = 0;
    while(path[i] != '\0'){
        i++;
    }
    if(path[i-4] != '.' || path[i-3] != 'p' || path[i-2] != 'g' || path[i-1] != 'm' || i<5){
        err = -5;
        printf("Attenzione, formato file non corretto! Errore: %d\t" , -err);
        return -5; 
        }
   
    if( nrows == 0){
        err =  -6;
        printf("Il numero di righe non deve essere <= 0 e neppure una stringa! Errore: %d\t", -err);
        return -6;
    }


    if( M == 0){
        
        err =  -7;
        printf("Il numero di iterazioni massime non deve essere <= 0 e neppure una stringa! Errore: %d\t", -err);
        return -7;
    }

    err = empty_image(path, &mandelbrot_img, ncols, nrows ); /* chiamata alla funzione per generare un'immagine vuota*/
    if (err != 0) {
    printf("Apertura immagine non riuscita: %d\n", -err);
      return 1;
  }

    int result = draw_image(Matrix,&mandelbrot_img, nrows, ncols, M); /* chiamata alla funzione per generare l'immagine del Mandelbrot set*/
    if(result != 0){
        printf("Creazione immagine non riuscita! Errore %d\t", -err);
        return err;
    }

 close_image(&mandelbrot_img);
 free(Matrix);
 return 0;
    
}

 
