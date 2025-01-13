import logging
from kasa import Discover, DeviceType
from anymatter.kasa.switch import KasaOnOffSwitch

logger = logging.getLogger(__name__)


class KasaDeviceFinder():
    _instance = None
    _devicesTypes = {
        DeviceType.Plug: KasaOnOffSwitch,
        DeviceType.Bulb: KasaOnOffSwitch,
        DeviceType.Strip: KasaOnOffSwitch,
        DeviceType.WallSwitch: KasaOnOffSwitch,
        DeviceType.LightStrip: KasaOnOffSwitch,
    }

    def __init__(self):
        # TODO: persist found and identified device type/mac for faster boot
        self._found_devices = []
    
    async def find(self, mac: str, label: str):
        device = None
        devices = await Discover.discover()
        for dev in devices.values():
            if dev.mac.lower() != mac.lower():
                continue
            
            if dev.device_type not in KasaDeviceFinder._devicesTypes:
                logger.warn(f"Kasa {dev.device_type} not supported.")
                break

            device = KasaDeviceFinder._devicesTypes[dev.device_type](mac.lower(), label)
            break

        return device

    @staticmethod
    def get():
        if not KasaDeviceFinder._instance:
            KasaDeviceFinder._instance = KasaDeviceFinder()
        
        return KasaDeviceFinder._instance


async def find_kasa_device(mac: str, label: str):
    return await KasaDeviceFinder.get().find(mac, label)
