from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InterfaceDiscoveredAddress(Base):
	"""The tab that shows description and ip of interface configured on this port.
	"""

	_SDM_NAME = 'interfaceDiscoveredAddress'

	def __init__(self, parent):
		super(InterfaceDiscoveredAddress, self).__init__(parent)

	@property
	def Description(self):
		"""Shows description of the interface.

		Returns:
			str
		"""
		return self._get_attribute('description')

	@property
	def IpAddress(self):
		"""Shows IP address of the interface.

		Returns:
			str
		"""
		return self._get_attribute('ipAddress')
