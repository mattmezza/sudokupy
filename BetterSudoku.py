from Sudoku import Sudoku
import math

class BetterSudoku(Sudoku):
	
	def __init__(self, line, verbose=False):
		Sudoku.__init__(self, line, verbose)
		self.col_labels=[i%self.n for i in range(self.n*self.n)]
		self.row_labels=[i/self.n for i in range(self.n*self.n)]
		self.sqr_labels=[(self.n/self.sn)*(self.row_labels[i]/self.sn)+self.col_labels[i]/self.sn for i in range(self.n*self.n)]
		self.inConflict = list()
		self.forbidden = list()
		for i in range(self.n*self.n):
			self.inConflict.append(set(self.inConflictAt(i)))
			self.forbidden.append(list(self.forbiddenAt(i)))

	def isInSameRow(self, a, b, c=None):
		if c==None:
			return self.row_labels[a]==self.row_labels[b]
		return (self.row_labels[a]==self.row_labels[b] and self.row_labels[b]==self.row_labels[c])

	def isInSameCol(self, a, b, c=None):
		if c==None:
			return self.col_labels[a]==self.col_labels[b]
		return (self.col_labels[a]==self.col_labels[b] and self.col_labels[b]==self.col_labels[c])

	def isInSameSquare(self, a, b, c=None):
		if c==None:
			return self.sqr_labels[a]==self.sqr_labels[b]
		return (self.sqr_labels[a]==self.sqr_labels[b] and self.sqr_labels[b]==self.sqr_labels[c])

	def forbiddenAt(self, index):
		forbiddenAt = list()
		for cell in self.inConflict[index]:
			if self.partial[cell]!=self.emptySymbol:
				forbiddenAt.append(self.partial[cell])
		return forbiddenAt
	
	def removeForbiddenFrom(self, value, index):
		for cell in self.inConflict[index]:
			self.forbidden[cell].remove(value)

	def addForbiddenTo(self, value, index):
		for cell in self.inConflict[index]:
			self.forbidden[cell].append(value)

	def inConflictAt(self, index):
		conflict=set()
		for i in range(self.n*self.n):
			if self.row_labels[i]==self.row_labels[index] or self.col_labels[i]==self.col_labels[index] or self.sqr_labels[i]==self.sqr_labels[index]:
				if i!=index:
					conflict.add(i)
		return conflict
	
	def isNotExtendible(self):
		for index,forbidden in enumerate(self.forbidden):
			if len(set(forbidden))==self.n:
				if self.verbose:
					print "Sudoku is not extendible because ", index," has ",self.n," different forbidden values ",forbidden
				return True
		return False

	def gamma(self, current):
		for digit in range(1, self.n+1):
			if digit not in self.forbidden[current]:
				yield digit

	def setNextEmpty(self, current, value):
		oldValue = self.partial[current]
		if oldValue!=self.emptySymbol:
			if self.verbose:
				print "removing ",oldValue," from forbidden of in conflict at ",current
			self.removeForbiddenFrom(oldValue, current)
		self.partial[current] = value
		if value!=self.emptySymbol:
			if self.verbose:
				print "adding ",value," to forbidden of in conflict at ",current
			self.addForbiddenTo(value, current)
