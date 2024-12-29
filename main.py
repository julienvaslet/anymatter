import asyncio
import logging
import os

from switchbotmeter import DevScanner

from anymatter.kasa import KasaOnOffSwitch
from anymatter.switchbot import SwitchbotMeterPlus

async def main():
    device = KasaOnOffSwitch(ip="10.0.0.106")
    await device.run()

async def main2():
    device = SwitchbotMeterPlus(mac="ce:2a:85:c6:43:3c")
    await device.run()


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    #asyncio.run(main())
    asyncio.run(main2())
