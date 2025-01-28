FROM python:3.11-slim
LABEL org.opencontainers.image.authors="Julien Vaslet"
LABEL org.opencontainers.image.url="https://github.com/julienvaslet/anymatter"
LABEL org.opencontainers.image.documentation="https://github.com/julienvaslet/anymatter"
LABEL org.opencontainers.image.source="https://github.com/julienvaslet/anymatter"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.ref.name="anymatter"
LABEL org.opencontainers.image.title="Anymatter"
LABEL org.opencontainers.image.description="A virtual Matter hub for connecting any device"
LABEL org.opencontainers.image.version="0.1.0"

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
    avahi-daemon avahi-utils dbus build-essential libglib2.0-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/dbus && \
    dbus-uuidgen > /var/lib/dbus/machine-id

RUN mkdir /{app,data}
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Pipe circuitmatter prints into a proper logger, debug level, keep __future__ imports at the top of the files
RUN find $(python -m pip show circuitmatter | grep Location | cut -f2 -d':')/circuitmatter -name '*.py' | xargs -n1 sed -i '1s/^/from circuitmatter.print import print\n/'
RUN find $(python -m pip show circuitmatter | grep Location | cut -f2 -d':')/circuitmatter -name '*.py' | xargs -I'{}' bash -c "cat <(grep '^from __future__' {}) <(grep -v '^from __future__' {}) > {}~ && mv {}~ {}"

COPY main.py /app
COPY anymatter /app/anymatter

# Provide the print wrapper to circuitmatter library
RUN cp /app/anymatter/circuitmatter-print.py $(python -m pip show circuitmatter | grep Location | cut -f2 -d':')/circuitmatter/print.py

RUN <<EOR
    cat > /app/start.sh <<EOF
#!/bin/bash
set -e
dbus-daemon --system
avahi-daemon -D
python main.py $(echo "\$@")
EOF
    chmod +x /app/start.sh
EOR

ENTRYPOINT [ "/app/start.sh" ]
CMD [ "--config", "/data/devices.config" ]
