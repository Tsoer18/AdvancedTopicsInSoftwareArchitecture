# Stage 1: Build dependencies and libraries
FROM alpine:latest as builder

WORKDIR /app

# Install dependencies
RUN apk update && \
    apk add paho-mqtt-c paho-mqtt-c-dev build-base gcc cmake openssl-dev git doxygen

# Clone and build nlohmann/json
RUN git clone --branch=v3.10.4 --depth=1 https://github.com/nlohmann/json.git /nlohmann/json

# Clone and build paho.mqtt.c
RUN git clone https://github.com/eclipse/paho.mqtt.c.git && \
    cd paho.mqtt.c && \
    cmake -Bbuild -H. -DPAHO_ENABLE_TESTING=OFF -DPAHO_BUILD_STATIC=ON \
    -DPAHO_WITH_SSL=ON -DPAHO_HIGH_PERFORMANCE=ON && cd build && make install

# Clone and build paho.mqtt.cpp
RUN git clone https://github.com/eclipse/paho.mqtt.cpp.git && \
    cd paho.mqtt.cpp && \
    cmake -Bbuild -H. -DPAHO_BUILD_STATIC=ON \
    -DPAHO_BUILD_DOCUMENTATION=TRUE -DPAHO_BUILD_SAMPLES=TRUE && \
    cd build && \
    make install

COPY ./mqttScheduler.cpp /app

RUN g++ mqttScheduler.cpp -o mqttScheduler -lpaho-mqttpp3 -lpaho-mqtt3c -I/nlohmann/json/single_include

CMD ["./mqttScheduler"]
