import logging
from anymatter.ble import BleListener
from anymatter.finder import DeviceFinder
from anymatter.switchbot.meterplus import SwitchbotMeterPlus

logger = logging.getLogger(__name__)


class SwitchbotDeviceFinder(DeviceFinder):
    _devicesTypes = {
        "Meter": SwitchbotMeterPlus,
    }

    def __init__(self):
        DeviceFinder.__init__(self)
    
    async def find(self, mac: str, label: str):
        mac = mac.lower()
        device_type = self.from_cache(mac)

        if not device_type:
            ble_device = await BleListener.get().find_device(mac)

            if ble_device is None:
                logger.warning(f"Switchbot device \"{mac}\" not found.")
                return None
            
            # Not ideal, to investigate
            if not ble_device.data:
                logger.warning(f"Switchbot device \"{mac}\" not supported.")
                return None
            
            # Only Meter device are supported for now
            device_type = "Meter"
            self.cache(mac, device_type)

        matter_device = SwitchbotDeviceFinder._devicesTypes[device_type](mac, label)
        BleListener.get().register(mac, matter_device.update)

        return matter_device


async def find_switchbot_device(mac: str, label: str):
    return await SwitchbotDeviceFinder.get().find(mac, label)
