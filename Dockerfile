FROM ubuntu:20.04 as app
WORKDIR /app

RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install -y python3.10 python3.10-dev
RUN apt install python3-pip -y
RUN apt install pkg-config -y
RUN apt install libmysqlclient-dev -y
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]