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


class BasePyEditor:

    def __init__(self):
        self.BASE_PY_PATH = '/PROJECT_NAME/PROJECT_NAME/settings/base.py'
        self.INSTALLED_APPS_START_PATTERN = '^ *INSTALLED_APPS = \\['
        self.INSTALLED_APPS_END_PATTERN = '^ *]'
        self.INSTALLED_APPS_INSERT = [
            '',
            '    \'wagtail.contrib.sitemaps\',',
            '    \'wagtail.contrib.routable_page\',',
            ']',
        ]
        self.AUTH_PASSWORD_VALIDATORS_START_PATTERN = '^ *AUTH_PASSWORD_VALIDATORS = \\['
        self.AUTH_PASSWORD_VALIDATORS_END_PATTERN = '^ *]'
        self.ALLOWED_HOST_INSERT = [
            ']',
            '',
            '# Hosts/domain names that are valid for this site; required if DEBUG is False',
            '# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts',
            'ALLOWED_HOSTS = ["HOST_IP"]',
        ]

    def find_installed_apps_start(self, prev_content: list) -> int:
        count = len(prev_content)
        p = re.compile(self.INSTALLED_APPS_START_PATTERN)
        i = 0
        for i in range(count):
            m = p.match(prev_content[i])
            if m is not None:
                break
        return i

    def find_installed_apps_end(self, prev_content: list, i: int) -> int:
        count = len(prev_content)
        p = re.compile(self.INSTALLED_APPS_END_PATTERN)
        j = 0
        for j in range(i + 1, count):
            m = p.match(prev_content[j])
            if m is not None:
                break
        return j - 1

    def insert_installed_apps(self, prev_content: list) -> list:
        count = len(prev_content)
        new_content = []
        pos = self.find_installed_apps_end(prev_content, self.find_installed_apps_start(prev_content))
        for i in range(pos):
            new_content.append(prev_content[i])
        new_content.extend(self.INSTALLED_APPS_INSERT)
        for j in range(pos + 2, count):
            new_content.append(prev_content[j])
        return new_content

    def find_auth_password_validators_start(self, prev_content: list) -> int:
        count = len(prev_content)
        p = re.compile(self.AUTH_PASSWORD_VALIDATORS_START_PATTERN)
        i = 0
        for i in range(count):
            m = p.match(prev_content[i])
            if m is not None:
                break
        return i

    def find_auth_password_validators_end(self, prev_content: list, i: int) -> int:
        count = len(prev_content)
        p = re.compile(self.AUTH_PASSWORD_VALIDATORS_END_PATTERN)
        j = 0
        for j in range(i + 1, count):
            m = p.match(prev_content[j])
            if m is not None:
                break
        return j

    def insert_allowed_host(self, prev_content: list) -> list:
        count = len(prev_content)
        new_content = []
        pos = self.find_auth_password_validators_end(
            prev_content,
            self.find_auth_password_validators_start(prev_content)
        )
        for i in range(pos):
            new_content.append(prev_content[i])
        new_content.extend(self.ALLOWED_HOST_INSERT)
        for j in range(pos + 1, count):
            new_content.append(prev_content[j])
        return new_content

    def run(self) -> None:
        fe = FileEntity()
        fe.path = self.BASE_PY_PATH
        fe.read()
        new_content = fe.content
        new_content = self.insert_installed_apps(new_content)
        new_content = self.insert_allowed_host(new_content)
        fe.content = new_content
        fe.write()
        return None


if __name__ == '__main__':
    subprocess.run(['pip3', 'install', 'wagtail'])
    subprocess.run(['wagtail', 'start', 'PROJECT_NAME'])
    subprocess.run(['mkdir', '/PROJECT_NAME/media'])
    subprocess.run(['mkdir', '/PROJECT_NAME/static'])
    ConfEditor().run()
    BasePyEditor().run()
    subprocess.run(['pip3', 'install', '-r', '/PROJECT_NAME/requirements.txt'])
    subprocess.run(['python3', '/PROJECT_NAME/manage.py', 'migrate'])
    subprocess.run(['cp', '/etc/nginx/uwsgi_params', '/PROJECT_NAME/'])
    os.chdir('/PROJECT_NAME/')
    subprocess.run(['python3', 'manage.py', 'collectstatic'])
