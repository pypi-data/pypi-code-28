from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetconfServer(Base):
	"""Netconf Server emulates a Netconf DUT which connects to a Netconf Client supporting Netconf as per RFC6241/RFC6242
	"""

	_SDM_NAME = 'netconfServer'

	def __init__(self, parent):
		super(NetconfServer, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def CapabilitiesBase1Dot0(self):
		"""Whether base1.0 support should be advertised in Capabilities.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesBase1Dot0')

	@property
	def CapabilitiesBase1Dot1(self):
		"""Whether base1.1 support should be advertised in Capabilities.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesBase1Dot1')

	@property
	def CapabilitiesCandidate(self):
		"""Whether supports capability candidate to make changes into an intermediate candidate database. Normally this is preferred over writable-running.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesCandidate')

	@property
	def CapabilitiesConfirmedCommit(self):
		"""Whether supports capability confirmed-commit to specify ability to commit a group of commands or none as a batch.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesConfirmedCommit')

	@property
	def CapabilitiesInterleave(self):
		"""Whether supports capability interleave to interleave notifications and responses.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesInterleave')

	@property
	def CapabilitiesNotification(self):
		"""Whether supports capability notification to aynchronously send notifications to Netconf client.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesNotification')

	@property
	def CapabilitiesRollbackOnError(self):
		"""Whether supports capability rollback to rollback partial changes make changes on detection of error during validate or commit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesRollbackOnError')

	@property
	def CapabilitiesStartup(self):
		"""Whether supports capability startup to make changes in config persistent on device restart.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesStartup')

	@property
	def CapabilitiesUrl(self):
		"""Whether supports capability url to specify netconf commands using url.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesUrl')

	@property
	def CapabilitiesValidate(self):
		"""Whether supports capability validate to specify ability to validate a netconf command prior to commit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesValidate')

	@property
	def CapabilitiesWritableRunning(self):
		"""Whether supports capability writable-running to directly modify running config.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesWritableRunning')

	@property
	def CapabilitiesXpath(self):
		"""Whether supports capability xpath to specify netconf commands and filters using xpath extensions.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('capabilitiesXpath')

	@property
	def ClientIpv4Address(self):
		"""Specify the IPv4 address of the Netconf Client which will connect with this Server.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('clientIpv4Address')

	@property
	def ConnectedVia(self):
		"""List of layers this layer used to connect to the wire

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('connectedVia')
	@ConnectedVia.setter
	def ConnectedVia(self, value):
		self._set_attribute('connectedVia', value)

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
	def Errors(self):
		"""A list of errors that have occurred

		Returns:
			list(dict(arg1:str[None|/api/v1/sessions/1/ixnetwork/?deepchild=*],arg2:list[str]))
		"""
		return self._get_attribute('errors')

	@property
	def Multiplier(self):
		"""Number of layer instances per parent instance (multiplier)

		Returns:
			number
		"""
		return self._get_attribute('multiplier')
	@Multiplier.setter
	def Multiplier(self, value):
		self._set_attribute('multiplier', value)

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
	def Password(self):
		"""Password for Username/Password mode.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('password')

	@property
	def PublicKeyDirectory(self):
		"""Directory containing public key file for this session

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('publicKeyDirectory')

	@property
	def PublicKeyFileName(self):
		"""File containing public key (e.g. generated using ssh_keygen). For multiple server rows and assymetric public key filenames( which cannot be expressed easily as a pattern) please explore File option in Master Row Pattern Editor by putting the file namesin a .csv and pulling those values into the column cells.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('publicKeyFileName')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SshAuthenticationMechanism(self):
		"""The authentication mechanism for connecting to Netconf Client.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sshAuthenticationMechanism')

	@property
	def StackedLayers(self):
		"""List of secondary (many to one) child layer protocols

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/topology?deepchild=*])
		"""
		return self._get_attribute('stackedLayers')
	@StackedLayers.setter
	def StackedLayers(self, value):
		self._set_attribute('stackedLayers', value)

	@property
	def StateCounts(self):
		"""A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up

		Returns:
			dict(total:number,notStarted:number,down:number,up:number)
		"""
		return self._get_attribute('stateCounts')

	@property
	def Status(self):
		"""Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

		Returns:
			str(configured|error|mixed|notStarted|started|starting|stopping)
		"""
		return self._get_attribute('status')

	@property
	def UserName(self):
		"""Username for Username/Password mode and Username for Key-Based authentication mode if applicable.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('userName')

	def remove(self):
		"""Deletes a child instance of NetconfServer on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

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

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def Start(self, Arg1):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Stop(self, Arg1):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfServer object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
