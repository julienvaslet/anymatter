import logging
from circuitmatter import CircuitMatter
from circuitmatter.pase import compute_qr_code
from anymatter.matter import Device
from anymatter.qrcode import print_qr_code

logger = logging.getLogger(__name__)


class Hub:
    def __init__(self):
        self._matter = None
        self._running = True
        self._product_name = "Anymatter Hub"
        self._vendor_id = 0xFFF4
        self._product_id = 0x1234
        self._devices = []
    
    def _display_qr_code(self):
        if not self._matter:
            return
        
        encoded = compute_qr_code(self._vendor_id, self._product_id, self._matter.nonvolatile["discriminator"], self._matter.nonvolatile["passcode"])
        print_qr_code(f"MT:{encoded}", f"{self._product_name}\nManual code: {self._matter.nonvolatile['manual_code']}")

    def add_device(self, device: Device):
        self._devices.append(device)
    
    async def run(self):
        self._running = True
        logger.info("Configuring matter device...")

        self._matter = CircuitMatter(
            vendor_id=self._vendor_id,
            product_id=self._product_id,
            product_name=self._product_name,
        )

        logger.info("Matter device is up.")
        self._display_qr_code()

        for device in self._devices:
            self._matter.add_device(device)

        while self._running:
            for device in self._devices:
                await device.tick()
            
            self._matter.process_packets()

        logger.info("Shutting down...")

        for device in self._devices:
            await device.disconnect()

    def shutdown(self):
        logger.info("Shutdown requested.")
        self._running = False

    