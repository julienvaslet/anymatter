from anymatter.device.switch import OnOffSwitch
from anymatter.kasa.device import KasaDevice

class KasaOnOffSwitch(KasaDevice, OnOffSwitch):
    def __init__(self, ip: str):
        super().__init__(ip)

    async def on(self):
        if not self._device:
            raise Exception("Device not connected")

        await self._device.turn_on()
        await self._device.update()

    async def off(self):
        if not self._device:
            raise Exception("Device not connected")

        await self._device.turn_off()
        await self._device.update()
