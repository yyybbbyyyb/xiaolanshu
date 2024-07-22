"""
Django settings for xiaolanshu project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os.path
from pathlib import Path
import pymysql
import yaml

# 解决force_text被弃用而图床上传图片失败的问题
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['django_secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 自定义应用
    'application.user',
    'application.cafeteria',
    'application.post',

    'application.testapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xiaolanshu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'xiaolanshu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': config['database']['engine'],
        'NAME': config['database']['name'],
        'USER': config['database']['user'],
        'PASSWORD': config['database']['password'],
        'HOST': config['database']['host'],
        'PORT': config['database']['port'],
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# set aliyun oss
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = 'django_oss_storage.backends.OssMediaStorage'

OSS_ACCESS_KEY_ID = config['oss']['oss_access_key_id']
OSS_ACCESS_KEY_SECRET = config['oss']['oss_access_key_secret']
OSS_ENDPOINT = config['oss']['oss_end_point']
OSS_PREFIX_URL = config['oss']['oss_prefix_url']
OSS_BUCKET_NAME = config['oss']['oss_bucket_name']
OSS_BUCKET_ACL_TYPE = config['oss']['oss_bucket_alc_type']  # private, public-read, public-read-write

OSS_MEDIA_URL = OSS_PREFIX_URL + OSS_BUCKET_NAME + '.' + OSS_ENDPOINT + '/' + MEDIA_URL

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'
