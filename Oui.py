napoleoVersion = "3.1.4"

"""
===========================================================================================
Napoleo
Version 3.1.4 "Normandie"
	A class with a bunch of functions for operating *.cdf and *.oui Napoleo data files.
	All the data can be accessed from the [name].tree, which is a dictionary, as well as
	with the help of [name].get([path]), considering "path" is the value full path, e. g.
	"Name.block1.values.thisOne".
	The flags are saved in a "flags" list, such as "Name.block1.values.thisOne.flags".
	For more info see 

Terms of use and license agreement below.
This project uses "Parse 1.6.6" by Richard Jones <richard@python.org> (see end of file).

===========================================================================================
"""


from parse import *
from parse import compile


class OuiSyntaxError (SyntaxError):
	pass


class NAPOLEO():
	def __init__(self, sourcefile, cdffileway="Default", special = None):
		if cdffileway == "Default":
			self.cdffileway = sourcefile[0:-4]+".cdf"
		else:
			self.cdffileway = cdffileway
		if special == "update":
			self.tree = {}
			self.updateTree()
			self.name = cdffileway[0:-4]
		elif special == "empty":
			self.tree = {}
			self.name = ""
		else:
			self.name = sourcefile[0:-4]
			self.sourcefile = sourcefile
			self.sourcefile = self.precompile()
			self.tree = self.compile()
			self.save(self.cdffileway)
	__version = "2.1.1t"

	def precompile(self):
		try:
			current = open(self.sourcefile , 'rt' , encoding="UTF-8")
			sourcefile = []
			for line in current:
				if len(line.split()) and not line.split()[0][0:2] == "//":
					sourcefile += line.split()
			current.close()
			com = False
			final = []
			try:
				self.version = parse("(napoleoversion)({value})", sourcefile[0])["value"]
				sourcefile = sourcefile[1:]
			except:
				pass

			for i in range(len(sourcefile)):
				if len(sourcefile[i])-1 and sourcefile[i][0:2] == "/*":
					com = True
				elif com and "*/" in sourcefile[i]:
					com = False
				elif not com:
					final.append(sourcefile[i])

			i = 0
			while i < len(final):
				try:
					if final[i][-1] == ")" or final[i][-1] == "{" or final[i][-1] == "}" or final[i][-1] == ">":
						i += 1
					else:
						temporary = [final[i]+" "+final[i+1]]
						final = final[0:i] + temporary + final[i+2:]
				except IndexError:
					pass
			return(final)

		except IOError or EOFError:
			print("Error: no file found:\n" + self.sourcefile)
	def getTree(self):
		return self.tree
	def setTree(self, filenew):
		self.cdffileway = filenew
		self.updateTree()
	def updateTree(self):
		try:
			current = open(self.cdffileway , 'rt' , encoding="UTF-8")
			for line in current:
				self.tree.update(eval(line))
			current.close()
		except IOError or EOFError:
			print("Error: no file found:\n" + self.cdffileway)

	def stdstream(self, strg, path):
		try:
			r = parse("({path})({value})", strg).named
			if len(r) < 2:
				raise OuiSyntaxError("Incorrect Oui syntax in " + str(path))
			return(r["path"], r["value"].split())
		except:
			raise OuiSyntaxError("Incorrect Oui syntax in " + str(path))
	def block(self, strg):
		try:
			r = parse("({nom}){", strg).named
			return(r["nom"])
		except:
			raise OuiSyntaxError("Incorrect Oui block")
	def flag(self, strg, path):
		try:
			r = parse("<{flag}>", strg).named
			if len(r) < 1:
				raise OuiSyntaxError("Incorrect Oui flag in " + str(path))
			return(path+["flags"], r["flag"])
		except:
			raise OuiSyntaxError("Incorrect Oui flag in " + str(path))

	def get(self, path):
		pattern = self.patternize(path)
		block = self.tree
		try:
			for blk in pattern:
				block = block[blk]
			return(block)
		except:
			print("Wrong path")

	def getValue(self, block, path):
		pattern = self.patternize(path)
		try:
			for blk in pattern:
				block = block[blk]
			return(block)
		except:
			print("Wrong path")

	def patternize(self, path):
		path += "."
		pattern = []
		cur = 0
		for symb in path:
			if symb == ".":
				pattern.append(path[0:cur])
				path = path[cur+1:]
				cur = 0
			else:
				cur += 1
		return(pattern)
	
	def setValue(self, tree, path, value):
		if len(path) == 1:
			if type(tree) == type([]):
				tree = {}
			if path[-1] == "flags":
				value = [value]
			if path[0] in tree and type(tree[path[0]])==type([]):
				tree[path[0]] += value
				return(tree)
			else:
				tree[path[0]] = value
		elif path[0] in tree:
			tree[path[0]] = self.setValue(tree[path[0]], path[1:], value)
		else:
			tree[path[0]] = {}
			tree[path[0]] = self.setValue(tree[path[0]], path[1:], value)
		return(tree)

	def save(self, path):
		cdf = open(path , 'w' , encoding="UTF-8")
		cdf.write(str(self.tree))
		cdf.close()

	def compile(self):
		tree = {}
		path = []
		for bray in self.sourcefile:
			try:
				if "{" in bray:
					path.append(self.block(bray))
					tree = self.setValue(tree, path, {})
				elif "<" in bray and ">" in bray:
					flag = self.flag(bray, path)
					tree = self.setValue(tree, flag[0], flag[1])
				elif bray == "}":
					path = path[:-1]
				else:
					vay = self.stdstream(bray, path)
					path.append(vay[0])
					tree = self.setValue(tree, path, vay[1])
					path = path[:-1]
			except(OuiSyntaxError):
				print("Incorrect OUI syntax in", bray)
		return(tree)



"""

Terms of use note:

	This code and the entire Project Napoleo, including the conception of Oui syntax,
	was developed by Kudryavcev Eremey <keremey57@gmail.com> in 2015.
	One may freely use parts of this code and modificate them with the only limit that
	this terms of use notice and the permission notice should be included in all copies
	or substantial portions of the files related to the Project? as well as the following
	license.


License of "Parse" by Richard Jones:

	Copyright (c) 2012-2013 Richard Jones <richard@python.org>
	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	
	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.

"""
