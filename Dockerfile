FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir broadlink pyyaml paho-mqtt flask

COPY . .

CMD ["python", "-m", "broadlinky.command_line", "server"]

