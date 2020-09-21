FROM nginx

RUN apt-get update \
    && apt-get -y install tree vim python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install wagtail
# It not works ... "RUN wagtail start" makes manage.py without collectstatic command.
RUN wagtail start [project-name]

RUN mkdir /etc/nginx/sites-available \
    && mkdir /etc/nginx/sites-enabled \
    && mkdir /[project-name]/media \
    && mkdir /[project-name]/static

COPY ./Deployer.py /[project-name]/
RUN python3 /[project-name]/Deployer.py

RUN pip3 install -r /[project-name]/requirements.txt \
    && python3 /[project-name]/manage.py migrate

RUN cd /[project-name] \
    && pip3 install uwsgi
RUN cp /etc/nginx/uwsgi_params /[project-name]/
RUN ln -s /etc/nginx/sites-available/[project-name]_nginx.conf /etc/nginx/sites-enabled/
RUN cd /[project-name] \
    && python3 manage.py collectstatic
RUN /etc/init.d/nginx restart
