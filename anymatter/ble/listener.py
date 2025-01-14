import asyncio
import atexit
import threading
import logging
from switchbotmeter import DevScanner

logger = logging.getLogger(__name__)


class BleListener:
    _instance = None

    def __init__(self):
        self._running = False
        self._known_devices = {}
        self._callbacks = {}
        self._thread = threading.Thread(target=self.run, args=())
        self._thread.daemon = True
        self._thread.start()

    @property
    def running(self) -> bool:
        return self._running

    def run(self):
        logger.debug("Listener thread started.")
        self._running = True

        # TODO: Directly use bluepy
        scanner = DevScanner(wait=4)

        while self._running:
            for device in next(scanner):
                mac = device.device.addr.lower()
                self._known_devices[mac] = device

                if mac in self._callbacks:
                    self._callbacks[mac](device)

    def register(self, mac: str, callback):
        self._callbacks[mac.lower()] = callback

    def unregister(self, mac: str):
        if mac in self._callbacks:
            del self._callbacks[mac]

    def stop(self):
        logger.debug("Stopping listener thread...")
        self._running = False

        if self._thread:
            self._thread.join()

        logger.debug("Listener thread stopped.")

    async def find_device(self, mac: str, timeout_ms=10000):
        mac = mac.lower()
        logger.debug(f"Looking for device \"{mac}\"...")

        waited_ms = 0
        while mac not in self._known_devices and waited_ms <= timeout_ms:
            await asyncio.sleep(0.5)
            waited_ms += 500

        if logger.isEnabledFor(logging.DEBUG):
            if mac in self._known_devices:
                logger.debug(f"Device \"{mac}\" found.")
            else:
                logger.debug(f"Device \"{mac}\" not found.")

        return self._known_devices[mac] if mac in self._known_devices else None

    @staticmethod
    def get():
        if not BleListener._instance:
            BleListener._instance = BleListener()
        
        return BleListener._instance


@atexit.register
def gracefully_stop_ble():
    if BleListener._instance:
        BleListener.get().stop()