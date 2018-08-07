from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Object(Base):
	"""Tlv object container which can contain one of a field, sub tlv or container
	"""

	_SDM_NAME = 'object'

	def __init__(self, parent):
		super(Object, self).__init__(parent)

	def Container(self, Name=None):
		"""Gets child instances of Container from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Container will be returned.

		Args:
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.container.Container))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.container import Container
		return self._select(Container(self), locals())

	def Field(self, Description=None, Name=None):
		"""Gets child instances of Field from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of Field will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.field.Field))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.field import Field
		return self._select(Field(self), locals())

	def RepeatableContainer(self, Name=None):
		"""Gets child instances of RepeatableContainer from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of RepeatableContainer will be returned.

		Args:
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.repeatablecontainer.RepeatableContainer))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.repeatablecontainer import RepeatableContainer
		return self._select(RepeatableContainer(self), locals())

	def SubTlv(self, Description=None, Name=None):
		"""Gets child instances of SubTlv from the server.

		Use the named parameters as selection criteria to find specific instances.
		All named parameters support regex.
		If no named parameters are specified then all instances of SubTlv will be returned.

		Args:
			Description (str): Description of the tlv
			Name (str): Name of the tlv

		Returns:
			list(obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.subtlv.SubTlv))

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.subtlv import SubTlv
		return self._select(SubTlv(self), locals())

	@property
	def Name(self):
		"""The name of the object

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
