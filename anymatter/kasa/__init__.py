import logging
from kasa import Discover, DeviceType
from anymatter.finder import DeviceFinder
from anymatter.kasa.switch import KasaOnOffSwitch

logger = logging.getLogger(__name__)

# TODO: Outlet/Plug vs Light vs WallSwitch
class KasaDeviceFinder(DeviceFinder):
    _devicesTypes = {
        DeviceType.Plug: KasaOnOffSwitch,
        DeviceType.Bulb: KasaOnOffSwitch,
        DeviceType.Strip: KasaOnOffSwitch,
        DeviceType.WallSwitch: KasaOnOffSwitch,
        DeviceType.LightStrip: KasaOnOffSwitch,
    }

    def __init__(self):
        DeviceFinder.__init__(self)
    
    async def find(self, mac: str, label: str):
        mac = mac.lower()
        device_type = self.from_cache(mac)

        if not device_type:
            devices = await Discover.discover()

            for dev in devices.values():
                self.cache(dev.mac.lower(), dev.device_type)

                if dev.mac.lower() != mac:
                    continue
            
                device_type = dev.device_type
    
        if device_type not in KasaDeviceFinder._devicesTypes:
            logger.warn(f"Kasa {device_type} not supported.")
            return None

        return KasaDeviceFinder._devicesTypes[device_type](mac, label)


async def find_kasa_device(mac: str, label: str):
    return await KasaDeviceFinder.get().find(mac, label)
