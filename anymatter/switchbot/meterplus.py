from anymatter.matter import Device
from anymatter.matter.capabilities import TemperatureSensing, RelativeHumiditySensing


class SwitchbotMeterPlus(Device):
    def __init__(self, mac: str, label: str):
        Device.__init__(self, mac, label)
        self._mac = mac
        self.vendor_id = 0x1397
        self.vendor_name = "Switchbot"
        
        self._temperature = TemperatureSensing()
        self.add_capability(self._temperature)

        self._humidity = RelativeHumiditySensing()
        self.add_capability(self._humidity)

    async def connect(self) -> bool:
        return True

    async def disconnect(self):
        pass

    def update(self, ble_device):
        # TODO: implement last udpate, then reachable with timeout?

        if ble_device.temp:
            self._temperature.value = ble_device.temp
        
        if ble_device.temp:
            self._humidity.value = ble_device.humidity

