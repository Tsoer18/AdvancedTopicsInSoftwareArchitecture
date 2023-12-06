FROM python:latest

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /usr/app/src

COPY dbtopahoconnector.py ./

CMD [ "python","-u","./dbtopahoconnector.py" ]