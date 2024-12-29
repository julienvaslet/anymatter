import logging
from typing import List
from circuitmatter.data_model import Cluster, NumberAttribute
from circuitmatter.clusters.general.identify import Identify
from circuitmatter.device_types.simple_device import SimpleDevice
from anymatter.device.device import Device

logger = logging.getLogger(__name__)


class TemperatureMeasurement(Cluster):
    CLUSTER_ID = 0x0402
    REVISION = 4

    MeasuredValue = NumberAttribute(
        0x0000, signed=True, bits=16, default=0, X_nullable=True, P_reportable=True
    )
    MinMeasuredValue = NumberAttribute(
        0x0001, signed=True, bits=16, default=-5000, X_nullable=True
    )
    MaxMeasuredValue = NumberAttribute(
        0x0002, signed=True, bits=16, default=15000, X_nullable=True
    )

    def __init__(self, refresh_callback = None):
        super().__init__()
        self._refresh_callback = refresh_callback

    def __getattribute__(self, value):
        if value == "MeasuredValue" and callable(self._refresh_callback):
            self._refresh_callback()

        return super().__getattribute__(value)


class MatterTemperatureSensor(SimpleDevice):
    DEVICE_TYPE_ID = 0x0302
    REVISION = 2

    def __init__(self, name: str, refresh_callback = None):
        super().__init__(name)
        self._identify = Identify()
        self.servers.append(self._identify)

        self.value = TemperatureMeasurement(refresh_callback)
        self.servers.append(self.value)


class TemperatureSensor(Device):
    def __init__(self):
        self._cm_device = MatterTemperatureSensor("TEMP1234", self._refresh)

    def _get_cm_devices(self) -> List[SimpleDevice]:
        return [self._cm_device]

    def _refresh(self):
        print("SHOULD REFRESSSSSSSSHHHHH")

    @property
    def value(self) -> float:
        return self._cm_device.value.MeasuredValue / 100.0

    @value.setter
    def value(self, value: float):
        i_value = round(value * 100)

        if i_value != self._cm_device.value.MeasuredValue:
            logger.info(f"Temperature is now {value} ({i_value}).")

        self._cm_device.value.MeasuredValue = i_value


        