from circuitmatter.data_model import Cluster, NumberAttribute


class TemperatureMeasurementCluster(Cluster):
    CLUSTER_ID = 0x0402
    REVISION = 4

    MeasuredValue = NumberAttribute(0x0000, signed=True, bits=16, default=0, X_nullable=True, P_reportable=True)
    MinMeasuredValue = NumberAttribute(0x0001, signed=True, bits=16, default=-5000, X_nullable=True)
    MaxMeasuredValue = NumberAttribute(0x0002, signed=True, bits=16, default=15000, X_nullable=True)
