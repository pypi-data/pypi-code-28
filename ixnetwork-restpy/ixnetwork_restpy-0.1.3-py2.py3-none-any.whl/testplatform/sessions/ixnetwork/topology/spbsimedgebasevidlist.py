from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SpbSimEdgeBaseVidList(Base):
	"""ISIS SPB Simulated Edge BaseVID Configuration
	"""

	_SDM_NAME = 'spbSimEdgeBaseVidList'

	def __init__(self, parent):
		super(SpbSimEdgeBaseVidList, self).__init__(parent)

	@property
	def SpbSimEdgeIsidList(self):
		"""Returns the one and only one SpbSimEdgeIsidList object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgeisidlist.SpbSimEdgeIsidList)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.spbsimedgeisidlist import SpbSimEdgeIsidList
		return self._read(SpbSimEdgeIsidList(self), None)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BaseVid(self):
		"""Base VID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('baseVid')

	@property
	def BaseVlanPriority(self):
		"""B-VLAN Priority

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('baseVlanPriority')

	@property
	def BvlanTpid(self):
		"""B-VLAN TPID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bvlanTpid')

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
	def EctAlgorithm(self):
		"""ECT AlgorithmType

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ectAlgorithm')

	@property
	def IsidCount(self):
		"""ISID Count(multiplier)

		Returns:
			number
		"""
		return self._get_attribute('isidCount')
	@IsidCount.setter
	def IsidCount(self, value):
		self._set_attribute('isidCount', value)

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
	def UseFlagBit(self):
		"""Use Flag Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('useFlagBit')

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
