from circuitmatter.device_types.simple_device import SimpleDevice


class Capability:
    def __init__(self):
        self._circuitmatter_device = None
    
    def get_circuitmatter_device(self) -> SimpleDevice:
        if not self._circuitmatter_device:
            raise Exception("CircuitMatter device has not been set up.")

        return self._circuitmatter_device
