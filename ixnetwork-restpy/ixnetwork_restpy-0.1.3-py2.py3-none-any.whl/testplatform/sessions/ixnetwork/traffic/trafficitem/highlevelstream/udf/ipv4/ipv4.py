from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ipv4(Base):
	"""This object provides different options for UDF in IPv4 Type.
	"""

	_SDM_NAME = 'ipv4'

	def __init__(self, parent):
		super(Ipv4, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""Species all the possible widths available for a UDF in particular Type.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def BitmaskCount(self):
		"""Specifies the number of bits to be masked to any integer value between 2 to 32.

		Returns:
			number
		"""
		return self._get_attribute('bitmaskCount')
	@BitmaskCount.setter
	def BitmaskCount(self, value):
		self._set_attribute('bitmaskCount', value)

	@property
	def InnerLoopIncrementBy(self):
		"""Specifies the Step Value by which the Inner Loop will be incremented.

		Returns:
			number
		"""
		return self._get_attribute('innerLoopIncrementBy')
	@InnerLoopIncrementBy.setter
	def InnerLoopIncrementBy(self, value):
		self._set_attribute('innerLoopIncrementBy', value)

	@property
	def InnerLoopLoopCount(self):
		"""Specifies the no. of times the inner loop will occur.

		Returns:
			number
		"""
		return self._get_attribute('innerLoopLoopCount')
	@InnerLoopLoopCount.setter
	def InnerLoopLoopCount(self, value):
		self._set_attribute('innerLoopLoopCount', value)

	@property
	def OuterLoopLoopCount(self):
		"""Specifies the no. of times the outer loop will occur.

		Returns:
			number
		"""
		return self._get_attribute('outerLoopLoopCount')
	@OuterLoopLoopCount.setter
	def OuterLoopLoopCount(self, value):
		self._set_attribute('outerLoopLoopCount', value)

	@property
	def SkipValues(self):
		"""If true, Skip Values option is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('skipValues')
	@SkipValues.setter
	def SkipValues(self, value):
		self._set_attribute('skipValues', value)

	@property
	def StartValue(self):
		"""Specifies the start value of the UDF.

		Returns:
			number
		"""
		return self._get_attribute('startValue')
	@StartValue.setter
	def StartValue(self, value):
		self._set_attribute('startValue', value)

	@property
	def Width(self):
		"""Specifies the width of the UDF.

		Returns:
			str(32)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)
