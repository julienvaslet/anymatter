import asyncio

class Device:
    def __init__(self):
        self._connected = False

    async def run(self):
        self._connected = await self.connect()

        # TODO: Retry?
        if not self._connected:
            print("Unable to connect to the device.")
            return

        await asyncio.sleep(2)
        await self.disconnect()

    async def connect(self) -> bool:
        pass

    async def disconnect(self):
        pass