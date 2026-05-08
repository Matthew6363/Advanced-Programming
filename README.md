# Advanced-Programming

# Advanced and Parallel Programming Project

This repository contains the two-part final project for the Advanced and Parallel Programming course. The work involves high-performance computing in **C** and the development of a custom interpreter in **Python**.

---

## Part 1: Parallel Mandelbrot Fractal (C)
The goal is to develop a program that renders the Mandelbrot set as a grayscale image in `.pgm` format

### Technical Features
* **Parallel Computing:** The core calculation is parallelized using **OpenMP** to optimize performance.
* **Memory Efficiency:** Image saving is handled via **mmap**.
* **Mathematical Model:** * Calculates the sequence $z_{n+1} = z_n^2 + c$ with a divergence radius $r=2$.
    * Interior points are colored white (255).
    * Exterior points use a logarithmic color scale $\lfloor255 \times \frac{\log(n)}{\log(M)}\rfloor$ based on the divergence speed $n$.
* **CLI Support:** Accepts the filename, max iterations ($M$), and vertical resolution ($n_{rows}$) as command-line arguments.
* **Architecture:** Modular design with separate modules for fractal logic (`mandelbrot.c/h`) and image management (`pgm.c/h`), compiled via **Makefile**.

---

## Part 2: Custom Language Interpreter (Python)
This part involves extending a Lisp-like interpreter to support advanced programming constructs.

### Language Features
* **Variables & Arrays:** * Variable allocation (`alloc`) and array allocation (`valloc`).
    * Value assignment for variables (`setq`) and specific array indices (`setv`).
* **Control Flow:**
    * **Conditionals:** `if` statements for branching logic.
    * **Loops:** `while` and `for` loops for iterative execution.
* **Subroutines:** Ability to define reusable code blocks (`defsub`) and execute them via `call`.
* **Comparisons:** Support for boolean operators: `>`, `>=`, `=`, `!=`, `<`, and `<=`.
* **Sequencing:** Built-in support for executing sequences of 2, 3, or 4 operations (`prog2`, `prog3`, `prog4`).

---

## Requirements & Submission
* **Documentation:** All significant functions are documented with descriptions of tasks, inputs, and outputs.
* **Error Handling:** The C program returns non-zero codes on failure, while the Python interpreter raises specific, coherent exceptions.
* **Compliance:** Every source file includes the student's full name, surname, and ID (matricola) in the header.and Python components must be delivered together in a single compressed archive.
