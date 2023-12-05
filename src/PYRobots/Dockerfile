FROM python:latest

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /usr/app/src

COPY PyRobts.py ./

CMD [ "python","-u","./PyRobts.py" ]