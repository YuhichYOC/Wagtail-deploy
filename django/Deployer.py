import re

PROJECT_NAME = '[project-name]'
HOST_IP = '[host-ip]'


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


class ProjectNginxConfWriter:

    def __init__(self):
        self.project_name = ''

    def set_project_name(self, arg):
        self.project_name = arg

    def run(self):
        content = [
            'upstream django {',
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
            '    uwsgi_pass django;',
            '    include /' + self.project_name + '/uwsgi_params;',
            '  }',
            '}'
        ]
        to_path = '/etc/nginx/sites-available/' + self.project_name + '_nginx.conf'
        fe = FileEntity()
        fe.set_path(to_path)
        fe.set_content(content)
        fe.write()


class NginxConfAppender:

    def run(self):
        fe = FileEntity()
        fe.set_path('/etc/nginx/nginx.conf')
        fe.read()
        content = fe.get_content()
        new_content = []
        p = re.compile('^( *)include +/etc/nginx/conf\\.d/\\*\\.conf;')
        for line in content:
            m = p.match(line)
            if m is not None:
                new_content.append(m.group(1) + 'include /etc/nginx/sites-enabled/*;')
            new_content.append(line)
        fe.set_content(new_content)
        fe.write()


class SettingsPyAppender:

    def __init__(self):
        self.project_name = ''
        self.host_ip = ''

    def set_project_name(self, arg):
        self.project_name = arg

    def set_host_ip(self, arg):
        self.host_ip = arg

    def insert_import_statement(self, prev_content):
        count = len(prev_content)
        new_content = []
        p_from = re.compile('^( *)from')
        p_import = re.compile('^( *)import')
        i = 0
        for i in range(count):
            m_from = p_from.match(prev_content[i])
            m_import = p_import.match(prev_content[i])
            if m_from is not None:
                new_content.append(m_from.group(1) + 'import os')
                new_content.append(prev_content[i])
                break
            if m_import is not None:
                new_content.append(m_import.group(1) + 'import os')
                new_content.append(prev_content[i])
                break
            new_content.append(prev_content[i])
        for j in range(i + 1, count):
            new_content.append(prev_content[j])
        return new_content

    def insert_host_ip(self, prev_content):
        new_content = []
        p = re.compile('^( *)(ALLOWED_HOSTS *= *\\[)')
        for line in prev_content:
            m = p.match(line)
            if m is not None:
                new_content.append(m.group(1) + m.group(2) + '"' + self.host_ip + '"]')
            else:
                new_content.append(line)
        return new_content

    def insert_static_root_define(self, prev_content):
        count = len(prev_content)
        new_content = []
        p = re.compile('^( *)STATIC_URL *= *')
        i = 0
        for i in range(count):
            new_content.append(prev_content[i])
            m = p.match(prev_content[i])
            if m is not None:
                new_content.append(m.group(1) + 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")')
                break
        for j in range(i + 1, count):
            new_content.append(prev_content[j])
        return new_content

    def run(self):
        fe = FileEntity()
        fe.set_path('/' + self.project_name + '/' + self.project_name + '/settings.py')
        fe.read()
        new_content = self.insert_static_root_define(
            self.insert_host_ip(self.insert_import_statement(fe.get_content())))
        fe.set_content(new_content)
        fe.write()


if __name__ == '__main__':
    pncw = ProjectNginxConfWriter()
    pncw.set_project_name(PROJECT_NAME)
    pncw.run()
    nca = NginxConfAppender()
    nca.run()
    spa = SettingsPyAppender()
    spa.set_project_name(PROJECT_NAME)
    spa.set_host_ip(HOST_IP)
    spa.run()
