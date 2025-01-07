from circuitmatter.data_model import BoolAttribute, Cluster, NumberAttribute, UTF8StringAttribute


class BridgedDeviceBasicInformationCluster(Cluster):
    CLUSTER_ID = 0x0039

    vendor_name = UTF8StringAttribute(0x01, max_length=32, default="Anymatter", optional=True)
    vendor_id = NumberAttribute(0x02, signed=False, bits=16, optional=True)
    product_name = UTF8StringAttribute(0x03, max_length=32, default="Anymatter device")
    product_id = NumberAttribute(0x04, signed=False, bits=16, default=0, optional=True)
    node_label = UTF8StringAttribute(0x05, max_length=32, default="", optional=True)
    hardware_version = NumberAttribute(0x07, signed=False, bits=16, default=0, optional=True)
    hardware_version_string = UTF8StringAttribute(0x08, min_length=1, max_length=64, default="Unknown", optional=True)
    software_version = NumberAttribute(0x09, signed=False, bits=16, default=0, optional=True)
    software_version_string = UTF8StringAttribute(0x0A, min_length=1, max_length=64, default="Unknown", optional=True)
    manufacturing_date = UTF8StringAttribute(0x0B, min_length=8, max_length=16, default="Unknown", optional=True)
    part_number = UTF8StringAttribute(0x0C, max_length=32, default="", optional=True)
    product_url = UTF8StringAttribute(0x0D, max_length=256, default="", optional=True)
    product_label = UTF8StringAttribute(0x0E, max_length=64, default="", optional=True)
    serial_number = UTF8StringAttribute(0x0F, max_length=32, default="", optional=True)
    reachable = BoolAttribute(0x11, default=True)
    unique_id = UTF8StringAttribute(0x12, max_length=32, default="")

