from anymatter.matter import Device
from anymatter.matter.capabilities import TemperatureSensing, RelativeHumiditySensing
from switchbotmeter import DevScanner


class SwitchbotMeterPlus(Device):
    def __init__(self, mac: str, label: str):
        Device.__init__(self, mac, label)
        self._mac = mac
        self.vendor_id = 0x1397
        self.vendor_name = "Switchbot"
        # TODO: Dev scanner seems to slow matter communication, aggregate?
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
        for device in next(self._scanner):
            if device.mac != self._mac:
                continue

            return [device.temp, device.humidity]
        
        return [None, None]
