FROM python:3.6

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential python-dev git
RUN set -ex \
        && git clone https://github.com/adafruit/Adafruit_Python_DHT.git \
	&& cd Adafruit_Python_DHT \
        && python setup.py install \
        && cd .. \
   	&& rm -rf Adafruit_Python_DHT

COPY requirments.txt .
RUN pip install -r requirments.txt

COPY src /src
WORKDIR /src
RUN ls

CMD ["python3", "dht_mqtt.py"]

