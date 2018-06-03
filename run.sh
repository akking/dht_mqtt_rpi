#!/bin/bash

docker build . -t dht_mqtt
docker run --detach --privileged --restart always dht_mqtt

