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

class SettingsPyAppender:

  def setProjectName(self, arg):
    self.projectName = arg

  def setHostIP(self, arg):
    self.hostIP = arg

  def insertImportStatement(self, prevContent):
    count = len(prevContent)
    newContent = []
    pFrom = re.compile('^( *)from')
    pImport = re.compile('^( *)import')
    for i in range(count):
      mFrom = pFrom.match(prevContent[i])
      mImport = pImport.match(prevContent[i])
      if mFrom is not None:
        newContent.append(mFrom.group(1) + 'import os')
        newContent.append(prevContent[i])
        break
      if mImport is not None:
        newContent.append(mImport.group(1) + 'import os')
        newContent.append(prevContent[i])
        break
      newContent.append(prevContent[i])
    for j in range(i + 1, count):
      newContent.append(prevContent[j])
    return newContent

  def insertHostIP(self, prevContent):
    newContent = []
    p = re.compile('^( *)(ALLOWED_HOSTS *= *\[)')
    for l in prevContent:
      m = p.match(l)
      if m is not None:
        newContent.append(m.group(1) + m.group(2) + '"' + self.hostIP + '"]')
      else:
        newContent.append(l)
    return newContent

  def insertStaticRootDefine(self, prevContent):
    count = len(prevContent)
    newContent = []
    p = re.compile('^( *)STATIC_URL *= *')
    for i in range(count):
      newContent.append(prevContent[i])
      m = p.match(prevContent[i])
      if m is not None:
        newContent.append(m.group(1) + 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")')
        break
    for j in range(i + 1, count):
      newContent.append(prevContent[j])
    return newContent

  def run(self):
    fe = FileEntity()
    fe.setPath('/' + self.projectName + '/' + self.projectName + '/settings.py')
    fe.read()
    newContent = self.insertStaticRootDefine(self.insertHostIP(self.insertImportStatement(fe.getContent())))
    fe.setContent(newContent)
    fe.write()

if __name__ == '__main__':
  pncw = ProjectNginxConfWriter()
  pncw.setProjectName(PROJECT_NAME)
  pncw.run()
  nca = NginxConfAppender()
  nca.run()
  spa = SettingsPyAppender()
  spa.setProjectName(PROJECT_NAME)
  spa.setHostIP(HOST_IP)
  spa.run()
