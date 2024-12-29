import asyncio
import logging
from typing import List
from circuitmatter import CircuitMatter
from circuitmatter.device_types.simple_device import SimpleDevice
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Device(ABC):
    def __init__(self):
        self._connected = False

    async def run(self):
        logger.info("Connecting to the device...")
        self._connected = await self.connect()

        # TODO: Retry?
        if not self._connected:
            raise Exception("Unable to connect to the device.")

        logger.info("Connected.")
        logger.info("Setting up Matter Device")

        matter = CircuitMatter(
            vendor_id=0xFFF4,
            product_id=0x1234,
            product_name="CircuitMatter Device"
        )

        for device in self._get_cm_devices():
            matter.add_device(device)

        logger.info("Matter device is up.")
        while True:
            await self.update()
            matter.process_packets()

        await self.disconnect()

    async def update(self):
        pass

    @abstractmethod
    def _get_cm_devices(self) -> List[SimpleDevice]:
        pass

    @abstractmethod
    async def connect(self) -> bool:
        pass

    @abstractmethod
    async def disconnect(self):
        pass