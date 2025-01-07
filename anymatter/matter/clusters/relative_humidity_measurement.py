from circuitmatter.data_model import Cluster, NumberAttribute


class RelativeHumidityMeasurementCluster(Cluster):
    CLUSTER_ID = 0x0405

    MeasuredValue = NumberAttribute(0x0000, signed=True, bits=16, default=0x0000, X_nullable=True, P_reportable=True)
    MinMeasuredValue = NumberAttribute(0x0001, signed=True, bits=16, default=0x0000, X_nullable=True)
    MaxMeasuredValue = NumberAttribute(0x0002, signed=True, bits=16, default=0x2710, X_nullable=True)
