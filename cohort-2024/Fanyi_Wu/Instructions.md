# Coursework

This repository is for the submission of your coursework for the C1 Research Computing Module

You have been given access with the role maintainer for this repository which will expire on the 17th of December, which is the submission deadline for this work

You should use this repository for both your code, and for your report.

## The problem
Please write a programme that solves Sudoku.

The programme should be able to take as input an incomplete grid in the form of a text file with a 9x9 grid of numbers with zero representing unknown values and `|`,`+`,`-` separating cells and , i.e.:
```
$ cat input.txt
000|007|000
000|009|504
000|050|169
---+---+---
080|000|305
075|000|290
406|000|080
---+---+---
762|080|000
103|900|000
000|600|000
```

and output the completed grid, to a file or terminal, in the same form.

The code should be simple to use, written in Python (or Python utilising user created C/Fortran libraries with python bindings), and be run-able from the command line, i.e.:
```
$ python src/solve_sudoku.py input.txt
```

## Criteria
The goal of this coursework project is for you to demonstrate that you have mastered good software development practices and can utilise the modern tools described in the module `C1 Research Computing` to support your code development.  

You will need to demonstrate the following:
- Writing clear readable code that is compliant with PEP8 style (for python)
- Providing appropriate documentation that is compatible with auto-documentation tools like Doxygen. (The documentation does not need to have been built by Doxygen in the repository)
- The project must be well structured (sensible folder structure, `README`, `licence`, `.gitignore`, `.pre_commit_config`, `Doxyfile`, `enviroment.yml`, `Dockerfile`, etc..) following standard best practice.
- Appropriate and robust unit tests for automatic validation of your code.
- You used appropriate version control best practice, including branching for development and testing.
- Demonstrate robust software development process including: prototyping, profiling and testing of different algorithms/packages, modularity, and validation and error/exception trapping in final code
- The code is portable and reproducible by utilising environment and containerisation tools like Conda and Docker.  The code should be runnable in the container without any effort beyond generating the image.

You will not be marked on:
- The sophistication of your algorithm or performance (beyond some sensible human timescale, i.e., "not hours”) Indeed you are more than welcome to read the wiki on common methods if you want: https://en.wikipedia.org/wiki/Sudoku_solving_algorithms.  Alternatively, you can try to design yours from scratch for fun.  All I am interested in is the creation process, and the quality (in the technical sense) of the final code.  I don't even really mind if it can't solve every starting grid, provided it tells you that it is stuck (rather than hangs or crashes).

Please **DO NOT** cut and paste code from existing solvers.  Remember I am not interested in the solution itself, but the quality of its creation.  Also, please remember the relevant section of the handbook that refers to use of ChatGPT in you academic work, specifically the following passage:


"*Generation tools must be used transparently:* 
 - *All use of auto-generation tools must be explicitly cited in every instance of their use.*
 - *This applies to generating code, whether used for prototyping, creation, reformatting, or any other purpose.  Students should add the citations to the README in home repository, and in any accompanying reports stating the prompts submitted, where the output was used, and how it was modified.*
 - *When used in conjunction with submitted reports for drafting, proofreading, suggesting alternative wordings, or for any other task it should be explicitly noted in an appendix to the report with the prompts submitted, where the output was used, and how it was modified.*
 - *Failure to adequately cite use of these tools is considered academic misconduct.*
"

## Submission
Ideally this repository will have a Dockerfile which will create the environment and clone the repository into it, with all inputs required to run the project. This should be accompanied by a short report of **not more than 3,000 words** describing the project and its development. You should ensure your report is logically structured and touches on the points mentioned above in the assessment criteria. Specifically, I would expect reports to cover the following topics:
- Short Introduction
- Selection of Solution Algorithm and Prototyping
- Development, Experimentation and Profiling
- Validation, Unit Tests and CI set up
- Packaging and Usability
- Summary

The report should be written in latex, with the generated PDF of the report placed in a folder called `report` in the repository.
