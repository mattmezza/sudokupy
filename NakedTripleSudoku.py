from NakedTwinsSudoku import NakedTwinsSudoku

class NakedTripleSudoku(NakedTwinsSudoku):
	
	def __init__(self, line, verbose=False):
		NakedTwinsSudoku.__init__(self, line, verbose)
		self.triple={}

	
	def searchTriple(self, current):
		triple=[]
		inConflict=self.inConflict[current]

		for firstIndex in inConflict:
			for secondIndex in inConflict:
				if self.partial[firstIndex]==self.emptySymbol and self.partial[secondIndex]==self.emptySymbol:
					if self.available[firstIndex]==self.available[secondIndex] and firstIndex!=secondIndex:
						for thirdIndex in inConflict:
							if self.partial[thirdIndex]==self.emptySymbol:
								if self.available[secondIndex]==self.available[thirdIndex] and firstIndex!=secondIndex and secondIndex!=thirdIndex and firstIndex!=thirdIndex:
									if len(self.available[firstIndex])==3:
										triple.append(firstIndex)
										triple.append(secondIndex)
										triple.append(thirdIndex)
										triple.append(self.available[firstIndex])
										if self.verbose:
											print self
											print "found triple ", triple[3], " in ",triple[0], " and ",triple[1]," and ",triple[2]
										return triple
		return None

	def addTripleConstraint(self, index, triple):	
		inSameRow=False
		if self.isInSameRow(triple[0], triple[1], triple[2]):
			inSameRow=True
			start = (triple[0]//self.n)*self.n
			if self.verbose:
				print "adding triple ",triple[3]," as forbidden in row ",(triple[0]//self.n)," and updating available values"
			for i in range(start, start+self.n):
				if i!=triple[0] and i!=triple[1] and i!=triple[2] and self.partial[i]==self.emptySymbol:
					for val in triple[3]:
						self.forbidden[i].append(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameCol(triple[0], triple[1], triple[2]):
			start = triple[0]%self.n
			if self.verbose:
				print "adding triple ",triple[3]," as forbidden in col ",(triple[0]%self.n)," and updating available values"
			for i in range(start, self.n, self.n*self.n):
				if i!=triple[0] and i!=triple[1] and i!=triple[2] and self.partial[i]==self.emptySymbol:
					for val in triple[3]:
						self.forbidden[i].append(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameSquare(triple[0], triple[1], triple[2]):
			squareIndices=[]
			for i in range(self.n*self.n):
				if self.sqr_labels[triple[0]]==self.sqr_labels[i]:
					squareIndices.append(i)
			rowIndices=[]
			colIndices=[]
			if inSameRow:
				start=(triple[0]//self.n)*self.n
				end=start+self.n
				for n in range(start, end):
					rowIndices.append(n)
			else:
				start=triple[0]%self.n
				for n in range(start, self.n, self.n*self.n):
					colIndices.append(n)
			if self.verbose:
				print "adding triple ",triple[3]," as forbidden in square ",(self.sqr_labels[triple[0]])," and updating available values"
			for i in squareIndices:
				if i!=triple[0] and i!=triple[1] and i!=triple[2] and self.partial[i]==self.emptySymbol and i not in rowIndices and i not in colIndices:
					for val in triple[3]:
						self.forbidden[i].append(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
								
	def removeTripleConstraint(self, index, triple):
		inSameRow=False
		if self.isInSameRow(triple[0], triple[1], triple[2]):
			inSameRow=True
			start = (triple[0]//self.n)*self.n
			if self.verbose:
				print "removing triple ",triple[3]," as forbidden in row ",(triple[0]//self.n)," and updating available values"
			for i in range(start, start+self.n):
				if i!=triple[0] and i!=triple[1] and i!=triple[2] and self.partial[i]==self.emptySymbol:
					for val in triple[3]:
						self.forbidden[i].remove(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameCol(triple[0], triple[1], triple[2]):
			start = triple[0]%self.n
			if self.verbose:
				print "removing triple ",triple[3]," as forbidden in col ",(triple[0]%self.n)," and updating available values"
			for i in range(start, self.n, self.n*self.n):
				if i!=triple[0] and i!=triple[1] and i!=triple[2] and self.partial[i]==self.emptySymbol:
					for val in triple[3]:
						self.forbidden[i].remove(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))
		if self.isInSameSquare(triple[0], triple[1], triple[2]):
			squareIndices=[]
			for i in range(self.n*self.n):
				if self.sqr_labels[triple[0]]==self.sqr_labels[i]:
					squareIndices.append(i)
			rowIndices=[]
			colIndices=[]
			if inSameRow:
				start=(triple[0]//self.n)*self.n
				end=start+self.n
				for n in range(start, end):
					rowIndices.append(n)
			else:
				start=triple[0]%self.n
				for n in range(start, self.n, self.n*self.n):
					colIndices.append(n)
			if self.verbose:
				print "removing triple ",triple[3]," as forbidden in square ",(self.sqr_labels[triple[0]])," and updating available values"
			for i in squareIndices:
				if i!=triple[0] and i!=triple[1] and i!=triple[2] and self.partial[i]==self.emptySymbol and i not in rowIndices and i not in colIndices:
					for val in triple[3]:
						self.forbidden[i].remove(val)
					self.available[i]=set(set(range(1,self.n+1))-set(self.forbidden[i]))

	def setNextEmpty(self, current, value):
		oldValue = self.partial[current]
		if oldValue!=self.emptySymbol:
			try: oldTriple=self.triple[current]
			except: oldTriple=None
			if oldTriple!=None:
				self.removeTripleConstraint(current, oldTriple)
				del self.triple[current]
		NakedTwinsSudoku.setNextEmpty(self, current, value)
		if value!=self.emptySymbol:
			triple = self.searchTriple(current)
			if triple!=None:
				self.triple[current]=triple
				self.addTripleConstraint(current, triple)
