import asyncio
import logging
from kasa import Discover

logger = logging.getLogger(__name__)

class KasaDevice:
    def __init__(self, ip: str):
        self._ip = ip
        self._device = None

    async def connect(self) -> bool:
        self._device = None
        logger.info(f"Connecting to Kasa device on IP {self._ip}...")

        try:
            self._device = await Discover.discover_single(self._ip)
        except:
            pass

        return self._device is not None

    async def disconnect(self):
        if not self._device:
            return

        logger.info(f"Disconnecting from Kasa device...")
        await self._device.disconnect()
        self._device = None
