#Source: https://dev.to/riverfount/dockerize-a-flask-app-17ag
FROM python:3.7

RUN apt update && apt-get upgrade -y
RUN apt install python -y
RUN apt install python-pip -y
RUN pip install --upgrade pip && pip install pipenv
RUN mkdir /root/Genisys
WORKDIR /root/Genisys


ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "/root/Genisys/app.py"
ENV FLASK_DEBUG True


COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 1337
CMD flask run --port 1337 --host 0.0.0.0
