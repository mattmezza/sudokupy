Sudoku solver
=========

Gimme any 81 digits sequence that represents a sudoku and I will solve it!

`python driver.py some_sudokus.txt nakedtriple` is the command to run to start solving every sudoku into `some_sudokus.txt` file. Optionally, you can add a last parameter to the list to obtain a verbose logging (add `True` if you want so).

the second parameter is the type of solver chosen, you can choose among:

- **standard**: a normal search problem implementation with backtrack;
- **better**: an improved version of the above method;
- **minimum**: a solver that implements the above improvements and the minimum value technique;
- **nakedtwins**: a solver that implements all the above improvements plus the naked twins technique to reduce the number of backtrack call;
- **nakedtriple**: a faster-super-dupy-fast version using (in addition to the above mentioned techniques) the naked triple method.

### TODOs
- [ ] improve command line interface
- [ ] write some info and documentation with regards to the techniques used
- [ ] packetize the software in a python module to easily install & import
- [ ] using multiple thread at sudoku list level and at sudoku level
- [ ] find the hardest sudoku ever!!!


The repo comes with a `some_sudokus.txt` database of more than 10k sudokus I have taken from the web and around (also on newspaper).

MIT Licensed © Matteo Merola 2016
