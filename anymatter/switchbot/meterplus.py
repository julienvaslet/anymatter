from anymatter.matter import Device
from anymatter.matter.capabilities import TemperatureSensing, RelativeHumiditySensing
from switchbotmeter import DevScanner


class SwitchbotMeterPlus(Device):
    def __init__(self, mac: str):
        super().__init__(mac)
        self._mac = mac
        self._scanner = DevScanner(macs=[self._mac])
        
        self._temperature = TemperatureSensing()
        self.add_capability(self._temperature)

        self._humidity = RelativeHumiditySensing()
        self.add_capability(self._humidity)

    async def connect(self) -> bool:
        return True

    async def disconnect(self):
        pass

    async def refresh(self):
        temperature, humidity = self.get_values()

        if temperature is not None:
            self._temperature.value = temperature

        if humidity is not None:
            self._humidity.value = humidity
    
    def get_values(self):
        # need root capability for "ble on", look at setcap command
        for device in next(self._scanner):
            if device.mac != self._mac:
                continue

            return [device.temp, device.humidity]
        
        return [None, None]
