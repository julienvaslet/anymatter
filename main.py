import asyncio
import logging
import os
import signal

from switchbotmeter import DevScanner

from anymatter.matter import Hub
from anymatter.kasa import KasaOnOffSwitch
from anymatter.switchbot import SwitchbotMeterPlus

def main():
    hub = Hub()

    def shutdown(signalnum, frame):
        hub.shutdown()

    signal.signal(signal.SIGINT, shutdown)
    hub.run()

async def main1():
    device = KasaOnOffSwitch(mac="dc:62:79:35:68:2a")
    await device.run()

async def main2():
    device = SwitchbotMeterPlus(mac="ce:2a:85:c6:43:3c")
    await device.run()


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    #asyncio.run(main1())
    #asyncio.run(main2())
    main()
