from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PimV4JoinPruneList(Base):
	"""PIM V4 Join Prune Data
	"""

	_SDM_NAME = 'pimV4JoinPruneList'

	def __init__(self, parent):
		super(PimV4JoinPruneList, self).__init__(parent)

	def Tag(self, Name=None):
		"""Gets child instances of Tag from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Tag will be returned.

		Args:
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._select(Tag(self), locals())

	def add_Tag(self, Enabled="False", Name=None):
		"""Adds a child instance of Tag on the server.

		Args:
			Enabled (bool): Enables/disables tags
			Name (str): specifies the name of the tag the entity will be part of

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag.Tag)

		Raises:
			AlreadyExistsError: The requested resource already exists on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tag import Tag
		return self._create(Tag(self), locals())

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

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
	def EnableFlapInfo(self):
		"""If selected, enables this Source entry for use in PIM-SM Register messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableFlapInfo')

	@property
	def EnablePack(self):
		"""If enabled, Multiple Groups can be included within a single packet.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePack')

	@property
	def FlapInterval(self):
		"""(in seconds) Specifies the amount of time between emulated flap events. The default is 60 seconds.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('flapInterval')

	@property
	def GroupAddressCount(self):
		"""The number of multicast group addresses to be included in the multicast group range. The maximum number of valid possible addresses depends on the values for the Group Address and the Group Mask Width. The default value is 1.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupAddressCount')

	@property
	def GroupV4Address(self):
		"""Group Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupV4Address')

	@property
	def GroupV4MaskWidth(self):
		"""Group Mask width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('groupV4MaskWidth')

	@property
	def LocalRouterId(self):
		"""The PIM-SM Router ID value, in IPv4 format.

		Returns:
			list(str)
		"""
		return self._get_attribute('localRouterId')

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
	def PruneSourceAddressCount(self):
		"""The number of Prune Source addresses to be included. The maximum number of valid possible addresses depends on the values for the Source Address and the Source Mask Width. The default value is 0. ONLY used for (*,G) Type to send (S,G,rpt) Prune Messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pruneSourceAddressCount')

	@property
	def PruneSourceV4Address(self):
		"""Prune Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pruneSourceV4Address')

	@property
	def PruneSourceV4MaskWidth(self):
		"""Prune Source Mask width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pruneSourceV4MaskWidth')

	@property
	def RangeType(self):
		"""The Multicast Range Type. Choose one of: (*, *, RP)-Wildcard Group Set. For (*,*, RP) Join/Prune messages. Refers to all Groups associated with this specific RP. (*, G)-Group Specific type. For (*,G) Join/Prune messages. Refers to all sources associated with a specific Group G on the RP tree. (S, G)-Source specific type. For (S,G) Join/Prune messages. Refers only to specific combination of Source S and Group G. (*, G) -> (S, G)-Switchover type. (For switchover from non-source specific group state to source-specific group state.) Register Triggered (S,G)-These are the ranges of multicast group address and unicast source address to which a PIM-SM Router emulating an RP (for those source-group combinations) will send Triggered (S,G) joins and Register-Stop messages after receiving Register messages.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rangeType')

	@property
	def RegisterStopTriggerCount(self):
		"""Available ONLY for use with Register Triggered (S,G) Range Type. (Default = 10)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('registerStopTriggerCount')

	@property
	def RpV4Address(self):
		"""RP Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rpV4Address')

	@property
	def SourceAddressCount(self):
		"""The number of multicast source addresses to be included. The maximum number of valid possible addresses depends on the values for the Source Address and the Source Mask Width. The default value is 0.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceAddressCount')

	@property
	def SourceGroupMappingType(self):
		"""Choose one of: Fully-meshed, One-to-One

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceGroupMappingType')

	@property
	def SourceV4Address(self):
		"""Source Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceV4Address')

	@property
	def SourceV4MaskWidth(self):
		"""Source Mask width

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sourceV4MaskWidth')

	@property
	def Status(self):
		"""Status

		Returns:
			list(str[join|leave|none|notStarted])
		"""
		return self._get_attribute('status')

	@property
	def SwitchOverInterval(self):
		"""(in seconds) The time interval allowed for the switch from using the RP tree to using a Source-specific tree-from (*,G) to (S,G). The default value is 0.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('switchOverInterval')

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

	def Join(self, Arg1):
		"""Executes the join operation on the server.

		Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('join', payload=locals(), response_object=None)

	def Join(self, Arg1, SessionIndices):
		"""Executes the join operation on the server.

		Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('join', payload=locals(), response_object=None)

	def Join(self, Arg1, SessionIndices):
		"""Executes the join operation on the server.

		Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('join', payload=locals(), response_object=None)

	def Join(self, Arg2):
		"""Executes the join operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('join', payload=locals(), response_object=None)

	def Leave(self, Arg1):
		"""Executes the leave operation on the server.

		Leave

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('leave', payload=locals(), response_object=None)

	def Leave(self, Arg1, SessionIndices):
		"""Executes the leave operation on the server.

		Leave

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('leave', payload=locals(), response_object=None)

	def Leave(self, Arg1, SessionIndices):
		"""Executes the leave operation on the server.

		Leave

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('leave', payload=locals(), response_object=None)

	def Leave(self, Arg2):
		"""Executes the leave operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('leave', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self, Arg1):
		"""Executes the resumePeriodicJoin operation on the server.

		Resume Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resumePeriodicJoin', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self, Arg1, SessionIndices):
		"""Executes the resumePeriodicJoin operation on the server.

		Resume Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resumePeriodicJoin', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self, Arg1, SessionIndices):
		"""Executes the resumePeriodicJoin operation on the server.

		Resume Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('resumePeriodicJoin', payload=locals(), response_object=None)

	def ResumePeriodicJoin(self, Arg2):
		"""Executes the resumePeriodicJoin operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('resumePeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self, Arg1):
		"""Executes the stopPeriodicJoin operation on the server.

		Stop Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopPeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self, Arg1, SessionIndices):
		"""Executes the stopPeriodicJoin operation on the server.

		Stop Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopPeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self, Arg1, SessionIndices):
		"""Executes the stopPeriodicJoin operation on the server.

		Stop Periodic Join

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pimV4JoinPruneList object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stopPeriodicJoin', payload=locals(), response_object=None)

	def StopPeriodicJoin(self, Arg2):
		"""Executes the stopPeriodicJoin operation on the server.

		Stops the protocol state machine for the given protocol session instances.

		Args:
			Arg2 (list(number)): List of indices into the protocol plugin. An empty list indicates all instances in the plugin.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('stopPeriodicJoin', payload=locals(), response_object=None)
