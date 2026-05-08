/* SIMONUTTI MATTIA SM3201292 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include "mandelbrot.h"
#include <omp.h>  
#include "pgm.h"


/* Funzione che apre il file, calcola la dimensione e fà il mapping con mmap. In input vengono passati il path del file da aprire e un dato di tipo
struct netbpm_ptr in cui andranno inserite le informazioni circa il file da aprire (dimensione) e che verranno usate per fare il mapping in memoria*/

int open_image(char * path, netpbm_ptr img) 
{
  img->fd = fopen(path, "r+");
  if (img->fd == NULL) {
    return -1;
  }
  struct stat sbuf;
  stat(path, &sbuf);
  img->size = sbuf.st_size;
  if (fscanf(img->fd, "P5\n%d %d\n255\n", &img->width, &img->height) != 2) {
    fclose(img->fd);
    printf("Intestazione file non corretta!\n");
    return -2;
  }
  img->offset = ftell(img->fd);
  img->data = mmap((void *)0, img->size, PROT_READ | PROT_WRITE, MAP_SHARED, fileno(img->fd), 0); /*PROT_READ e PROT_WRITE permettono la lettura e la modifica dei dati del file*/
  if (img->data == MAP_FAILED) {
    fclose(img->fd);
    printf("Fallito mapping in memoria\n");
    return -3;
  }
  return 0;
}

/*funzione che crea un'immagine vuota, vengono passati in input il path del file da creare, la struttura img in cui inserire i valori width e heigth
passati anch'essi in input */
int empty_image(char * path, netpbm_ptr img, int width, int height) 
{
  FILE * fd = fopen(path, "w+");
  if (fd == NULL) {
    return -1;
  }

  /*scriviamo nel file la larghezza e altezza volute*/
  /*modifichiamo la dimensione del file creato (ftruncate) sommando ai valori scritti da noi le dimensioni in altezza e larghezza dell'immagine*/
  int written = fprintf(fd, "P5\n%d %d\n255\n", width, height); 
  ftruncate(fileno(fd), written + width * height); 
  fclose(fd);
  return open_image(path, img);
}

/*funzione per accedere ai singoli pixel dell'immagine, passiamo in input la struttura img e le coordinate a cui vogliamo accedere*/


char * pixel_at(netpbm_ptr img, int x, int y) {
  if (img == NULL) {
    return NULL;
  }
  if (x < 0 || x >= img->width) {
    return NULL;
  }
  if (y < 0 || y >= img->height) {
    return NULL;
  }
  return &img->data[y * img->width + x + img->offset];
}

int close_image(netpbm_ptr img)
{
  if (img == NULL) {
    return -1;
  }
  munmap(img->data, img->size);
  fclose(img->fd);
  return 0;
}

/* Funzione per creare l'immagine del frattale, prende in input una matrice di dimensione ncols*nrows, un puntatore ad una struttura img, nrows, ncols e il numero massimo di iterazioni*/

int draw_image(int *Matrix, netpbm_ptr img, int nrows, int ncols, int M){
  
  double start = omp_get_wtime();
  color_matrix(Matrix, nrows, ncols, M); /* Viene chiamata la funzione che riempie la matrice con i colori dei pixel in base al numero di iterazioni svolte*/
  #pragma omp parallel for schedule(static)

  for (int y = 0; y < nrows; y++) {
    for (int x = 0; x < ncols; x++) {
      
      char *cup = pixel_at(img, x, y); /* accediamo al pixel in posizione (x,y)*/

      if (cup == NULL) {
        printf("Error at x = %d y = %d\n", x, y);
      }

      *cup = Matrix[y*ncols + x]; /* Coloriamo il pixel con il colore indicato dalla matrice*/
      }


  }

  
 
  double end = omp_get_wtime();
  float seconds = (float) (end - start);

  printf("%f\t", seconds);

  return 0;

  
}