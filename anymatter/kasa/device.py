import asyncio
from kasa import Discover

class KasaDevice:
    def __init__(self, ip: str):
        self._ip = ip
        self._device = None

    async def connect(self) -> bool:
        try:
            self._device = None
            self._device = await Discover.discover_single(self._ip)
        except:
            pass

        return self._device is not None

    async def disconnect(self):
        if not self._device:
            return

        await self._device.disconnect()
        self._device = None
