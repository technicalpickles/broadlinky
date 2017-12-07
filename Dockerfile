FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir broadlink pyyaml

COPY . .

CMD ["python", "-m", "broadlinky.command_line", "server"]

