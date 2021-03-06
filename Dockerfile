FROM daocloud/ci-python:2.7

MAINTAINER Lawrence Liu<lawrence@betterlife.io>

# RUN echo "deb http://mirrors.163.com/ubuntu precise main universe" > /etc/apt/sources.list
# RUN apt-get -y update
# RUN apt-get -y install build-essential python python-dev python-pip
RUN mkdir -p /tmp/app
ADD . /tmp/app

RUN pip install -r /tmp/app/requirements.txt

EXPOSE 80
WORKDIR "/tmp/app"
ENTRYPOINT ["python", "app.py"]