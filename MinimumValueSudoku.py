from BetterSudoku import BetterSudoku

class MinimumValueSudoku(BetterSudoku):


	def __init__(self, line, verbose=False):
		BetterSudoku.__init__(self, line, verbose)
		self.available=list()
		complete=set(range(1,self.n+1))
		for i in range(self.n*self.n):
			forbidden=set(self.forbidden[i])
			self.available.append(set(complete-forbidden))

	def computeNextEmpty(self):
		try: i=self.partial.index(self.emptySymbol)
		except: return None
		minimumIndex = self.findMinimum()
		if self.verbose:
			print "nextEmpty is ", minimumIndex, " because it has the minimum number of admissible values"
		return minimumIndex

	def findMinimum(self):
		minimumLen = self.n
		minimumIndex = 0
		for index,available in enumerate(self.available):
			if len(available)<minimumLen and self.partial[index]==self.emptySymbol:
				minimumIndex=index
				minimumLen=len(available)
		return minimumIndex

	def updateAvailableFor(self, current):
		if self.verbose:
			print "updating available values after forbidden edit"
		for cell in self.inConflict[current]:
			self.available[cell]=set(set(range(1,self.n+1))-set(self.forbidden[cell]))

	def setNextEmpty(self, current, value):
		BetterSudoku.setNextEmpty(self, current, value)
		self.updateAvailableFor(current)


