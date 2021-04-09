import os
import re
import subprocess


class FileEntity:

    def __init__(self):
        self.f_path: str = ''
        self.f_content: list = []
        self.f_regexp_replace_file_pattern_indicator: str = 'pattern:'
        self.f_regexp_replace_file_replacement_indicator: str = 'replacement:'

    @property
    def path(self) -> str:
        return self.f_path

    @property
    def content(self) -> list:
        return self.f_content

    @property
    def regexp_replace_file_pattern_indicator(self) -> str:
        return self.f_regexp_replace_file_pattern_indicator

    @property
    def regexp_replace_file_replacement_indicator(self) -> str:
        return self.f_regexp_replace_file_replacement_indicator

    @path.setter
    def path(self, arg: str):
        self.f_path = arg

    @content.setter
    def content(self, arg: list):
        self.f_content = arg

    @regexp_replace_file_pattern_indicator.setter
    def regexp_replace_file_pattern_indicator(self, arg: str):
        self.f_regexp_replace_file_pattern_indicator = arg

    @regexp_replace_file_replacement_indicator.setter
    def regexp_replace_file_replacement_indicator(self, arg: str):
        self.f_regexp_replace_file_replacement_indicator = arg

    def read(self) -> None:
        self.content = []
        with open(self.path, 'r') as f:
            self.content.extend(f.read().split('\n'))
        return None

    def write(self) -> None:
        with open(self.path, 'w') as f:
            for line in self.content:
                f.write(line)
                f.write('\n')
        return None

    def rewrite(self, content: list) -> None:
        f = FileEntity()
        f.path = self.path
        f.content = content
        f.write()
        return None

    def append(self, content: list) -> None:
        f = FileEntity()
        f.path = self.path
        f.read()
        f.content.extend(content)
        f.write()
        return None

    def replace_regexp(self, pattern: str, replacement: str) -> None:
        f = FileEntity()
        f.path = self.path
        f.read()
        l_p = re.compile(pattern)
        new_content = []
        for line in f.content:
            l_m = l_p.match(line)
            if l_m is not None:
                new_content.append(replacement)
            else:
                new_content.append(line)
        f.content = new_content
        f.write()
        return None

    def content_replace(self, pattern: str, replacement: str) -> None:
        self.content = list(map(
            lambda line:
            line.replace(pattern, replacement),
            self.content
        ))
        return None

    def content_replace_regexp(self, pattern_file_path: str) -> None:
        patterns = FileEntity()
        patterns.path = pattern_file_path
        patterns.read()
        pattern_from = len(self.regexp_replace_file_pattern_indicator)
        for item in patterns.content:
            pattern_to = item.find(self.regexp_replace_file_replacement_indicator)
            replacement_from = \
                item.find(self.regexp_replace_file_replacement_indicator) + \
                len(self.regexp_replace_file_replacement_indicator)
            pattern = item[pattern_from:pattern_to]
            replacement = item[replacement_from:]
            self.replace_regexp(pattern, replacement)
        return None


class ConfEditor:

    def __init__(self):
        self.f_nginx_sites_available_path = '/etc/nginx/sites-available/PROJECT_NAME_nginx.conf'
        self.f_nginx_sites_available = [
            'upstream django {',
            '  server unix:///PROJECT_NAME/PROJECT_NAME.sock;',
            '}',
            'server {',
            '  listen 8000;',
            '  server_name example.com;',
            '  charset utf-8;',
            '  client_max_body_size 75M;',
            '  location /media {',
            '    alias /PROJECT_NAME/media;',
            '  }',
            '  location /static {',
            '    alias /PROJECT_NAME/static;',
            '  }',
            '  location / {',
            '    uwsgi_pass django;',
            '    include /PROJECT_NAME/uwsgi_params;',
            '  }',
            '}',
        ]
        self.f_nginx_conf_path = '/etc/nginx/conf.d/default.conf'
        self.f_nginx_conf_target_pattern = '^}'
        self.f_nginx_conf_append = '    include /etc/nginx/sites-enabled/*;'

    def edit_nginx_sites_available(self) -> None:
        fe = FileEntity()
        fe.path = self.f_nginx_sites_available_path
        fe.content = self.f_nginx_sites_available
        fe.write()
        return None

    def edit_nginx_conf(self) -> None:
        fe = FileEntity()
        fe.path = self.f_nginx_conf_path
        fe.read()
        p = re.compile(self.f_nginx_conf_target_pattern)
        new_content = []
        for line in fe.content:
            m = p.match(line)
            if m is not None:
                new_content.append(self.f_nginx_conf_append)
            new_content.append(line)
        fe.content = new_content
        fe.write()
        return None

    def run(self) -> None:
        self.edit_nginx_sites_available()
        self.edit_nginx_conf()
        return None


