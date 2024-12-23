from anymatter.device.switch import OnOffSwitch
from anymatter.kasa.device import KasaDevice

class KasaOnOffSwitch(KasaDevice, OnOffSwitch):
    def __init__(self, ip: str):
        super().__init__(ip)