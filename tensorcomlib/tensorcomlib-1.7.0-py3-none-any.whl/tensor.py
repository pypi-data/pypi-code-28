import numpy as np
from prettytable import PrettyTable
from .tools import prod

#Tensor Class

class tensor(object):

	data = None
	shape = None
	dtype = None

	def __init__(self, data = None, shape = None):

		if shape == None:
			shape = data.shape
		super(tensor, self).__init__()
		self.data = np.array(data)
		self.shape = tuple(shape)
		self.dtype = data.dtype

	def size(self):
		return prod(self.shape)

	def copy(self):
		return tensor(self.data.copy(),self.shape)

	def dimsize(self, ind):
		return self.shape[ind]

	def ndims(self):
		return len(self.shape)

	def tendtype(self):
		return self.dtype

	def information(self):
		print('\tTensor\tInformation')
		table = PrettyTable(['Order', 'Shape', 'Size'])
		table.add_row([self.ndims(), self.shape, self.size()])
		table.reversesort = False
		table.border = 1
		print(table)