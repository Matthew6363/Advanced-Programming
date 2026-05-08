# SIMONUTTI MATTIA SM3201292 #

CC = gcc-14
CFLAGS = -O3 -fopenmp -Wall
LIB = lib
CHEADERS = ${wildcard *.h}
PROGNAME = main

all: ${PROGNAME}

${PROGNAME}: main.o ${LIB}/libpgm.a ${LIB}/libmandelbrot.a
	@${CC} ${CFLAGS} -o $@ $< -L./${LIB}/ -lpgm -lmandelbrot

${LIB}:
	mkdir -p $@

${LIB}/libpgm.a: pgm.o ${LIB}
	ar rs $@ $<

${LIB}/libmandelbrot.a: mandelbrot.o ${LIB}
	@ar rs $@ $<

main.o: main.c ${CHEADERS}
	@${CC} ${CFLAGS} -c $<

%.o: %.c %.h
	@${CC} ${CFLAGS} -c $<


.PHONY: clean clean-all
clean:
	rm -f *.o

clean-all: clean
	rm -rf ${LIB}
	rm -f ${PROGNAME}
	rm *.pgm
