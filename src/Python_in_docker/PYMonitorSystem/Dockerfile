FROM python:latest

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /usr/app/src

COPY mqttmonitor.py ./

CMD [ "python","-u","./mqttmonitor.py" ]