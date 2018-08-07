from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OspfTrafficEngineering(Base):
	"""Ospf Traffic Engineering Configuration
	"""

	_SDM_NAME = 'ospfTrafficEngineering'

	def __init__(self, parent):
		super(OspfTrafficEngineering, self).__init__(parent)

	@property
	def AdministratorGroup(self):
		"""Administrator Group

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('administratorGroup')

	@property
	def BandwidthPriority0(self):
		"""Bandwidth for Priority 0 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority0')

	@property
	def BandwidthPriority1(self):
		"""Bandwidth for Priority 1 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority1')

	@property
	def BandwidthPriority2(self):
		"""Bandwidth for Priority 2 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority2')

	@property
	def BandwidthPriority3(self):
		"""Bandwidth for Priority 3 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority3')

	@property
	def BandwidthPriority4(self):
		"""Bandwidth for Priority 4 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority4')

	@property
	def BandwidthPriority5(self):
		"""Bandwidth for Priority 5 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority5')

	@property
	def BandwidthPriority6(self):
		"""Bandwidth for Priority 6 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority6')

	@property
	def BandwidthPriority7(self):
		"""Bandwidth for Priority 7 (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidthPriority7')

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
	def Enable(self):
		"""Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enable')

	@property
	def MaxBandwidth(self):
		"""Maximum Bandwidth (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxBandwidth')

	@property
	def MaxReservableBandwidth(self):
		"""Maximum Reservable Bandwidth (B/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxReservableBandwidth')

	@property
	def MetricLevel(self):
		"""TE Metric Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('metricLevel')

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
