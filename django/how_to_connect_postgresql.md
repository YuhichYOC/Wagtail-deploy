| No. | 操作 |
| --- | --- |
| 1. | apt install python3-psycopg2 |
| 2. | vim /[project-name]/[project-name]/settings.py |
| 3. | python3 /[project-name]/manage.py migrate |

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': [],
        'USER': [],
        'PASSWORD': [],
        'HOST': [],
        'PORT': [],
    }
}
```
