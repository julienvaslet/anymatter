from anymatter.matter.temperature import TemperatureSensor
from switchbotmeter import DevScanner


class SwitchbotMeterPlus(TemperatureSensor):
    def __init__(self, mac: str):
        super().__init__()
        self._mac = mac
        self._scanner = DevScanner(macs=[self._mac])

    async def connect(self) -> bool:
        return True

    async def disconnect(self):
        pass

    async def refresh(self):
        value = self.get_value()

        if value is not None:
            self.value = value
    
    def get_value(self):
        # need libglib2.0-dev to install?
        # need root capability for "ble on", look at setcap command
        for device in next(self._scanner):
            if device.mac != self._mac:
                continue

            return(device.temp)
        
        return None
