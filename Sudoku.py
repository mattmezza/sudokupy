from SearchProblem import SearchProblem
import math

class Sudoku(SearchProblem):
	"""Basic sudoku class"""

	emptySymbol=0	#empty cell

	def __init__(self, line, verbose=False):
		self.verbose=verbose
		self.count=0
		self.n=int(math.sqrt(len(line)))	#side of the grid
		self.sn=int(math.sqrt(self.n))		#side of a sub-grid
		self.instance=[]					#instance
		self.partial=[]						#working copy
		line=line.replace('\n','')	
		for symbol in line:
			self.instance.append(int(symbol))
		self.partial=list(self.instance)


	def computeNextEmpty(self):
		try: i=self.partial.index(0)
		except: i=None
		if self.verbose:
			print "nextEmpty is ",i
		return i

	def setNextEmpty(self, nextEmpty, digit):
		self.partial[nextEmpty]=digit

	def gamma(self, currentEmpty):
		i = currentEmpty
		bag = [self.partial[j] for j in filter(lambda x: (self.col_labels[i]==self.col_labels[x]) or (self.row_labels[i]==self.row_labels[x]) or (self.sqr_labels[i]==self.sqr_labels[x]), range(self.n*self.n))]
		return filter(lambda x: x not in bag, range(1, self.n+1))

	def __str__(self):
		s=""
		for r in range(self.n):
			if r%self.sn==0 and r>0:
				cell=''
				for i in range(self.sn):
					cell+=str('-' * (self.sn*2))
					if i+1!=self.sn and i>0:
						cell+='-'
					if i+1!=self.sn:
						cell+='|'
				s+=cell+"\t"+cell+"\n"
			for c in range(self.n):
				if c%self.sn==0 and c>0:
					s+='| '
				if self.instance[r*self.n+c]==Sudoku.emptySymbol:
					s+='. '
				else:
					s+=str(self.instance[r*self.n+c])+" "
			s+="	"
			for c in range(self.n):	
				if c%self.sn==0 and c>0:
					s+='| '
				if self.partial[r*self.n+c]==Sudoku.emptySymbol:
					s+='. '
				else:
					s+=str(self.partial[r*self.n+c])+" "
			s+="\n"
		return s

	def commaSeparatedSolution(self):
		return str(self.partial).replace(" ", "").replace("[", "").replace("]", "")

