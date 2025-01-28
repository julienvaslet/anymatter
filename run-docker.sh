#!/bin/bash
basedir=$(cd `dirname $0`; pwd)
docker build -t anymatter ${basedir}

# Network host for TCP/UDP communication
# Privilged for Bluetooth LE communication
container=$(docker run --network=host --privileged --mount type=bind,src="${basedir}/data",dst=/data -d anymatter)
docker logs --follow ${container}

echo "Stopping container ${container}..."
docker stop ${container}
echo "Stopped."