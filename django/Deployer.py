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
        self.NGINX_CONF_PATH = '/etc/nginx/conf.d/default.conf'
        self.TARGET_START_PATTERN = '^( *)location'
        self.TARGET_END_PATTERN = '^( *)\\}'
        self.NGINX_CONF_REPLACE = [
            '    charset utf-8;',
            '    location /media {',
            '      alias /PROJECT_NAME/media;',
            '    }',
            '    location /static {',
            '      alias /PROJECT_NAME/static;',
            '    }',
            '    location / {',
            '      uwsgi_pass unix:/PROJECT_NAME/PROJECT_NAME.sock;',
            '      include /PROJECT_NAME/uwsgi_params;',
            '    }',
        ]

    def find_nginx_conf_target_start(self) -> int:
        f = FileEntity()
        f.path = self.NGINX_CONF_PATH
        f.read()
        p = re.compile(self.TARGET_START_PATTERN)
        i = 0
        for i in range(len(f.content)):
            if p.match(f.content[i]) is not None:
                break
        return i

    def find_nginx_conf_target_end(self, i: int) -> int:
        f = FileEntity()
        f.path = self.NGINX_CONF_PATH
        f.read()
        p = re.compile(self.TARGET_END_PATTERN)
        j = 0
        for j in range(i + 1, len(f.content)):
            if p.match(f.content[j]) is not None:
                break
        return j

    def replace_nginx_conf(self) -> None:
        start = self.find_nginx_conf_target_start()
        f = FileEntity()
        f.path = self.NGINX_CONF_PATH
        f.read()
        new_content = []
        for i in range(len(f.content)):
            if start == i:
                new_content.extend(self.NGINX_CONF_REPLACE)
                break
            new_content.append(f.content[i])
        end = self.find_nginx_conf_target_end(start)
        for i in range(end + 1, len(f.content)):
            new_content.append(f.content[i])
        f.content = new_content
        f.write()
        return None

    def run(self) -> None:
        self.replace_nginx_conf()
        return None


class SettingsPyEditor:

    def __init__(self):
        self.FROM_PATTERN = '^( *)from'
        self.IMPORT_PATTERN = '^( *)import'
        self.IMPORT_APPEND = 'import os'
        self.ALLOWED_HOSTS_PATTERN = '^( *)(ALLOWED_HOSTS *= *\\[)'
        self.STATIC_URL_PATTERN = '^( *)STATIC_URL *= *'
        self.SETTINGS_PY_PATH = '/PROJECT_NAME/PROJECT_NAME/settings.py'

    def insert_import_os(self, prev_content: list) -> list:
        count = len(prev_content)
        new_content = []
        p_from = re.compile(self.FROM_PATTERN)
        p_import = re.compile(self.IMPORT_PATTERN)
        i = 0
        for i in range(count):
            m_from = p_from.match(prev_content[i])
            m_import = p_import.match(prev_content[i])
            if m_from is not None:
                new_content.append(m_from.group(1) + self.IMPORT_APPEND)
                new_content.append(prev_content[i])
                break
            if m_import is not None:
                new_content.append(m_import.group(1) + self.IMPORT_APPEND)
                new_content.append(prev_content[i])
                break
            new_content.append(prev_content[i])
        for j in range(i + 1, count):
            new_content.append(prev_content[j])
        return new_content

    def insert_host_ip(self, prev_content) -> list:
        new_content = []
        p = re.compile(self.ALLOWED_HOSTS_PATTERN)
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
        p = re.compile(self.STATIC_URL_PATTERN)
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
        f = FileEntity()
        f.path = self.SETTINGS_PY_PATH
        f.read()
        new_content = f.content
        new_content = self.insert_import_os(new_content)
        new_content = self.insert_host_ip(new_content)
        new_content = self.insert_static_root_define(new_content)
        f.content = new_content
        f.write()
        return None


if __name__ == '__main__':
    subprocess.run(['django-admin.py', 'startproject', 'PROJECT_NAME'])
    subprocess.run(['mkdir', '/PROJECT_NAME/media/'])
    subprocess.run(['mkdir', '/PROJECT_NAME/static'])
    ConfEditor().run()
    SettingsPyEditor().run()
    subprocess.run(['cp', '/etc/nginx/uwsgi_params', '/PROJECT_NAME/'])
    os.chdir('/PROJECT_NAME/')
    subprocess.run(['python3', 'manage.py', 'collectstatic'])
