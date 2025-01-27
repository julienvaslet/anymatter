import logging
from typing import Optional

logger = logging.getLogger(__name__)


class DeviceFinder():
    _instance = None

    def __init__(self):
        self._cached_devices = {}
    
    async def find(self, mac: str, label: str):
        raise Exception("Not implemented")

    def from_cache(self, mac: str) -> Optional[str]:
        return self._cached_devices.get(mac, None)

    def cache(self, mac: str, type: str):
        self._cached_devices[mac] = type
        logger.info(f"Cached \"{mac}\" as \"{type}\".")

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = cls()
        
        return cls._instance


async def find_kasa_device(mac: str, label: str):
    return await KasaDeviceFinder.get().find(mac, label)
