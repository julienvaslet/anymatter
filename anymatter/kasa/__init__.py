from anymatter.kasa.switch import KasaOnOffSwitch


def find_kasa_device(mac: str, label: str):
    return KasaOnOffSwitch(mac)
