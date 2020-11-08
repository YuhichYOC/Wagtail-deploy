import os
import subprocess

DJANGO_PROJECT_NAME = '[django-project-name]'
DJANGO_HOST = '[django-host]'

WAGTAIL_PROJECT_NAME = '[wagtail-project-name]'
WAGTAIL_HOST = '[wagtail-host]'


class FileEntity:

    def __init__(self):
        self.content = []
        self.path = ''

    def set_path(self, arg):
        self.path = arg

    def get_content(self):
        return self.content

    def set_content(self, arg):
        self.content = arg

    def read(self):
        self.content.clear()
        with open(self.path, 'r') as f:
            lines = f.read().split('\n')
            for line in lines:
                self.content.append(line)

    def write(self):
        with open(self.path, 'w') as f:
            for line in self.content:
                f.write(line)
                f.write('\n')


def replace_content(content, keyword, replacement):
    new_content = []
    for line in content:
        new_content.append(line.replace(keyword, replacement))
    return new_content


def prepare_django():
    fe = FileEntity()
    fe.set_path('start.sh')
    fe.read()
    content = fe.get_content()
    new_content = replace_content(content, '[django-name]', DJANGO_PROJECT_NAME)
    fe.set_content(new_content)
    fe.write()
    fe.set_path('reload.sh')
    fe.read()
    content = fe.get_content()
    new_content = replace_content(content, '[django-name]', DJANGO_PROJECT_NAME)
    fe.set_content(new_content)
    fe.write()
    if os.path.isdir('django'):
        fe.set_path('django/Dockerfile')
        fe.read()
        content = fe.get_content()
        new_content = replace_content(content, '[project-name]', DJANGO_PROJECT_NAME)
        fe.set_content(new_content)
        fe.write()
        fe.set_path('django/Deployer.py')
        fe.read()
        content = fe.get_content()
        new_content = replace_content(content, '[project-name]', DJANGO_PROJECT_NAME)
        new_content = replace_content(new_content, '[host-ip]', DJANGO_HOST)
        fe.set_content(new_content)
        fe.write()


def prepare_wagtail():
    fe = FileEntity()
    fe.set_path('start.sh')
    fe.read()
    content = fe.get_content()
    new_content = replace_content(content, '[wagtail-name]', WAGTAIL_PROJECT_NAME)
    fe.set_content(new_content)
    fe.write()
    if os.path.isdir('wagtail'):
        fe.set_path('wagtail/Deployer.py')
        fe.read()
        content = fe.get_content()
        new_content = replace_content(content, '[project-name]', WAGTAIL_PROJECT_NAME)
        new_content = replace_content(new_content, '[host-ip]', WAGTAIL_HOST)
        new_content = replace_content(new_content, '[django-project-name]', DJANGO_PROJECT_NAME)
        fe.set_content(new_content)
        fe.write()


if __name__ == '__main__':
    prepare_django()
    prepare_wagtail()
    subprocess.call(['chmod', '754', 'firstboot.sh'])
    subprocess.call(['chmod', '754', 'start.sh'])
    subprocess.call(['chmod', '754', 'stop.sh'])
    subprocess.call(['chmod', '754', 'reload.sh'])
    if os.path.isdir('django'):
        subprocess.call(['chmod', '754', 'django/build.sh'])
        subprocess.call('django/build.sh')
    if os.path.isdir('wagtail'):
        subprocess.call('./firstboot.sh')
        subprocess.call(['docker', 'cp', 'wagtail/Deployer.py', 'wagtail:/'])
        subprocess.call(['docker', 'exec', 'wagtail', '/bin/bash', '-c', 'python3 Deployer.py'])
        subprocess.call('./stop.sh')
