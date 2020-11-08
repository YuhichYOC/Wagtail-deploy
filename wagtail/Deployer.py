import os
import re
import subprocess

PROJECT_NAME = '[project-name]'
HOST_IP = '[host-ip]'

DJANGO_PROJECT_NAME = '[django-project-name]'


class FileEntity:

    def __init__(self):
        self.path = ''
        self.content = []

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


class WagtailStarter:

    def __init__(self):
        self.project_name = ''

    def set_project_name(self, arg):
        self.project_name = arg

    def install_wagtail(self):
        subprocess.call(['pip3', 'install', 'wagtail'])

    def wagtail_start(self):
        subprocess.call(['wagtail', 'start', self.project_name])

    def create_media_directory(self):
        subprocess.call(['mkdir', '/' + self.project_name + '/media'])

    def create_static_directory(self):
        subprocess.call(['mkdir', '/' + self.project_name + '/static'])

    def collect_static(self):
        os.chdir('/' + self.project_name)
        subprocess.call(['python3', 'manage.py', 'collectstatic'])
        os.chdir('/')

    def run(self):
        self.install_wagtail()
        self.wagtail_start()
        self.create_media_directory()
        self.create_static_directory()
        self.collect_static()


class BasePyAppender:

    def __init__(self):
        self.project_name = ''
        self.host_ip = ''

    def set_project_name(self, arg):
        self.project_name = arg

    def set_host_ip(self, arg):
        self.host_ip = arg

    def find_installed_apps_start(self, prev_content):
        count = len(prev_content)
        p = re.compile('^ *INSTALLED_APPS = \\[')
        i = 0
        for i in range(count):
            m = p.match(prev_content[i])
            if m is not None:
                break
        return i

    def find_installed_apps_end(self, prev_content, i):
        count = len(prev_content)
        p = re.compile('^ *]')
        j = 0
        for j in range(i + 1, count):
            m = p.match(prev_content[j])
            if m is not None:
                break
        return j - 1

    def insert_installed_apps(self, prev_content):
        count = len(prev_content)
        new_content = []
        pos = self.find_installed_apps_end(prev_content, self.find_installed_apps_start(prev_content))
        for i in range(pos):
            new_content.append(prev_content[i])
        new_content.append('')
        new_content.append('    \'wagtail.contrib.sitemaps\',')
        new_content.append('    \'wagtail.contrib.routable_page\',')
        new_content.append(']')
        for j in range(pos + 2, count):
            new_content.append(prev_content[j])
        return new_content

    def find_auth_password_validators_start(self, prev_content):
        count = len(prev_content)
        p = re.compile('^ *AUTH_PASSWORD_VALIDATORS = \\[')
        i = 0
        for i in range(count):
            m = p.match(prev_content[i])
            if m is not None:
                break
        return i

    def find_auth_password_validators_end(self, prev_content, i):
        count = len(prev_content)
        p = re.compile('^ *]')
        j = 0
        for j in range(i + 1, count):
            m = p.match(prev_content[j])
            if m is not None:
                break
        return j

    def insert_allowed_host(self, prev_content):
        count = len(prev_content)
        new_content = []
        pos = self.find_auth_password_validators_end(prev_content,
                                                     self.find_auth_password_validators_start(prev_content))
        for i in range(pos):
            new_content.append(prev_content[i])
        new_content.append(']')
        new_content.append('')
        new_content.append('# Hosts/domain names that are valid for this site; required if DEBUG is False')
        new_content.append('# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts')
        new_content.append('ALLOWED_HOSTS = ["' + self.host_ip + '"]')
        for j in range(pos + 1, count):
            new_content.append(prev_content[j])
        return new_content

    def run(self):
        fe = FileEntity()
        fe.set_path('/' + self.project_name + '/' + self.project_name + '/settings/base.py')
        fe.read()
        new_content = self.insert_allowed_host(self.insert_installed_apps(fe.get_content()))
        fe.set_content(new_content)
        fe.write()


class ProjectNginxConfWriter:

    def __init__(self):
        self.project_name = ''

    def set_project_name(self, arg):
        self.project_name = arg

    def run(self):
        content = [
            'upstream wagtail {',
            '  server unix:///' + self.project_name + '/' + self.project_name + '.sock;',
            '}',
            'server {',
            '  listen 8000;',
            '  server_name example.com;',
            '  charset utf-8;',
            '  client_max_body_size 75M;',
            '  location /media {',
            '    alias /' + self.project_name + '/media;',
            '  }',
            '  location /static {',
            '    alias /' + self.project_name + '/static;',
            '  }',
            '  location / {',
            '    uwsgi_pass wagtail;',
            '    include /' + self.project_name + '/uwsgi_params;',
            '  }',
            '}'
        ]
        to_path = '/etc/nginx/sites-available/' + self.project_name + '_nginx.conf'
        fe = FileEntity()
        fe.set_path(to_path)
        fe.set_content(content)
        fe.write()


class PostProcesses:

    def __init__(self):
        self.project_name = ''
        self.django_project_name = ''

    def set_project_name(self, arg):
        self.project_name = arg

    def set_django_project_name(self, arg):
        self.django_project_name = arg

    def requirements_install(self):
        subprocess.call(['pip3', 'install', '-r', '/' + self.project_name + '/requirements.txt'])

    def run_migrate(self):
        subprocess.call(['python3', '/' + self.project_name + '/manage.py', 'migrate'])

    def copy_uwsgi_params(self):
        subprocess.call(['cp', '/etc/nginx/uwsgi_params', '/' + self.project_name + '/'])

    def link_wagtail_to_enable(self):
        subprocess.call(
            ['ln', '-s', '/etc/nginx/sites-available/' + self.project_name + '_nginx.conf', '/etc/nginx/sites-enabled'])

    def unlink_django_from_enabled(self):
        subprocess.call(['unlink', '/etc/nginx/sites-enabled/' + self.django_project_name + '_nginx.conf'])

    def run(self):
        self.requirements_install()
        self.run_migrate()
        self.copy_uwsgi_params()
        self.link_wagtail_to_enable()
        self.unlink_django_from_enabled()


if __name__ == '__main__':
    ws = WagtailStarter()
    ws.set_project_name(PROJECT_NAME)
    ws.run()
    bpa = BasePyAppender()
    bpa.set_project_name(PROJECT_NAME)
    bpa.set_host_ip(HOST_IP)
    bpa.run()
    pncw = ProjectNginxConfWriter()
    pncw.set_project_name(PROJECT_NAME)
    pncw.run()
    pp = PostProcesses()
    pp.set_project_name(PROJECT_NAME)
    pp.set_django_project_name(DJANGO_PROJECT_NAME)
    pp.run()
