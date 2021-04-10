import os
import subprocess
import sys

import FileEntity

WORKING_DIRECTORY = '/home/y/PycharmProjects/Wagtail-deploy/'
DOCKER_FILE_DIR = 'django-required-package/'
IMAGE_NAME = 'yuhichyoc/django-required-package'
HOST_IP = '192.168.74.130'
CONTAINER_NAME = 'wagtail'
PORT_NUMBER = '8002'
PROJECT_NAME = 'myblog'


def print_captured_stdout(arg: list) -> None:
    for item in arg:
        print(item)
    return None


class ContainerController:

    def __init__(self):
        self.f_working_directory: str = ''
        self.f_image_name: str = ''
        self.f_host_ip: str = ''
        self.f_container_name: str = ''
        self.f_port_number: str = ''
        self.f_project_name: str = ''
        self.NGINX_START: str = "/etc/init.d/nginx start"
        self.START: str = "cd /{0}/ && uwsgi --socket {0}.sock --module {0}.wsgi --chmod-socket=666"

    @property
    def working_directory(self) -> str:
        return self.f_working_directory

    @property
    def image_name(self) -> str:
        return self.f_image_name

    @property
    def host_ip(self) -> str:
        return self.f_host_ip

    @property
    def container_name(self) -> str:
        return self.f_container_name

    @property
    def port_number(self) -> str:
        return self.f_port_number

    @property
    def project_name(self) -> str:
        return self.f_project_name

    @working_directory.setter
    def working_directory(self, arg: str):
        self.f_working_directory = arg

    @image_name.setter
    def image_name(self, arg: str):
        self.f_image_name = arg

    @host_ip.setter
    def host_ip(self, arg: str):
        self.f_host_ip = arg

    @container_name.setter
    def container_name(self, arg: str):
        self.f_container_name = arg

    @port_number.setter
    def port_number(self, arg: str):
        self.f_port_number = arg

    @project_name.setter
    def project_name(self, arg: str):
        self.f_project_name = arg

    @staticmethod
    def list_any(operation: tuple) -> list:
        return list(bytes.decode(subprocess.run(['docker', *operation], capture_output=True).stdout).split('\n'))

    def filter_any(self, operation: tuple, condition: str) -> list:
        return list(filter(lambda item: item.startswith(condition), self.list_any(operation)))

    def build_image(self, docker_file_dir: str) -> None:
        if not os.path.isdir(docker_file_dir):
            return None
        if not os.path.isfile(docker_file_dir + 'Dockerfile'):
            return None
        if 0 < len(self.filter_any(('images',), self.image_name)):
            return None
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'build', '-t', self.image_name, docker_file_dir + '.'
        ], capture_output=True).stdout).split('\n')))
        return None

    def run(self) -> None:
        if 0 == len(self.filter_any(('images',), self.image_name)):
            return None
        if 0 < len(self.filter_any(('ps', '-a', '--format', '{{.Names}}'), self.container_name)):
            return None
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'run', '--name', self.container_name,
            '-p', self.port_number + ':80',
            '-d', '-i', '-t', self.image_name, '/bin/bash',
        ], capture_output=True).stdout).split('\n')))
        f = FileEntity.FileEntity()
        f.path = self.working_directory + 'Deployer.py'
        f.read()
        f.content_replace('PROJECT_NAME', self.project_name)
        f.content_replace('HOST_IP', self.host_ip)
        f.path = self.working_directory + 'Deployer.mod.py'
        f.write()
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'cp', self.working_directory + 'Deployer.mod.py', self.container_name + ':/'
        ], capture_output=True).stdout).split('\n')))
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'exec', self.container_name, '/bin/bash', '-c', 'python3 Deployer.mod.py'
        ], capture_output=True).stdout).split('\n')))
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'stop', self.container_name
        ], capture_output=True).stdout).split('\n')))
        return None

    def start(self) -> None:
        if 0 == len(self.filter_any(('ps', '-a', '--format', '{{.Names}}'), self.container_name)):
            return None
        if 0 < len(self.filter_any(('ps', '--format', '{{.Names}}'), self.container_name)):
            return None
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'start', self.container_name
        ], capture_output=True).stdout).split('\n')))
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'exec', '-d', self.container_name, '/bin/bash', '-c', self.NGINX_START
        ], capture_output=True).stdout).split('\n')))
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'exec', '-d', self.container_name, '/bin/bash', '-c', self.START.format(self.project_name)
        ], capture_output=True).stdout).split('\n')))
        return None

    def stop(self) -> None:
        if 0 == len(self.filter_any(('ps', '-a', '--format', '{{.Names}}'), self.container_name)):
            return None
        if 0 == len(self.filter_any(('ps', '--format', '{{.Names}}'), self.container_name)):
            return None
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'stop', self.container_name
        ], capture_output=True).stdout).split('\n')))
        return None

    def restart(self) -> None:
        if 0 == len(self.filter_any(('ps', '-a', '--format', '{{.Names}}'), self.container_name)):
            return None
        if 0 == len(self.filter_any(('ps', '--format', '{{.Names}}'), self.container_name)):
            return None
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'stop', self.container_name
        ], capture_output=True).stdout).split('\n')))
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'start', self.container_name
        ], capture_output=True).stdout).split('\n')))
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'exec', '-d', self.container_name, '/bin/bash', '-c', self.NGINX_START
        ], capture_output=True).stdout).split('\n')))
        print_captured_stdout(list(bytes.decode(subprocess.run([
            'docker', 'exec', '-d', self.container_name, '/bin/bash', '-c', self.START.format(self.project_name)
        ], capture_output=True).stdout).split('\n')))
        return None


