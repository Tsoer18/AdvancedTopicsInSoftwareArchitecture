FROM alpine:latest

WORKDIR /app

COPY ./HelloWorld.cpp /app

RUN apk update && \
    apk add paho-mqtt-c paho-mqtt-c-dev build-base gcc cmake openssl-dev git doxygen 

RUN git clone https://github.com/eclipse/paho.mqtt.c.git && \
    cd paho.mqtt.c && \
    cmake -Bbuild -H. -DPAHO_ENABLE_TESTING=OFF -DPAHO_BUILD_STATIC=ON \
    -DPAHO_WITH_SSL=ON -DPAHO_HIGH_PERFORMANCE=ON && cd build && make install

RUN git clone https://github.com/eclipse/paho.mqtt.cpp.git && \
    cd paho.mqtt.cpp && \
    cmake -Bbuild -H. -DPAHO_BUILD_STATIC=ON \
    -DPAHO_BUILD_DOCUMENTATION=TRUE -DPAHO_BUILD_SAMPLES=TRUE && \
    cd build && \
    make install


RUN g++ HelloWorld.cpp -o HelloWorld -lpaho-mqttpp3 -lpaho-mqtt3c

CMD ["./HelloWorld"]


