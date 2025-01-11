import asyncio
import logging
import os
import re
import signal
import sys
from argparse import ArgumentParser
from collections import namedtuple
from typing import List
from anymatter.matter import Hub
from anymatter.kasa import KasaOnOffSwitch
from anymatter.switchbot import SwitchbotMeterPlus


Device = namedtuple("Device", "model mac name")

class Config:
    devices: List[Device] = []
    loglevel: str = "INFO"


def parse_args(args) -> Config:
    parser = ArgumentParser(prog="anymatter")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-d", "--device", action="append", default=[], dest="devices")
    options = parser.parse_args(args)

    config = Config()

    if options.verbose:
        config.loglevel = "DEBUG"

    device_re = re.compile(r"^(?P<model>[^/]+)/(?P<mac>[A-Fa-f0-9]{2}(?::[A-Fa-f0-9]{2}){5})(?:/(?P<label>.*))?$")

    for device_config in options.devices:
        m = re.match(device_re, device_config)
        config.devices.append(Device(m.group("model"), m.group("mac"), m.group("label")))

    return config

async def main(devices: List[Device]):
    devices_resolver = {
        "kasa": KasaOnOffSwitch,
        "switchbot": SwitchbotMeterPlus,
    }

    hub = Hub()

    for device in devices:
        model = device.model.lower()

        if not model in devices_resolver:
            raise Exception(f"Unsupported device brand/model \"{device.model}\".")

        # TODO: Use real resolvers and label
        hub.add_device(devices_resolver[model](mac=device.mac))

    def shutdown(signalnum, frame):
        hub.shutdown()

    signal.signal(signal.SIGINT, shutdown)
    
    await hub.run()

if __name__ == "__main__":
    config = parse_args(sys.argv[1:])
    logging.basicConfig(level=os.environ.get("LOGLEVEL", config.loglevel))
    asyncio.run(main(config.devices))
