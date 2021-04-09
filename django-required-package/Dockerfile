FROM nginx

RUN apt-get update \
    && apt-get -y install tree vim python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install Django
RUN pip3 install uwsgi