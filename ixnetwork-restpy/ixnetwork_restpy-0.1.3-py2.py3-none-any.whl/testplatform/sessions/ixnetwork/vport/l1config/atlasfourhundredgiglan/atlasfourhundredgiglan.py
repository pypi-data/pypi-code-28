from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AtlasFourHundredGigLan(Base):
	"""
	"""

	_SDM_NAME = 'atlasFourHundredGigLan'

	def __init__(self, parent):
		super(AtlasFourHundredGigLan, self).__init__(parent)

	@property
	def Fcoe(self):
		"""Returns the one and only one Fcoe object from the server.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.atlasfourhundredgiglan.fcoe.fcoe.Fcoe)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.atlasfourhundredgiglan.fcoe.fcoe import Fcoe
		return self._read(Fcoe(self), None)

	@property
	def AutoInstrumentation(self):
		"""

		Returns:
			str(endOfFrame|floating)
		"""
		return self._get_attribute('autoInstrumentation')
	@AutoInstrumentation.setter
	def AutoInstrumentation(self, value):
		self._set_attribute('autoInstrumentation', value)

	@property
	def BadBlocksNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('badBlocksNumber')
	@BadBlocksNumber.setter
	def BadBlocksNumber(self, value):
		self._set_attribute('badBlocksNumber', value)

	@property
	def EnableAutoNegotiation(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableAutoNegotiation')
	@EnableAutoNegotiation.setter
	def EnableAutoNegotiation(self, value):
		self._set_attribute('enableAutoNegotiation', value)

	@property
	def EnablePPM(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')
	@EnablePPM.setter
	def EnablePPM(self, value):
		self._set_attribute('enablePPM', value)

	@property
	def EnableRsFec(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRsFec')
	@EnableRsFec.setter
	def EnableRsFec(self, value):
		self._set_attribute('enableRsFec', value)

	@property
	def EnableRsFecStats(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableRsFecStats')
	@EnableRsFecStats.setter
	def EnableRsFecStats(self, value):
		self._set_attribute('enableRsFecStats', value)

	@property
	def EnabledFlowControl(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabledFlowControl')
	@EnabledFlowControl.setter
	def EnabledFlowControl(self, value):
		self._set_attribute('enabledFlowControl', value)

	@property
	def FirecodeAdvertise(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('firecodeAdvertise')
	@FirecodeAdvertise.setter
	def FirecodeAdvertise(self, value):
		self._set_attribute('firecodeAdvertise', value)

	@property
	def FirecodeForceOff(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('firecodeForceOff')
	@FirecodeForceOff.setter
	def FirecodeForceOff(self, value):
		self._set_attribute('firecodeForceOff', value)

	@property
	def FirecodeForceOn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('firecodeForceOn')
	@FirecodeForceOn.setter
	def FirecodeForceOn(self, value):
		self._set_attribute('firecodeForceOn', value)

	@property
	def FirecodeRequest(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('firecodeRequest')
	@FirecodeRequest.setter
	def FirecodeRequest(self, value):
		self._set_attribute('firecodeRequest', value)

	@property
	def FlowControlDirectedAddress(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('flowControlDirectedAddress')
	@FlowControlDirectedAddress.setter
	def FlowControlDirectedAddress(self, value):
		self._set_attribute('flowControlDirectedAddress', value)

	@property
	def ForceDisableFEC(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('forceDisableFEC')
	@ForceDisableFEC.setter
	def ForceDisableFEC(self, value):
		self._set_attribute('forceDisableFEC', value)

	@property
	def GoodBlocksNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('goodBlocksNumber')
	@GoodBlocksNumber.setter
	def GoodBlocksNumber(self, value):
		self._set_attribute('goodBlocksNumber', value)

	@property
	def IeeeL1Defaults(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('ieeeL1Defaults')

	@property
	def LaserOn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('laserOn')
	@LaserOn.setter
	def LaserOn(self, value):
		self._set_attribute('laserOn', value)

	@property
	def LinkTraining(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('linkTraining')
	@LinkTraining.setter
	def LinkTraining(self, value):
		self._set_attribute('linkTraining', value)

	@property
	def LoopContinuously(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('loopContinuously')
	@LoopContinuously.setter
	def LoopContinuously(self, value):
		self._set_attribute('loopContinuously', value)

	@property
	def LoopCountNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('loopCountNumber')
	@LoopCountNumber.setter
	def LoopCountNumber(self, value):
		self._set_attribute('loopCountNumber', value)

	@property
	def Loopback(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def LoopbackMode(self):
		"""

		Returns:
			str(internalLoopback|lineLoopback|none)
		"""
		return self._get_attribute('loopbackMode')
	@LoopbackMode.setter
	def LoopbackMode(self, value):
		self._set_attribute('loopbackMode', value)

	@property
	def Ppm(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def RsFecAdvertise(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rsFecAdvertise')
	@RsFecAdvertise.setter
	def RsFecAdvertise(self, value):
		self._set_attribute('rsFecAdvertise', value)

	@property
	def RsFecForceOn(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rsFecForceOn')
	@RsFecForceOn.setter
	def RsFecForceOn(self, value):
		self._set_attribute('rsFecForceOn', value)

	@property
	def RsFecRequest(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('rsFecRequest')
	@RsFecRequest.setter
	def RsFecRequest(self, value):
		self._set_attribute('rsFecRequest', value)

	@property
	def SendSetsMode(self):
		"""

		Returns:
			str(alternate|typeAOnly|typeBOnly)
		"""
		return self._get_attribute('sendSetsMode')
	@SendSetsMode.setter
	def SendSetsMode(self, value):
		self._set_attribute('sendSetsMode', value)

	@property
	def Speed(self):
		"""

		Returns:
			str(speed100g|speed200g|speed400g|speed50g)
		"""
		return self._get_attribute('speed')
	@Speed.setter
	def Speed(self, value):
		self._set_attribute('speed', value)

	@property
	def StartErrorInsertion(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('startErrorInsertion')
	@StartErrorInsertion.setter
	def StartErrorInsertion(self, value):
		self._set_attribute('startErrorInsertion', value)

	@property
	def TxIgnoreRxLinkFaults(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('txIgnoreRxLinkFaults')
	@TxIgnoreRxLinkFaults.setter
	def TxIgnoreRxLinkFaults(self, value):
		self._set_attribute('txIgnoreRxLinkFaults', value)

	@property
	def TypeAOrderedSets(self):
		"""

		Returns:
			str(localFault|remoteFault)
		"""
		return self._get_attribute('typeAOrderedSets')
	@TypeAOrderedSets.setter
	def TypeAOrderedSets(self, value):
		self._set_attribute('typeAOrderedSets', value)

	@property
	def TypeBOrderedSets(self):
		"""

		Returns:
			str(localFault|remoteFault)
		"""
		return self._get_attribute('typeBOrderedSets')
	@TypeBOrderedSets.setter
	def TypeBOrderedSets(self, value):
		self._set_attribute('typeBOrderedSets', value)

	@property
	def UseANResults(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('useANResults')
	@UseANResults.setter
	def UseANResults(self, value):
		self._set_attribute('useANResults', value)
