FROM yuhichyoc/wagtail

RUN django-admin startproject [django-project]
COPY ./settings.py ./[django-project]/[django-project]/

RUN cd ./[django-project]/ \
    && python3 manage.py startapp [app]
