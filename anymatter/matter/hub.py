import logging
from circuitmatter import CircuitMatter
from circuitmatter.pase import compute_qr_code
from anymatter import __version__
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

    def _debug_endpoints(self):
        def log(prefix, data):
            for line in f"{data}".split("\n"):
                logger.info(f"{prefix} {line}")

        for endpoint, clusters in self._matter._endpoints.items():
            logger.info(f"[Endpoint#{endpoint}]")

            for cluster_id, cluster in clusters.items():
                logger.info(f"[Endpoint#{endpoint}][{type(cluster).__name__}][ClusterID] 0x{cluster_id:04x}")

                for attribute, _ in type(cluster)._attributes():
                    value = getattr(cluster, attribute)

                    if isinstance(value, list): 
                        for index, item in enumerate(value):
                            log(f"[Endpoint#{endpoint}][{type(cluster).__name__}][{attribute}][{index}]", item)

                    else:
                        log(f"[Endpoint#{endpoint}][{type(cluster).__name__}][{attribute}]", value)
    
    async def run(self):
        self._running = True
        logger.info("Configuring matter device...")

        self._matter = CircuitMatter(
            vendor_id=self._vendor_id,
            product_id=self._product_id,
            product_name=self._product_name,
        )

        self._matter.root_node.descriptor.DeviceTypeList[0].DeviceType = 0x000e
        self._matter.root_node.descriptor.DeviceTypeList[0].Revision = 1

        # Bridge??
        self._matter.root_node.servers[3].feature_map = 0x01
        self._matter.root_node.servers[3].vendor_id = 0x0269
        self._matter.root_node.servers[3].vendor_name = "Anymatter"
        self._matter.root_node.servers[3].product_id = 0x0482
        self._matter.root_node.servers[3].product_name = "Anymatter Hub"
        self._matter.root_node.servers[3].node_label = "Anymatter Hub"
        self._matter.root_node.servers[3].hardware_version_string = __version__
        self._matter.root_node.servers[3].software_version_string = __version__
        self._matter.root_node.servers[3].product_url = "https://github.com/julienvaslet/anymatter"

        logger.info("Matter device is up.")
        self._display_qr_code()

        for device in self._devices:
            self._matter.add_device(device)

        self._debug_endpoints()

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

    