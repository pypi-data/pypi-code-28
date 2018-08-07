from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class EgressTracking(Base):
	"""Provides different options for Egress Tracking.
	"""

	_SDM_NAME = 'egressTracking'

	def __init__(self, parent):
		super(EgressTracking, self).__init__(parent)

	@property
	def FieldOffset(self):
		"""Returns the one and only one FieldOffset object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.fieldoffset.FieldOffset)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.egresstracking.fieldoffset.fieldoffset import FieldOffset
		return self._read(FieldOffset(self), None)

	@property
	def AvailableEncapsulations(self):
		"""(Read only) Specifies the available Encapsulations for Egress Tracking.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableEncapsulations')

	@property
	def AvailableOffsets(self):
		"""(Read only) Specifies the available Offsets for Egress Tracking.

		Returns:
			list(str)
		"""
		return self._get_attribute('availableOffsets')

	@property
	def CustomOffsetBits(self):
		"""Specifies the Custom Offset in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .

		Returns:
			number
		"""
		return self._get_attribute('customOffsetBits')
	@CustomOffsetBits.setter
	def CustomOffsetBits(self, value):
		self._set_attribute('customOffsetBits', value)

	@property
	def CustomWidthBits(self):
		"""Specifies the Custom Width in bits for Egress Tracking when Encapsulation is Any: Use Custom Settings .

		Returns:
			number
		"""
		return self._get_attribute('customWidthBits')
	@CustomWidthBits.setter
	def CustomWidthBits(self, value):
		self._set_attribute('customWidthBits', value)

	@property
	def Encapsulation(self):
		"""Specifies the Encapsulation for Egress Tracking.

		Returns:
			str
		"""
		return self._get_attribute('encapsulation')
	@Encapsulation.setter
	def Encapsulation(self, value):
		self._set_attribute('encapsulation', value)

	@property
	def Offset(self):
		"""Specifies the Offset for Egress Tracking.

		Returns:
			str
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	def remove(self):
		"""Deletes a child instance of EgressTracking on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()
