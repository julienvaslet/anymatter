import logging
from abc import abstractmethod
from circuitmatter.clusters.general.on_off import OnOff

from anymatter.asyncio import await_coroutine
from anymatter.matter.capabilities.capability import Capability

logger = logging.getLogger(__name__)


class PowerControl(Capability):
    def __init__(self, name: str):
        Capability.__init__(self, 0x0100, 3)
        self._name = name
        self._on_off = OnOff()
        self._on_off.on = self._on
        self._on_off.off = self._off
        self.servers.append(self._on_off)

    @property
    def status(self) -> bool:
        return self._on_off.OnOff

    @status.setter
    def status(self, value: bool):
        if value == self._on_off.OnOff:
            return
        
        self._on_off.OnOff = value
        status = "on" if value else "off"
        logger.info(f"{self._name} has been turned {status}.")

    def _on(self, *args):
        logger.info(f"Turning on {self._name}...")

        try:
            await_coroutine(self.on())
            self.status = True

        except Exception as e:
            logger.error(f"An error has occured while turning {self._name} on: {e}")
            pass
    
    def _off(self, *args):
        logger.info(f"Turning off {self._name}...")

        try:
            await_coroutine(self.off())
            self.status = False

        except Exception as e:
            logger.error(f"An error has occured while turning {self._name} off: {e}")
            pass
    
    @abstractmethod
    async def on(self):
        raise Exception("Not implemented")

    @abstractmethod
    async def off(self):
        raise Exception("Not implemented")
