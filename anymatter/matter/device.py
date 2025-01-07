import asyncio
import logging
import sys
import time
from pathlib import Path
from typing import List
from circuitmatter import CircuitMatter
from circuitmatter.clusters.system_model import descriptor
from circuitmatter.device_types.simple_device import SimpleDevice
from circuitmatter.pase import compute_qr_code
from abc import ABC, abstractmethod
from anymatter.matter.capabilities import Capability
from anymatter.matter.clusters import BridgedDeviceBasicInformationCluster
from anymatter.qrcode import print_qr_code

logger = logging.getLogger(__name__)


class Device(SimpleDevice):
    def __init__(self, name: str, refresh_rate_ms=1000):
        SimpleDevice.__init__(self, name)
        self._connected = False
        self._capabilities = []
        self._refresh_rate_ms = refresh_rate_ms
        self._last_refresh_ms = 0

        self._bridged_device = BridgedDeviceBasicInformationCluster()
        self.servers.append(self._bridged_device)

    @property
    def vendor_name(self):
        return self._bridged_device.vendor_name
    
    @vendor_name.setter
    def vendor_name(self, value: str):
        self._bridged_device.vendor_name = vendor_name

    @property
    def product_name(self):
        return self._bridged_device.product_name
    
    @product_name.setter
    def product_name(self, value: str):
        self._bridged_device.product_name = product_name

    def _register_device_type(self, device_type_id: int, revision: int): 
        device_type = descriptor.DescriptorCluster.DeviceTypeStruct()
        device_type.DeviceType = device_type_id
        device_type.Revision = revision
        self.descriptor.DeviceTypeList.append(device_type)
    
    def add_capability(self, capability: Capability):
        self._register_device_type(capability.device_type_id, capability.revision)
        
        for server in capability.servers:
            self.servers.append(server)

    async def tick(self):
        if not self._connected:
            self._connected = await self.connect()

            if not self._connected:
                logger.warn("Unable to connect to the device.")
            else:
                logger.info("Connected.")
        
        if not self._connected:
            return

        current_time_ms = round(time.time() * 1000)

        if current_time_ms > self._last_refresh_ms + self._refresh_rate_ms:
            self._last_refresh_ms = current_time_ms
            await self.refresh()


    async def refresh(self):
        pass

    @abstractmethod
    async def connect(self) -> bool:
        pass

    @abstractmethod
    async def disconnect(self):
        pass