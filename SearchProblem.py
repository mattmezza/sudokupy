class SearchProblem:

	calls=0

	def exhaustiveSearch(self):
		for s in self.enumerateSI():
			if self.isAdmissible():
				return s
		return False

	def backTrack(self):
		self.calls+=1
		currentEmpty=self.computeNextEmpty()
		if currentEmpty==None:
			return True
		for gamma in self.gamma(currentEmpty):
			if self.verbose:
				print "Trying to set ",gamma," into [",currentEmpty,"]..."
			self.setNextEmpty(currentEmpty, gamma)
			if not self.isNotExtendible():
				if self.verbose:
					print gamma," seems to be good for [",currentEmpty,"]..."
				if self.backTrack():
					return True
			if self.verbose:
				print gamma," is not good for [",currentEmpty,"]..."
			self.setNextEmpty(currentEmpty, self.emptySymbol)
		return False
