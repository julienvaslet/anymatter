import asyncio
import logging
import os
import signal

from anymatter.matter import Hub
from anymatter.kasa import KasaOnOffSwitch
from anymatter.switchbot import SwitchbotMeterPlus


async def main():
    hub = Hub()
    hub.add_device(KasaOnOffSwitch(mac="dc:62:79:35:68:2a"))
    hub.add_device(SwitchbotMeterPlus(mac="ce:2a:85:c6:43:3c"))

    def shutdown(signalnum, frame):
        hub.shutdown()

    signal.signal(signal.SIGINT, shutdown)
    
    await hub.run()

if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    asyncio.run(main())
