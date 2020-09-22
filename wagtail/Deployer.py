import re

PROJECT_NAME = [project-name]
HOST_IP = [host-ip]

class FileEntity:

  def __init__(self):
    self.content = []

  def setPath(self, arg):
    self.path = arg

  def getContent(self):
    return self.content

  def setContent(self, arg):
    self.content = arg

  def read(self):
    with open(self.path, 'r') as f:
      lines = f.read().split('\n')
      for l in lines:
        self.content.append(l)

  def write(self):
    with open(self.path, 'w') as f:
      for l in self.content:
        f.write(l)
        f.write('\n')

class BasePyAppender:

  def setProjectName(self, arg):
    self.projectName = arg

  def setHostIP(self, arg):
    self.hostIP = arg

  def findInstalledAppsStart(self, prevContent):
    count = len(prevContent)
    p = re.compile('^ *INSTALLED_APPS = \[')
    for i in range(count):
      m = p.match(prevContent[i])
      if m is not None:
        break
    return i

  def findInstalledAppsEnd(self, prevContent, i):
    count = len(prevContent)
    p = re.compile('^ *\]')
    for j in range(i + 1, count):
      m = p.match(prevContent[j])
      if m is not None:
        break
    return j - 1

  def insertInstalledApps(self, prevContent):
    count = len(prevContent)
    newContent = []
    pos = self.findInstalledAppsEnd(prevContent, self.findInstalledAppsStart(prevContent))
    for i in range(pos):
      newContent.append(prevContent[i])
    newContent.append('')
    newContent.append('    \'wagtail.contrib.sitemaps\',')
    newContent.append('    \'wagtail.contrib.routable_page\',')
    newContent.append(']')
    for j in range(pos + 2, count):
      newContent.append(prevContent[j])
    return newContent

  def findAuthPasswordValidatorsStart(self, prevContent):
    count = len(prevContent)
    p = re.compile('^ *AUTH_PASSWORD_VALIDATORS = \[')
    for i in range(count):
      m = p.match(prevContent[i])
      if m is not None:
        break
    return i

  def findAuthPasswordValidatorsEnd(self, prevContent, i):
    count = len(prevContent)
    p = re.compile('^ *\]')
    for j in range(i + 1, count):
      m = p.match(prevContent[j])
      if m is not None:
        break
    return j

  def insertAllowedHost(self, prevContent):
    count = len(prevContent):
    newContent = []
    pos = self.findAuthPasswordValidatorsEnd(prevContent, self.findAuthPasswordValidatorsStart(prevContent))
    for i in range(pos):
      newContent.append(prevContent[i])
    newContent.append('')
    newContent.append('# Hosts/domain names that are valid for this site; required if DEBUG is False')
    newContent.append('# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts')
    newContent.append('ALLOWED_HOSTS = [' + self.hostIP + ']')
    for j in range(pos + 1, count):
      newContent.append(prevContent[j])
    return newContent

  def run(self):
    fe = FileEntity()
    fe.setPath('/' + self.projectName + '/' + self.projectName + '/settings/base.py')
    fe.read()
    newContent = self.insertAllowedHost(self.insertInstalledApps(fe.getContent()))
    fe.setContent(newContent)
    fe.write()

class ProjectNginxConfWriter:

  def setProjectName(self, arg):
    self.projectName = arg

  def run(self):
    content = [
        'upstream django {',
        '  server unix:///' + self.projectName + '/' + self.projectName + '.sock;',
        '}',
        'server {',
        '  listen 8000;',
        '  server_name example.com;',
        '  charset utf-8;',
        '  client_max_body_size 75M;',
        '  location /media {',
        '    alias /' + self.projectName + '/media;',
        '  }',
        '  location /static {',
        '    alias /' + self.projectName + '/static;',
        '  }',
        '  location / {',
        '    uwsgi_pass django;',
        '    include /' + self.projectName + '/uwsgi_params;',
        '  }',
        '}'
    ]
    toPath = '/etc/nginx/sites-available/' + self.projectName + '_nginx.conf'
    fe = FileEntity()
    fe.setPath(toPath)
    fe.setContent(content)
    fe.write()

class NginxConfAppender:

  def run(self):
    fe = FileEntity()
    fe.setPath('/etc/nginx/nginx.conf')
    fe.read()
    content = fe.getContent()
    newContent = []
    p = re.compile('^( *)include +/etc/nginx/conf\.d/\*\.conf;')
    for l in content:
      m = p.match(l)
      if m is not None:
        newContent.append(m.group(1) + 'include /etc/nginx/sites-enabled/*;')
      newContent.append(l)
    fe.setContent(newContent)
    fe.write()

if __name__ == '__main__':
  bpa = BasePyAppender()
  bpa.setProjectName(PROJECT_NAME)
  bpa.setHostIP(HOST_IP)
  bpa.run()
  pncw = ProjectNginxConfWriter()
  pncw.setProjectName(PROJECT_NAME)
  pncw.run()
  nca = NginxConfAppender()
  nca.run()
