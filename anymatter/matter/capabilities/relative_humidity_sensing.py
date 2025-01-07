import logging

from anymatter.asyncio import await_coroutine
from anymatter.matter.capabilities.capability import Capability
from anymatter.matter.clusters import RelativeHumidityMeasurementCluster

logger = logging.getLogger(__name__)


class RelativeHumiditySensing(Capability):
    def __init__(self):
        Capability.__init__(self, 0x0307, 2)
        self._measurement = RelativeHumidityMeasurementCluster()
        self.servers.append(self._measurement)

    @property
    def value(self) -> float:
        return self._measurement.MeasuredValue / 100.0

    @value.setter
    def value(self, value: float):
        i_value = round(value * 100)

        if i_value != self._measurement.MeasuredValue:
            logger.info(f"Relative humidity is now {value} ({i_value}).")

        self._measurement.MeasuredValue = i_value
