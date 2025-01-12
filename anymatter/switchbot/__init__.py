from anymatter.switchbot.meterplus import SwitchbotMeterPlus


def find_switchbot_device(mac: str, label: str):
    return SwitchbotMeterPlus(mac)
