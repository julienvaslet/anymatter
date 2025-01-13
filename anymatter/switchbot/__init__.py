from anymatter.switchbot.meterplus import SwitchbotMeterPlus


async def find_switchbot_device(mac: str, label: str):
    return SwitchbotMeterPlus(mac, label)
