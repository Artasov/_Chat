FROM python:3.8

COPY requirements.txt /srv/requirements.txt
COPY entrypoint.sh /srv/entrypoint.sh
RUN apt-get update \
    && apt-get install -y dos2unix

RUN apt-get update \
    && apt-get install -yyq netcat

RUN apt-get install -y libpq-dev \
    && python -m pip install --upgrade pip \
    && python -m pip install -r /srv/requirements.txt

COPY . /srv
WORKDIR /srv

RUN echo "Europe/Moscow" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

RUN dos2unix /srv/entrypoint.sh && apt-get --purge remove -y dos2unix
ENTRYPOINT ["./entrypoint.sh"]


