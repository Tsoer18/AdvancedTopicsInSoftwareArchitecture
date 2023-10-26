FROM python:latest

ADD requirements.txt /
RUN pip install -r requirements.txt
RUN python -m pip install "pymongo[srv]"

WORKDIR /usr/app/src

COPY mqttconnector.py ./
COPY PYmongoGetDatabase.py ./

CMD [ "python","-u","./mqttconnector.py" ]