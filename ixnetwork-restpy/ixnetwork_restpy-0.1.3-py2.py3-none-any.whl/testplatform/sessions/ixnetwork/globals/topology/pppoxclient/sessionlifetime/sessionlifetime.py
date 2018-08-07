from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class SessionLifetime(Base):
	"""Parameters used for controlling the lifetime and restart capabilities of sessions
	"""

	_SDM_NAME = 'sessionLifetime'

	def __init__(self, parent):
		super(SessionLifetime, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def EnableLifetime(self):
		"""Enable session lifetime

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableLifetime')

	@property
	def EnableRestart(self):
		"""Enable automatic session restart after stop at lifetime expiry

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableRestart')

	@property
	def MaxLifetime(self):
		"""Maximum session lifetime (in seconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxLifetime')

	@property
	def MaxRestarts(self):
		"""Maximum number of times each session is automatically restarted

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('maxRestarts')

	@property
	def MinLifetime(self):
		"""Minimum session lifetime (in seconds)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('minLifetime')

	@property
	def RowNames(self):
		"""name of rows.

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def UnlimitedRestarts(self):
		"""Allow each session to always be automatically restarted

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('unlimitedRestarts')

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
