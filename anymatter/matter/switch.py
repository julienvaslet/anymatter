from abc import abstractmethod
from typing import List
from circuitmatter.device_types.simple_device import SimpleDevice
from circuitmatter.device_types.lighting import on_off
from anymatter.matter.device import Device


class MatterSwitch(on_off.OnOffLight):
    def __init__(self, name: str):
        super().__init__(name)

    def on(self, *args):
        pass
    
    def off(self, *args):
        pass
        

class OnOffSwitch(Device):
    def __init__(self):
        Device.__init__(self)
        self._cm_device = MatterSwitch("LED1234")
        self._cm_device.on = self.on
        self._cm_device.off = self.off

    def _get_cm_devices(self) -> List[SimpleDevice]:
        return [self._cm_device]

    @abstractmethod
    async def on(self):
        raise Exception("Not implemented")

    @abstractmethod
    async def off(self):
        raise Exception("Not implemented")
        