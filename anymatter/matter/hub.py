import logging
from circuitmatter import CircuitMatter
from circuitmatter.pase import compute_qr_code
from anymatter.qrcode import print_qr_code

logger = logging.getLogger(__name__)


class Hub:
    def __init__(self):
        self._matter = None
        self._running = True
        self._product_name = "Anymatter Hub"
        self._vendor_id = 0xFFF4
        self._product_id = 0x1234
    
    def _display_qr_code(self):
        if not self._matter:
            return
        
        encoded = compute_qr_code(self._vendor_id, self._product_id, self._matter.nonvolatile["discriminator"], self._matter.nonvolatile["passcode"])
        print_qr_code(f"MT:{encoded}", f"{self._product_name}\nManual code: {self._matter.nonvolatile['manual_code']}")
    
    def run(self):
        self._running = True
        logger.info("Configuring matter device...")

        self._matter = CircuitMatter(
            vendor_id=self._vendor_id,
            product_id=self._product_id,
            product_name=self._product_name,
        )

        logger.info("Matter device is up.")

        self._display_qr_code()

        while self._running:
            self._matter.process_packets()

        logger.info("Shutting down...")

    def shutdown(self):
        logger.info("Shutdown requested.")
        self._running = False

    