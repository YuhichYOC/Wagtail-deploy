FROM nginx

RUN apt-get update \
    && apt-get -y install tree vim python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install Django
RUN django-admin.py startproject [project-name]
RUN pip3 install uwsgi
RUN mkdir /etc/nginx/sites-available \
    && mkdir /etc/nginx/sites-enabled \
    && mkdir /[project-name]/media \
    && mkdir /[project-name]/static

COPY ./Deployer.py /[project-name]/
RUN python3 /[project-name]/Deployer.py

RUN cp /etc/nginx/uwsgi_params /[project-name]/
RUN ln -s /etc/nginx/sites-available/[project-name]_nginx.conf /etc/nginx/sites-enabled/
RUN cd /[project-name] \
    && python3 manage.py collectstatic
RUN /etc/init.d/nginx restart
