FROM ubuntu

RUN apt-get update \
    && apt-get -y install \
    tree \
    vim \
    python3 \
    python3-pip

RUN pip3 install --upgrade pip \
    && pip3 install \
    wheel \
    wagtail \
    django-colorful \
    django-el-pagination \
    django-social-share \
    puput

RUN wagtail start [myproject]

COPY ./base.py /[myproject]/[myproject]/settings/
COPY ./urls.py /[myproject]/[myproject]/

RUN pip3 install -r ./[myproject]/requirements.txt \
    && python3 ./[myproject]/manage.py migrate \
    && python3 ./[myproject]/manage.py puput_initial_data
