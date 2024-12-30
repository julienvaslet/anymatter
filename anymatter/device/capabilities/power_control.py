from abc import abstractmethod
from circuitmatter.clusters.general.identify import Identify
from circuitmatter.clusters.general.on_off import OnOff
from circuitmatter.device_types.simple_device import SimpleDevice

from anymatter.asyncio import await_coroutine
from anymatter.device.capabilities.capability import Capability


class PowerControl(Capability):
    class CircuitMatterDevice(SimpleDevice):
        DEVICE_TYPE_ID = 0x0100
        REVISION = 3

        def __init__(self, name, capability):
            super().__init__(name)
            self._capability = capability

            self._identify = Identify()
            self.servers.append(self._identify)

            self._on_off = OnOff()
            self._on_off.on = self._on
            self._on_off.off = self._off
            self.servers.append(self._on_off)
            
        
        def set_status(self, value: bool):
            self._on_off.on_off = value
        
        def _on(self, *args):
            print("ONNN")
            try:
                await_coroutine(self._capability.on())
                print("ONNN GOOOOD")
                self.set_status(True)
            except Exception as e:
                print("EXCEEEEPT", e)
                pass
        
        def _off(self, *args):
            print("OFFFFF")
            try:
                await_coroutine(self._capability.off())
                print("OFFFF GOOOD")
                self.set_status(False)
            except Exception as e:
                print("EXCEEEEPT", e)
                pass
        

    def __init__(self):
        Capability.__init__(self)
        self._circuitmatter_device = PowerControl.CircuitMatterDevice("Light123", self)
        self._status = False

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, value: bool):
        self._status = value
        self._circuitmatter_device.set_status(self._status)

    @abstractmethod
    async def on(self):
        raise Exception("Not implemented")

    @abstractmethod
    async def off(self):
        raise Exception("Not implemented")
