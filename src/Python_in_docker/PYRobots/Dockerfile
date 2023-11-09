FROM python:latest

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /usr/app/src

COPY mqttconnector.py ./

CMD [ "python","-u","./mqttconnector.py" ]