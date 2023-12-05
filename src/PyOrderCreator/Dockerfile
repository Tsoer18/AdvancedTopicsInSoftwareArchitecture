FROM python:latest

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /usr/app/src

COPY PyOrderCreater.py ./

CMD [ "python","-u","./PyOrderCreater.py" ]