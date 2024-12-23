import asyncio

from circuitmatter import CircuitMatter
from circuitmatter.device_types.lighting import on_off
from anymatter.kasa import KasaOnOffSwitch

class LED(on_off.OnOffLight):
    def __init__(self, name):
        super().__init__(name)
        self._value = False

    def on(self):
        self._value = True
        print("ON")
    
    def off(self):
        self._value = False
        print("OFF")

async def main():
    device = KasaOnOffSwitch(ip="10.0.0.106")
    await device.run()

def mattermain():
    matter = CircuitMatter()
    led = LED("led1")
    matter.add_device(led)

    while True:
        matter.process_packets()


if __name__ == "__main__":
    #asyncio.run(main())
    mattermain()
