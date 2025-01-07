import logging
from anymatter.matter.capabilities import PowerControl
from anymatter.kasa.device import KasaDevice

logger = logging.getLogger(__name__)


class KasaPowerControl(PowerControl):
    def __init__(self, device: KasaDevice):
        PowerControl.__init__(self, device.name)
        self._device = device

    async def on(self):
        device = self._device.device

        if not device:
            raise Exception("Device not connected")

        logger.info(f"Turning on {device.mac}...")
        await device.turn_on()
        await device.update()

    async def off(self):
        device = self._device.device

        if not device:
            raise Exception("Device not connected")

        logger.info(f"Turning off {device.mac}...")
        await device.turn_off()
        await device.update()


class KasaOnOffSwitch(KasaDevice):
    def __init__(self, mac: str):
        KasaDevice.__init__(self, mac)
        self._power_control = KasaPowerControl(self)
        self.add_capability(self._power_control)

    async def refresh(self):
        if not self.device:
            return
        
        self._power_control.status = self.device.is_on
