
from decouple import config
import pymysql

pymysql.install_as_MySQLdb()






import os  # Make sure to import the os module

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Library',
        'USER': 'root',
        'PASSWORD': '1812',
        'HOST': 'localhost',  
        'PORT': '3306',
    }
}
