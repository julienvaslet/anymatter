import time
from anymatter.matter import Device
from anymatter.matter.capabilities import TemperatureSensing, RelativeHumiditySensing


class SwitchbotMeterPlus(Device):
    def __init__(self, mac: str, label: str):
        Device.__init__(self, mac, label)
        self._mac = mac
        self.vendor_id = 0x1397
        self.vendor_name = "Switchbot"
        self._last_update_ms = None
        self._timeout_ms = 10000
        
        self._temperature = TemperatureSensing()
        self.add_capability(self._temperature)

        self._humidity = RelativeHumiditySensing()
        self.add_capability(self._humidity)

    async def connect(self) -> bool:
        return True

    async def disconnect(self):
        pass

    async def refresh(self):
        current_time_ms = round(time.time() * 1000)

        if self._last_update_ms is None or self._last_update_ms + self._timeout_ms < current_time_ms:
            self.reachable = False

    def update(self, ble_device):
        self._last_update_ms = round(time.time() * 1000)
        self.reachable = True

        if ble_device.temp:
            self._temperature.value = ble_device.temp
        
        if ble_device.temp:
            self._humidity.value = ble_device.humidity

