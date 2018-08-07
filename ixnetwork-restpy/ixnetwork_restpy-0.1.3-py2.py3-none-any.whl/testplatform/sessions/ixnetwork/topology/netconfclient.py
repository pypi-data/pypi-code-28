from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class NetconfClient(Base):
	"""Netconf Client emulates a Netconf Controller which connects to a DUT supporting Netconf as per RFC6241/RFC6242
	"""

	_SDM_NAME = 'netconfClient'

	def __init__(self, parent):
		super(NetconfClient, self).__init__(parent)

	@property
	def CommandSnippetsData(self):
		"""Returns the one and only one CommandSnippetsData object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.commandsnippetsdata.CommandSnippetsData)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.commandsnippetsdata import CommandSnippetsData
		return self._read(CommandSnippetsData(self), None)

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
		"""Whether supports capability notification to aynchronously handle notifications from Netconf server device connected to.

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
	def DecryptedCapture(self):
		"""Whether SSH packets for this session will be captured and stored on client in decrypted form.Note that this is not linked to IxNetwork control or data capture which will capture the packets in encrypted format only.Also note that this option should be avoided if Continuous Tranmission mode is enabled for any of the Command Snippets which can leadto huge capture files being generated which could in turn affect Stop time since during Stop, the captures are transferred to the client.The Decrypted Capture can be viewed by either doing right-click on a client where this option is enabled and doing Get Decrypted Capture( allowed on 5 clients at a time ; each of the captures will be opened in a new Wireshark pop-up) OR by stopping the client and then directly opening it from the configured Output Directory from inside the current run folder/capture.This option can be enabled even when a session is already up in which case the capture will be started from that point of time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('decryptedCapture')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def EnablePassphrase(self):
		"""If the Private Key was passphrase protected, this should be enabled to allow configuration of passphrase used.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enablePassphrase')

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
	def NetconfSessionState(self):
		"""Shows the current state of the Netconf SSH Session. None - Not started. Initialized - Configuration has reached the port and TCP connect is on-going. Connecting - SSH Connect is in process. Authenticating - The SSH session is authenticating with the DUT using user/password or Key-based authentication. Open Channel - SSH session is established and SSH Channel is being opened on which data will be sent. Requesting Subsystem - Netconf Subsystem is being requested on top of SSH channel. Ready - The SSH session is in Ready state and waiting for Netconf data to be exchanged. Note that this does not mean that NETCONF is in Up state. That is reached only after Netconf Capabilities are negotiated and there is at least one matching Netconf version (1.0 or 1.1) supported on both client and server. Reconnecting - The TCP connection is broken with DUT and the client is trying to reconnect via TCP with the server.

		Returns:
			list(str[authenticating|connecting|initialized|none|openingChannel|ready|reconnecting|requestingSubsystem])
		"""
		return self._get_attribute('netconfSessionState')

	@property
	def NumberOfCommandSnippetsPerClient(self):
		"""Number of Command Snippets per client.Maximum 100 are allowed per client.

		Returns:
			number
		"""
		return self._get_attribute('numberOfCommandSnippetsPerClient')
	@NumberOfCommandSnippetsPerClient.setter
	def NumberOfCommandSnippetsPerClient(self, value):
		self._set_attribute('numberOfCommandSnippetsPerClient', value)

	@property
	def OutputDirectory(self):
		"""Location of Directory in Client where the decrypted capture, if enabled, and server replies, if enabled, will be stored.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('outputDirectory')

	@property
	def Passphrase(self):
		"""The passphrase with which the Private Key was additionally protected during generation. For multiple clients and assymetric passphrases( which cannot be expressed easily as a pattern) please explore File option in Master Row Pattern Editor by putting the file namesin a .csv and pulling those values into the column cells.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('passphrase')

	@property
	def Password(self):
		"""Password for Username/Password mode.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('password')

	@property
	def PortNumber(self):
		"""The TCP Port Number the Netconf Server is listening on to which to connect.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('portNumber')

	@property
	def PrivateKeyDirectory(self):
		"""Directory containing Private Key file for this session.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('privateKeyDirectory')

	@property
	def PrivateKeyFileName(self):
		"""File containing Private Key.(e.g. generated using ssh_keygen) . For multiple clients and assymetric key file names( which cannot be expressed easily as a pattern) please explore File option in Master Row Pattern Editor by putting the file namesin a .csv and pulling those values into the column cells.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('privateKeyFileName')

	@property
	def SaveReplyXML(self):
		"""If this is enabled, Hellos and replies to commands sent via Command Snippets or global command (such as 'get') by the Netconf Server will be stored in the Output Directoryin current run folder/Replies. Any RPC errors recieved will be stored in a separate Error directory for convenience of debugging error scenarios.This option can be enabled even when a session is already up in which case the replies will be saved from that point of time.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('saveReplyXML')

	@property
	def ServerIpv4Address(self):
		"""Specify the IPv4 address of the DUT to which the Netconf Server should connect.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('serverIpv4Address')

	@property
	def SessionStatus(self):
		"""Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.

		Returns:
			list(str[down|notStarted|up])
		"""
		return self._get_attribute('sessionStatus')

	@property
	def SshAuthenticationMechanism(self):
		"""The authentication mechanism for connecting to Netconf Server.

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
		"""Username for Username/Password mode and also used for Key-based Authentication as the username.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('userName')

	def remove(self):
		"""Deletes a child instance of NetconfClient on the server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def ExecuteCommandGet(self, Arg1):
		"""Executes the executeCommandGet operation on the server.

		Send get command to DUT if the Netconf session is in established/ready state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('executeCommandGet', payload=locals(), response_object=None)

	def ExecuteCommandGet(self, Arg1, SessionIndices):
		"""Executes the executeCommandGet operation on the server.

		Send get command to DUT if the Netconf session is in established/ready state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
			SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('executeCommandGet', payload=locals(), response_object=None)

	def ExecuteCommandGet(self, Arg1, SessionIndices):
		"""Executes the executeCommandGet operation on the server.

		Send get command to DUT if the Netconf session is in established/ready state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('executeCommandGet', payload=locals(), response_object=None)

	def ExecuteCommandGet(self, Arg2):
		"""Executes the executeCommandGet operation on the server.

		Send the configured command for the selected rows to the DUT if the selected client's Netconf session is up with the DUT.

		Args:
			Arg2 (list(number)): List of indices into the device group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('executeCommandGet', payload=locals(), response_object=None)

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

	def GetDecryptedCapture(self, Arg2):
		"""Executes the getDecryptedCapture operation on the server.

		If Enable Capture is enabled, this will fetch and open the decrypted capture for selected sessions.

		Args:
			Arg2 (list(number)): List of indices into the device group.

		Returns:
			list(str): ID to associate each async action invocation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('getDecryptedCapture', payload=locals(), response_object=None)

	def RestartDown(self, Arg1):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('restartDown', payload=locals(), response_object=None)

	def RestartDown(self, Arg1, SessionIndices):
		"""Executes the restartDown operation on the server.

		Stop and start interfaces and sessions that are in Down state.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('start', payload=locals(), response_object=None)

	def Start(self, Arg1, SessionIndices):
		"""Executes the start operation on the server.

		Start selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)

	def Stop(self, Arg1, SessionIndices):
		"""Executes the stop operation on the server.

		Stop selected protocols.

		Args:
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
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
			Arg1 (list(str[None|/api/v1/sessions/1/ixnetwork/topology])): This parameter requires a list of /topology/./netconfClient object references
			SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._execute('stop', payload=locals(), response_object=None)
