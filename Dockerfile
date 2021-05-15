FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /myStuff

#ADD time.py /

COPY . /myStuff
COPY ./app /myStuff/app

CMD [ "python", "/myStuff/run.py" ]