class Runner:

    def __init__(self):
        self.f_shell_arg_action: str = ''
        self.f_shell_arg_container: str = ''
        self.ACTION_NAME_BUILD: str = 'build'
        self.ACTION_NAME_START: str = 'start'
        self.ACTION_NAME_STOP: str = 'stop'
        self.ACTION_NAME_RESTART: str = 'restart'
        self.CONTAINER_NAME_REQUIRED_PACKAGE: str = 'django-required-package'
        self.CONTAINER_SHORTENED_NAME_REQUIRED_PACKAGE: str = 'rq'
        self.CONTAINER_NAME_DJANGO: str = 'django'
        self.CONTAINER_SHORTENED_NAME_DJANGO: str = 'd'
        self.CONTAINER_NAME_WAGTAIL: str = 'wagtail'
        self.CONTAINER_SHORTENED_NAME_WAGTAIL: str = 'w'

    @property
    def shell_arg_action(self) -> str:
        return self.f_shell_arg_action

    @property
    def shell_arg_container(self) -> str:
        return self.f_shell_arg_container

    @shell_arg_action.setter
    def shell_arg_action(self, arg: str):
        self.f_shell_arg_action = arg

    @shell_arg_container.setter
    def shell_arg_container(self, arg: str):
        self.f_shell_arg_container = arg

    def build(self) -> None:
        if self.CONTAINER_NAME_REQUIRED_PACKAGE == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_REQUIRED_PACKAGE == self.f_shell_arg_container:
            c = ContainerController()
            c.image_name = IMAGE_NAME
            c.build_image(DOCKER_FILE_DIR)
        elif self.CONTAINER_NAME_DJANGO == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_DJANGO == self.shell_arg_container:
            d = ContainerController()
            d.working_directory = WORKING_DIRECTORY + 'django/'
            d.image_name = IMAGE_NAME
            d.host_ip = HOST_IP
            d.container_name = CONTAINER_NAME
            d.port_number = PORT_NUMBER
            d.project_name = PROJECT_NAME
            d.run()
        elif self.CONTAINER_NAME_WAGTAIL == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_WAGTAIL == self.shell_arg_container:
            w = ContainerController()
            w.working_directory = WORKING_DIRECTORY + 'wagtail/'
            w.image_name = IMAGE_NAME
            w.host_ip = HOST_IP
            w.container_name = CONTAINER_NAME
            w.port_number = PORT_NUMBER
            w.project_name = PROJECT_NAME
            w.run()
        else:
            pass
        return None

    def start(self) -> None:
        if self.CONTAINER_NAME_DJANGO == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_DJANGO == self.shell_arg_container:
            d = ContainerController()
            d.container_name = CONTAINER_NAME
            d.project_name = PROJECT_NAME
            d.start()
        elif self.CONTAINER_NAME_WAGTAIL == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_WAGTAIL == self.shell_arg_container:
            w = ContainerController()
            w.container_name = CONTAINER_NAME
            w.project_name = PROJECT_NAME
            w.start()
        else:
            pass
        return None

    def stop(self) -> None:
        if self.CONTAINER_NAME_DJANGO == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_DJANGO == self.shell_arg_container:
            d = ContainerController()
            d.container_name = CONTAINER_NAME
            d.stop()
        elif self.CONTAINER_NAME_WAGTAIL == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_WAGTAIL == self.shell_arg_container:
            w = ContainerController()
            w.container_name = CONTAINER_NAME
            w.stop()
        else:
            pass
        return None

    def restart(self) -> None:
        if self.CONTAINER_NAME_DJANGO == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_DJANGO == self.shell_arg_container:
            d = ContainerController()
            d.container_name = CONTAINER_NAME
            d.project_name = PROJECT_NAME
            d.restart()
        elif self.CONTAINER_NAME_WAGTAIL == self.shell_arg_container or \
                self.CONTAINER_SHORTENED_NAME_WAGTAIL == self.shell_arg_container:
            w = ContainerController()
            w.container_name = CONTAINER_NAME
            w.project_name = PROJECT_NAME
            w.restart()
        else:
            pass
        return None

    def run(self) -> None:
        if self.ACTION_NAME_BUILD == self.shell_arg_action:
            self.build()
        elif self.ACTION_NAME_START == self.shell_arg_action:
            self.start()
        elif self.ACTION_NAME_STOP == self.shell_arg_action:
            self.stop()
        elif self.ACTION_NAME_RESTART == self.shell_arg_action:
            self.restart()
        else:
            pass
        return None


if __name__ == '__main__':
    args = sys.argv
    r = Runner()
    r.shell_arg_action = args[1]
    r.shell_arg_container = args[2]
    r.run()
