from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class VxlanStaticInfo(Base):
	"""VXLAN Unicast Info.
	"""

	_SDM_NAME = 'vxlanStaticInfo'

	def __init__(self, parent):
		super(VxlanStaticInfo, self).__init__(parent)

	@property
	def Active(self):
		"""Flag.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def LocalVNI(self):
		"""VNI

		Returns:
			list(str)
		"""
		return self._get_attribute('localVNI')

	@property
	def MacStaticConfig(self):
		"""Statically configure the Remote Inner Mac address to Outer Vtep IP mapping, used for traffic.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('macStaticConfig')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def RemoteVmStaticIpv4(self):
		"""VM IPv4 Address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteVmStaticIpv4')

	@property
	def RemoteVmStaticMac(self):
		"""Remote VM MAC address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteVmStaticMac')

	@property
	def RemoteVtepIpv4(self):
		"""Remote VTEP Unicast IPv4

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteVtepIpv4')

	@property
	def SuppressArp(self):
		"""Suppress Arp for VM IP, VM MAC pair.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('suppressArp')

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('fetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
