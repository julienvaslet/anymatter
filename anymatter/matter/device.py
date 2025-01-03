import asyncio
import logging
import sys
import time
from pathlib import Path
from typing import List
from circuitmatter import CircuitMatter
from circuitmatter.device_types.simple_device import SimpleDevice
from circuitmatter.pase import compute_qr_code
from abc import ABC, abstractmethod
from anymatter.matter.capabilities import Capability
from anymatter.qrcode import print_qr_code

logger = logging.getLogger(__name__)


class Device(ABC):
    def __init__(self, product_name="Anymatter device", product_id=0x1234, vendor_id=0xFFF4, refresh_rate_ms=1000):
        self._connected = False
        self._matter = None
        self._capabilities = []
        self._product_name = product_name
        self._product_id = product_id
        self._vendor_id = vendor_id
        self._refresh_rate_ms = refresh_rate_ms
        self._last_refresh_ms = 0

    def _display_qr_code(self):
        if not self._matter:
            return
        
        encoded = compute_qr_code(self._vendor_id, self._product_id, self._matter.nonvolatile["discriminator"], self._matter.nonvolatile["passcode"])
        print_qr_code(f"MT:{encoded}")
        print(f"Manual code: {self._matter.nonvolatile['manual_code']}")
    
    def add_capability(self, capability: Capability):
        self._capabilities.append(capability)

    async def run(self):
        logger.info("Connecting to the device...")
        self._connected = await self.connect()

        # TODO: Retry?
        if not self._connected:
            raise Exception("Unable to connect to the device.")

        logger.info("Connected.")
        logger.info("Setting up Matter Device")

        state_filename = f"matter-device-states/{self._product_name.lower().replace(' ', '-')}.json"
        Path(state_filename).parent.mkdir(parents=True, exist_ok=True)

        self._matter = CircuitMatter(
            vendor_id=self._vendor_id,
            product_id=self._product_id,
            product_name=self._product_name,
            state_filename=state_filename,
        )

        for capability in self._capabilities:
            self._matter.add_device(capability.get_circuitmatter_device())

        logger.info("Matter device is up.")
        self._display_qr_code()

        while True:
            current_time_ms = round(time.time() * 1000)

            if current_time_ms > self._last_refresh_ms + self._refresh_rate_ms:
                self._last_refresh_ms = current_time_ms
                await self.refresh()

            self._matter.process_packets()

        await self.disconnect()

    async def refresh(self):
        pass

    @abstractmethod
    async def connect(self) -> bool:
        pass

    @abstractmethod
    async def disconnect(self):
        pass