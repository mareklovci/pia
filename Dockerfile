FROM ubuntu:latest
MAINTAINER vulpeszerda87 "mareklovci@gmail.com"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /pia/requirements.txt

WORKDIR /pia

RUN pip install -r requirements.txt

COPY . /pia

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]
