class Capability:
    def __init__(self, device_type_id: int, revision: int):
        self._device_type_id = device_type_id
        self._revision = revision
        self._servers = []

    @property
    def device_type_id(self):
        return self._device_type_id
    
    @property
    def revision(self):
        return self._revision

    @property
    def servers(self):
        return self._servers
