from MinimumValueSudoku import MinimumValueSudoku

class NakedTwinsSudoku(MinimumValueSudoku):
	
	def __init__(self, line, verbose=False):
		MinimumValueSudoku.__init__(self, line, verbose)
		self.twins={}

	
	def searchTwins(self, current):
		twins=[]
		inConflict=self.inConflict[current]
		for firstIndex in inConflict:
			for secondIndex in inConflict:
				if self.partial[firstIndex]==self.emptySymbol and self.partial[secondIndex]==self.emptySymbol:
					if self.available[firstIndex]==self.available[secondIndex] and firstIndex!=secondIndex:
						if len(self.available[firstIndex])==2:
							twins.append(firstIndex)
							twins.append(secondIndex)
							twins.append(self.available[firstIndex])
							if self.verbose:
								print self
								print "found twins ", twins[2], " in ",twins[0], " and ",twins[1]
							return twins
		return None

	def addTwinsConstraint(self, index, twins):	
		inSameRow=False
		if self.isInSameRow(twins[0], twins[1]):
			inSameRow=True
			start = (twins[0]//self.n)*self.n
			if self.verbose:
				print "adding twins ",twins[2]," as forbidden in row ",(twins[0]//self.n)," and updating available values"
			for i in range(start, start+self.n):
				if i!=twins[0] and i!=twins[1] and self.partial[i]==self.emptySymbol:
					for val in twins[2]:
						self.forbidden[i].append(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameCol(twins[0], twins[1]):
			start = twins[0]%self.n
			if self.verbose:
				print "adding twins ",twins[2]," as forbidden in col ",(twins[0]%self.n)," and updating available values"
			for i in range(start, self.n, self.n*self.n):
				if i!=twins[0] and i!=twins[1] and self.partial[i]==self.emptySymbol:
					for val in twins[2]:
						self.forbidden[i].append(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameSquare(twins[0], twins[1]):
			squareIndices=[]
			for i in range(self.n*self.n):
				if self.sqr_labels[twins[0]]==self.sqr_labels[i]:
					squareIndices.append(i)
			rowIndices=[]
			colIndices=[]
			if inSameRow:
				start=(twins[0]//self.n)*self.n
				end=start+self.n
				for n in range(start, end):
					rowIndices.append(n)
			else:
				start=twins[0]%self.n
				for n in range(start, self.n, self.n*self.n):
					colIndices.append(n)
			if self.verbose:
				print "adding twins ",twins[2]," as forbidden in square ",(self.sqr_labels[twins[0]])," and updating available values"
			for i in squareIndices:
				if i!=twins[0] and i!=twins[1] and self.partial[i]==self.emptySymbol and i not in rowIndices and i not in colIndices:
					for val in twins[2]:
						self.forbidden[i].append(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
								
	def removeTwinsConstraint(self, index, twins):
		inSameRow=False
		if self.isInSameRow(twins[0], twins[1]):
			inSameRow=True
			start = (twins[0]//self.n)*self.n
			if self.verbose:
				print "removing twins ",twins[2]," as forbidden in row ",(twins[0]//self.n)," and updating available values"
			for i in range(start, start+self.n):
				if i!=twins[0] and i!=twins[1] and self.partial[i]==self.emptySymbol:
					for val in twins[2]:
						self.forbidden[i].remove(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameCol(twins[0], twins[1]):
			start = twins[0]%self.n
			if self.verbose:
				print "removing twins ",twins[2]," as forbidden in col ",(twins[0]%self.n)," and updating available values"
			for i in range(start, self.n, self.n*self.n):
				if i!=twins[0] and i!=twins[1] and self.partial[i]==self.emptySymbol:
					for val in twins[2]:
						self.forbidden[i].remove(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameSquare(twins[0], twins[1]):
			squareIndices=[]
			for i in range(self.n*self.n):
				if self.sqr_labels[twins[0]]==self.sqr_labels[i]:
					squareIndices.append(i)
			rowIndices=[]
			colIndices=[]
			if inSameRow:
				start=(twins[0]//self.n)*self.n
				end=start+self.n
				for n in range(start, end):
					rowIndices.append(n)
			else:
				start=twins[0]%self.n
				for n in range(start, self.n, self.n*self.n):
					colIndices.append(n)
			if self.verbose:
				print "removing twins ",twins[2]," as forbidden in square ",(self.sqr_labels[twins[0]])," and updating available values"
			for i in squareIndices:
				if i!=twins[0] and i!=twins[1] and self.partial[i]==self.emptySymbol and i not in rowIndices and i not in colIndices:
					for val in twins[2]:
						self.forbidden[i].remove(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))

	def setNextEmpty(self, current, value):
		oldValue = self.partial[current]
		if oldValue!=self.emptySymbol:
			try: oldTwins=self.twins[current]
			except: oldTwins=None
			if oldTwins!=None:
				self.removeTwinsConstraint(current, oldTwins)
				del self.twins[current]
		MinimumValueSudoku.setNextEmpty(self, current, value)
		if value!=self.emptySymbol:
			twins = self.searchTwins(current)
			if twins!=None:
				self.twins[current]=twins
				self.addTwinsConstraint(current, twins)