class SettingsPyEditor:

    def __init__(self):
        self.f_from_pattern = '^( *)from'
        self.f_import_pattern = '^( *)import'
        self.f_import_append = 'import os'
        self.f_allowed_hosts_pattern = '^( *)(ALLOWED_HOSTS *= *\\[)'
        self.f_static_url_pattern = '^( *)STATIC_URL *= *'
        self.f_settings_py_path = '/PROJECT_NAME/PROJECT_NAME/settings.py'

    def insert_import_os(self, prev_content: list) -> list:
        count = len(prev_content)
        new_content = []
        p_from = re.compile(self.f_from_pattern)
        p_import = re.compile(self.f_import_pattern)
        i = 0
        for i in range(count):
            m_from = p_from.match(prev_content[i])
            m_import = p_import.match(prev_content[i])
            if m_from is not None:
                new_content.append(m_from.group(1) + self.f_import_append)
                new_content.append(prev_content[i])
                break
            if m_import is not None:
                new_content.append(m_import.group(1) + self.f_import_append)
                new_content.append(prev_content[i])
                break
            new_content.append(prev_content[i])
        for j in range(i + 1, count):
            new_content.append(prev_content[j])
        return new_content

    def insert_host_ip(self, prev_content) -> list:
        new_content = []
        p = re.compile(self.f_allowed_hosts_pattern)
        for line in prev_content:
            m = p.match(line)
            if m is not None:
                new_content.append(m.group(1) + m.group(2) + '"HOST_IP"]')
            else:
                new_content.append(line)
        return new_content

    def insert_static_root_define(self, prev_content) -> list:
        count = len(prev_content)
        new_content = []
        p = re.compile(self.f_static_url_pattern)
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

    def run(self) -> None:
        fe = FileEntity()
        fe.path = self.f_settings_py_path
        fe.read()
        new_content = fe.content
        new_content = self.insert_import_os(new_content)
        new_content = self.insert_host_ip(new_content)
        new_content = self.insert_static_root_define(new_content)
        fe.content = new_content
        fe.write()
        return None


if __name__ == '__main__':
    subprocess.call(['django-admin.py', 'startproject', 'PROJECT_NAME'])
    subprocess.call(['mkdir', '/etc/nginx/sites-available/'])
    subprocess.call(['mkdir', '/etc/nginx/sites-enabled/'])
    subprocess.call(['mkdir', '/PROJECT_NAME/media/'])
    subprocess.call(['mkdir', '/PROJECT_NAME/static'])
    ConfEditor().run()
    SettingsPyEditor().run()
    subprocess.call(['cp', '/etc/nginx/uwsgi_params', '/PROJECT_NAME/'])
    subprocess.call(['ln', '-s', '/etc/nginx/sites-available/PROJECT_NAME_nginx.conf', '/etc/nginx/sites-enabled/'])
    os.chdir('/PROJECT_NAME/')
    subprocess.call(['python3', 'manage.py', 'collectstatic'])
    subprocess.call(['systemctl', 'restart', 'nginx'])
