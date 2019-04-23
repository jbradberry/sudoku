Sudoku solvers
==============

This repo contains some Python implementations of Sudoku solving
algorithms that I've played around with.


The files
---------

sudoku.py
  My original implementation of a Sudoku solver.

dancinglinks.py
  An implementation of Knuth's Dancing Links algorithm.  This is
  considerably faster than my original implementation.

test_sudoku.txt
  An example sudoku problem, taken from one of the filler cards in a
  deck of standard Bicycle playing cards.

test_sudoku2.txt
  Another example sudoku problem, this one billed as "the world's most
  difficult Sudoku problem".


Usage
-----

No installation is required and there are no dependencies other than
Python 2 itself.
::

   $ time python sudoku.py test_sudoku.txt
   632845179
   471369285
   895721463
   748153692
   163492758
   259678341
   524916837
   986237514
   317584926

   228 calls

   real	0m0.103s
   user	0m0.095s
   sys	0m0.008s


   $ time python dancinglinks.py test_sudoku.txt
   632845179
   471369285
   895721463
   748153692
   163492758
   259678341
   524916837
   986237514
   317584926

   56 calls

   real	0m0.032s
   user	0m0.028s
   sys	0m0.004s
