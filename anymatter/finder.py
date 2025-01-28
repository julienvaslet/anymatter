import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class DeviceFinder():
    _dirpath = "/data"
    _instance = None

    def __init__(self):
        self._cached_devices = {}
        self._read_cache_from_disk()
    
    async def find(self, mac: str, label: str):
        raise Exception("Not implemented")

    def from_cache(self, mac: str) -> Optional[str]:
        return self._cached_devices.get(mac, None)

    def cache(self, mac: str, type: str):
        if self._cached_devices.get(mac) != type:
            logger.info(f"Cached \"{mac}\" as \"{type}\".")
        
        self._cached_devices[mac] = type
        self._write_cache_to_disk()

    def _get_cache_path(self):
        return f"{self.__class__._dirpath}/{self.__class__.__name__}.cache"

    def _read_cache_from_disk(self):
        try:
            with open(self._get_cache_path()) as f:
                self._cached_devices = json.load(f)
        
        except FileNotFoundError:
            pass

    def _write_cache_to_disk(self):
        with open(self._get_cache_path(), "w") as f:
            json.dump(self._cached_devices, f)

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = cls()
        
        return cls._instance


async def find_kasa_device(mac: str, label: str):
    return await KasaDeviceFinder.get().find(mac, label)
