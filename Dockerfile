FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    avahi-daemon avahi-utils dbus build-essential libglib2.0-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/dbus && \
    dbus-uuidgen > /var/lib/dbus/machine-id

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app
COPY anymatter /app/anymatter
COPY matter-device-state.json /app

CMD dbus-daemon --system && \
    avahi-daemon -D && \
    python -u main.py
