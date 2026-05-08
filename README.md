# Advanced-Programming

# Advanced and Parallel Programming Project

This repository contains the two-part final project for the Advanced and Parallel Programming course. The work involves high-performance computing in **C** and the development of a custom interpreter in **Python**.

---

## Part 1: Parallel Mandelbrot Fractal (C)
[cite_start]The goal is to develop a program that renders the Mandelbrot set as a grayscale image in `.pgm` format[cite: 3, 28].

### Technical Features
* [cite_start]**Parallel Computing:** The core calculation is parallelized using **OpenMP** to optimize performance[cite: 41].
* [cite_start]**Memory Efficiency:** Image saving is handled via **mmap**[cite: 42].
* [cite_start]**Mathematical Model:** * Calculates the sequence $z_{n+1} = z_n^2 + c$ with a divergence radius $r=2$[cite: 14, 22].
    * [cite_start]Interior points are colored white (255)[cite: 30].
    * [cite_start]Exterior points use a logarithmic color scale $\lfloor255 \times \frac{\log(n)}{\log(M)}\rfloor$ based on the divergence speed $n$[cite: 31].
* [cite_start]**CLI Support:** Accepts the filename, max iterations ($M$), and vertical resolution ($n_{rows}$) as command-line arguments[cite: 18, 19, 20, 21].
* [cite_start]**Architecture:** Modular design with separate modules for fractal logic (`mandelbrot.c/h`) and image management (`pgm.c/h`), compiled via **Makefile**[cite: 36, 37].

---

## Part 2: Custom Language Interpreter (Python)
[cite_start]This part involves extending a Lisp-like interpreter to support advanced programming constructs[cite: 57].

### Language Features
* [cite_start]**Variables & Arrays:** * Variable allocation (`alloc`) and array allocation (`valloc`)[cite: 62, 65].
    * [cite_start]Value assignment for variables (`setq`) and specific array indices (`setv`)[cite: 67, 68].
* **Control Flow:**
    * [cite_start]**Conditionals:** `if` statements for branching logic[cite: 75].
    * [cite_start]**Loops:** `while` and `for` loops for iterative execution[cite: 77, 79].
* [cite_start]**Subroutines:** Ability to define reusable code blocks (`defsub`) and execute them via `call`[cite: 82, 83].
* [cite_start]**Comparisons:** Support for boolean operators: `>`, `>=`, `=`, `!=`, `<`, and `<=`[cite: 59].
* [cite_start]**Sequencing:** Built-in support for executing sequences of 2, 3, or 4 operations (`prog2`, `prog3`, `prog4`)[cite: 72].

---

## Requirements & Submission
* [cite_start]**Documentation:** All significant functions are documented with descriptions of tasks, inputs, and outputs[cite: 46, 141].
* [cite_start]**Error Handling:** The C program returns non-zero codes on failure, while the Python interpreter raises specific, coherent exceptions[cite: 45, 139, 140].
* [cite_start]**Compliance:** Every source file includes the student's full name, surname, and ID (matricola) in the header[cite: 47, 142].and Python components must be delivered together in a single compressed archive.
