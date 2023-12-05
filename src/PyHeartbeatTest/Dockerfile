FROM python:latest

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /usr/app/src

COPY heartbeatTest.py ./

CMD [ "python","-u","./heartbeatTest.py" ]