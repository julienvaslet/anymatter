from __future__ import annotations
import asyncio
import logging
from kasa import Discover
from anymatter.matter import Device

logger = logging.getLogger(__name__)


class KasaDevice(Device):
    def __init__(self, mac: str, label: str):
        Device.__init__(self, mac, label)
        self._mac = mac
        self._device = None
        self.vendor_name = "TP-Link Systems Inc."
        self.vendor_id = 0x1391

    @property
    def device(self) -> KasaDevice:
        return self._device

    async def connect(self) -> bool:
        self._device = None
        logger.info(f"Connecting to Kasa device {self._mac}...")

        try:
            devices = await Discover.discover()
            for device in devices.values():
                if device.mac.lower() == self._mac.lower():
                    self._device = device
                    break
        except:
            pass

        # DeviceInfo(
        #     short_name='HS103',
        #     long_name='HS103',
        #     brand='kasa',
        #     device_family='IOT.SMARTPLUGSWITCH',
        #     device_type=<DeviceType.Plug: 'plug'>,
        #     hardware_version='5.0',
        #     firmware_version='1.0.13',
        #     firmware_build='Build 240117 Rel.162355',
        #     requires_auth=False,
        #     region='US'
        # )

        return self._device is not None

    async def disconnect(self):
        if not self._device:
            return

        logger.info(f"Disconnecting from Kasa device...")
        await self._device.disconnect()
        self._device = None
