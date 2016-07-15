from Sudoku import Sudoku
from BetterSudoku import BetterSudoku
from MinimumValueSudoku import MinimumValueSudoku
from NakedTwinsSudoku import NakedTwinsSudoku
from NakedTripleSudoku import NakedTripleSudoku
import time					#for time
import sys					#for argv

try: kind=sys.argv[2]
except: kind="standard"
try: verbose=sys.argv[3]
except: verbose=False
if verbose!="True":
	verbose=False


try: filename=sys.argv[1]
except: print "No filename param"; sys.exit(1)

print "Trying to solve with ", kind, " instance of sudoku"

with open(filename) as myfile:
	lines = myfile.readlines()
	total=len(lines)
	for i,line in enumerate(lines):
		if kind=="standard":
			sudoku = Sudoku(line, verbose)
		elif kind=="better":
			sudoku = BetterSudoku(line, verbose)
		elif kind=="minimum":
			sudoku = MinimumValueSudoku(line, verbose)
		elif kind=="nakedtwins":
			sudoku = NakedTwinsSudoku(line,verbose)
		elif kind=="nakedtriple":
			sudoku = NakedTripleSudoku(line, verbose)
		else:
			print "No such method for ", kind
			sys.exit(1)
		
		print "Solving ",i+1,"of",total,"...\n"
		if verbose:
			print "\nInitial grid:\n",sudoku
		start_time=time.time()
		solved=sudoku.backTrack()
		elapsed=time.time()-start_time
		if solved:
			print sudoku	
			print "Solution for ",i+1,"of",total," computed in ",elapsed," seconds and ",sudoku.calls,"recursive calls!\n\n"
			print sudoku.commaSeparatedSolution()
		else:
			print "No solution found :-(\n\n"
