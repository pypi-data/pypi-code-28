from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PceInitiateLSPParameters(Base):
	"""This tab configures the Initiated LSP Parameters.
	"""

	_SDM_NAME = 'pceInitiateLSPParameters'

	def __init__(self, parent):
		super(PceInitiateLSPParameters, self).__init__(parent)

	def PceInitiateXROobject(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PceInitiateXROobject from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PceInitiateXROobject will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceinitiatexroobject.PceInitiateXROobject))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceinitiatexroobject import PceInitiateXROobject
		return self._select(PceInitiateXROobject(self), locals())

	def PcepEroSubObjectsList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PcepEroSubObjectsList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PcepEroSubObjectsList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceperosubobjectslist.PcepEroSubObjectsList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pceperosubobjectslist import PcepEroSubObjectsList
		return self._select(PcepEroSubObjectsList(self), locals())

	def PcepMetricSubObjectsList(self, DescriptiveName=None, Name=None):
		"""Gets child instances of PcepMetricSubObjectsList from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of PcepMetricSubObjectsList will be returned.

		Args:
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepmetricsubobjectslist.PcepMetricSubObjectsList))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.pcepmetricsubobjectslist import PcepMetricSubObjectsList
		return self._select(PcepMetricSubObjectsList(self), locals())

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AssociationId(self):
		"""The Association ID of this LSP.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('associationId')

	@property
	def Bandwidth(self):
		"""Bandwidth (bits/sec)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bandwidth')

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
	def DestEndPointIpv4(self):
		"""Dest IPv4 address of the path for which a path computation is Initiated. Will be greyed out if IP Version is IPv6.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destEndPointIpv4')

	@property
	def DestEndPointIpv6(self):
		"""Dest IPv6 address of the path for which a path computation is Initiated. Will be greyed out if IP Version is IPv4.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('destEndPointIpv6')

	@property
	def EnableXro(self):
		"""Include XRO

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableXro')

	@property
	def ExcludeAny(self):
		"""This is a type of Resource Affinity Procedure that is used to validate a link. This control accepts a link only if the link carries all of the attributes in the set.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('excludeAny')

	@property
	def FailBit(self):
		"""Fail Bit

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('failBit')

	@property
	def HoldingPriority(self):
		"""The priority of the LSP with respect to holding resources. The value 0 is the highest priority. Holding Priority is used in deciding whether this session can be preempted by another session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('holdingPriority')

	@property
	def IncludeAll(self):
		"""This is a type of Resource Affinity Procedure that is used to validate a link. This control excludes a link from consideration if the link carries any of the attributes in the set.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAll')

	@property
	def IncludeAny(self):
		"""This is a type of Resource Affinity Procedure that is used to validate a link. This control accepts a link if the link carries any of the attributes in the set.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAny')

	@property
	def IncludeAssociation(self):
		"""Indicates whether PPAG will be included in a PCInitiate message. All other attributes in sub-tab-PPAG would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeAssociation')

	@property
	def IncludeBandwidth(self):
		"""Indicates whether Bandwidth will be included in a PCInitiate message. All other attributes in sub-tab-Bandwidth would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeBandwidth')

	@property
	def IncludeEndPoints(self):
		"""Indicates whether END-POINTS object will be included in a PCInitiate message. All other attributes in sub-tab-End Points would be editable only if this checkbox is enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeEndPoints')

	@property
	def IncludeEro(self):
		"""Specifies whether ERO is active or inactive. All subsequent attributes of the sub-tab-ERO would be editable only if this is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeEro')

	@property
	def IncludeLsp(self):
		"""Indicates whether LSP will be included in a PCInitiate message. All other attributes in sub-tab-LSP would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLsp')

	@property
	def IncludeLspa(self):
		"""Indicates whether LSPA will be included in a PCInitiate message. All other attributes in sub-tab-LSPA would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeLspa')

	@property
	def IncludeMetric(self):
		"""Indicates whether the PCInitiate message will have the metric list that is configured. All subsequent attributes of the sub-tab-Metric would be editable only if this is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeMetric')

	@property
	def IncludeSrp(self):
		"""Indicates whether SRP object will be included in a PCInitiate message. All other attributes in sub-tab-SRP would be editable only if this checkbox is enabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSrp')

	@property
	def IncludeSymbolicPathNameTlv(self):
		"""Indicates if Symbolic-Path-Name TLV is to be included in PCInitiate message.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('includeSymbolicPathNameTlv')

	@property
	def IpVersion(self):
		"""Drop down to select the IP Version with 2 choices : IPv4 / IPv6

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipVersion')

	@property
	def LocalProtection(self):
		"""When set, this means that the path must include links protected with Fast Reroute

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localProtection')

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
	def NumberOfEroSubObjects(self):
		"""Value that indicates the number of ERO Sub Objects to be configured.

		Returns:
			number
		"""
		return self._get_attribute('numberOfEroSubObjects')
	@NumberOfEroSubObjects.setter
	def NumberOfEroSubObjects(self, value):
		self._set_attribute('numberOfEroSubObjects', value)

	@property
	def NumberOfMetricSubObject(self):
		"""Value that indicates the number of Metric Objects to be configured.

		Returns:
			number
		"""
		return self._get_attribute('numberOfMetricSubObject')
	@NumberOfMetricSubObject.setter
	def NumberOfMetricSubObject(self, value):
		self._set_attribute('numberOfMetricSubObject', value)

	@property
	def NumberOfXroSubObjects(self):
		"""Number of XRO Sub Objects

		Returns:
			number
		"""
		return self._get_attribute('numberOfXroSubObjects')
	@NumberOfXroSubObjects.setter
	def NumberOfXroSubObjects(self, value):
		self._set_attribute('numberOfXroSubObjects', value)

	@property
	def OverridePlspId(self):
		"""Indicates if PLSP-ID will be set by the state machine or user. If disabled user wont have the control and state machine will set it.

		Returns:
			bool
		"""
		return self._get_attribute('overridePlspId')
	@OverridePlspId.setter
	def OverridePlspId(self, value):
		self._set_attribute('overridePlspId', value)

	@property
	def OverrideSrpIdNumber(self):
		"""Indicates whether SRP ID Number is overridable.

		Returns:
			bool
		"""
		return self._get_attribute('overrideSrpIdNumber')
	@OverrideSrpIdNumber.setter
	def OverrideSrpIdNumber(self, value):
		self._set_attribute('overrideSrpIdNumber', value)

	@property
	def PathSetupType(self):
		"""Indicates which type of LSP will be requested in the PCInitiated Request.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('pathSetupType')

	@property
	def PlspId(self):
		"""An identifier for the LSP. A PCC creates a unique PLSP-ID for each LSP that is constant for the lifetime of a PCEP session. The PCC will advertise the same PLSP-ID on all PCEP sessions it maintains at a given time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('plspId')

	@property
	def ProtectionLsp(self):
		"""Indicates whether Protection LSP Bit is On.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('protectionLsp')

	@property
	def SessionInfo(self):
		"""Logs additional information about the LSP state

		Returns:
			list(str[advertised|delegatedActive|delegatedDown|delegatedGoingUp|delegatedUp|init|none|notDelegatedActive|notDelegatedDown|notDelegatedGoingUp|notDelegatedUp|pcErrorReceived|removedByPCC|removedByPCE|returnDelegation])
		"""
		return self._get_attribute('sessionInfo')

	@property
	def SetupPriority(self):
		"""The priority of the LSP with respect to taking resources.The value 0 is the highest priority.The Setup Priority is used in deciding whether this session can preempt another session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('setupPriority')

	@property
	def SrcEndPointIpv4(self):
		"""Source IPv4 address of the path for which a path computation is Initiated. Will be greyed out if IP Version is set to IPv6.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srcEndPointIpv4')

	@property
	def SrcEndPointIpv6(self):
		"""Source IPv6 address of the path for which a path computation is Initiated. Will be greyed out if IP version is set to IPv4.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srcEndPointIpv6')

	@property
	def SrpIdNumber(self):
		"""The SRP object is used to correlate between initiation requests sent by the PCE and the error reports and state reports sent by the PCC. This number is unique per PCEP session and is incremented per initiation.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('srpIdNumber')

	@property
	def StandbyMode(self):
		"""Indicates whether Standby LSP Bit is On.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('standbyMode')

	@property
	def SymbolicPathName(self):
		"""Each LSP (path) must have a symbolic name that is unique in the PCC. It must remain constant throughout a path's lifetime, which may span across multiple consecutive PCEP sessions and/or PCC restarts.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('symbolicPathName')

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

	def ReturnDelegation(self, Arg1):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Initiated LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pceInitiateLSPParameters object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('returnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, Arg1, SessionIndices):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Initiated LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pceInitiateLSPParameters object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('returnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, Arg1, SessionIndices):
		"""Executes the returnDelegation operation on the server.

		Return Delegation of PCE-Initiated LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pceInitiateLSPParameters object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('returnDelegation', payload=locals(), response_object=None)

	def ReturnDelegation(self, Arg2):
		"""Executes the returnDelegation operation on the server.

		Return Delegation helps PCE to return a delegation of LSP/LSPs.

		Args:
			Arg2 (list(number)): Return Delegation.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('returnDelegation', payload=locals(), response_object=None)

	def TakeControl(self, Arg1):
		"""Executes the takeControl operation on the server.

		Take Control of PCE-Initiated LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pceInitiateLSPParameters object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('takeControl', payload=locals(), response_object=None)

	def TakeControl(self, Arg1, SessionIndices):
		"""Executes the takeControl operation on the server.

		Take Control of PCE-Initiated LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pceInitiateLSPParameters object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('takeControl', payload=locals(), response_object=None)

	def TakeControl(self, Arg1, SessionIndices):
		"""Executes the takeControl operation on the server.

		Take Control of PCE-Initiated LSPs

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./pceInitiateLSPParameters object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('takeControl', payload=locals(), response_object=None)

	def TakeControl(self, Arg2):
		"""Executes the takeControl operation on the server.

		Take Control helps PCE to take control of Orphan LSP/LSPs.

		Args:
			Arg2 (list(number)): Take Control.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('takeControl', payload=locals(), response_object=None)
