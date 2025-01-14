import logging
from anymatter.switchbot.meterplus import SwitchbotMeterPlus
from anymatter.ble import BleListener

logger = logging.getLogger(__name__)


async def find_switchbot_device(mac: str, label: str):
    mac = mac.lower()
    ble_device = await BleListener.get().find_device(mac)

    if ble_device is None:
        logger.warning(f"Switchbot device \"{mac}\" not found.")
        return None
    
    # Not ideal, to investigate
    if not ble_device.data:
        logger.warning(f"Switchbot device \"{mac}\" not supported.")
        return None

    matter_device = SwitchbotMeterPlus(mac, label)
    matter_device.update(ble_device)
    BleListener.get().register(mac, matter_device.update)

    return matter_device
