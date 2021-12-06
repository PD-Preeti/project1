import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+0@p7rslj*!jsxir*77n=&-(%8sm$20vot!4l#yf+%0rs!alm6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminboard',
    'employee',
    'social_django',
    'simple_mail',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'adminboard.middleware.CustomMiddleware',
#    'adminboard.middleware.MailerMiddleware',
#    'adminboard.middleware.MailerTwoMiddleware',
#    'employee.middleware.CustomMiddleware'
]

ROOT_URLCONF = 'learningMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
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

WSGI_APPLICATION = 'learningMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#   }
#}

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'devanalytics',
         'USER': 'raghav',
         'PASSWORD': 'programming',
         'HOST': 'localhost',
         'PORT': '',
     }
 }




# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
  
USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
 os.path.join(BASE_DIR, 'static')
] #local

#STATIC_ROOT = os.path.join(BASE_DIR, 'static') #server

# enable django-modeltranslation integration
SIMPLE_MAIL_USE_MODELTRANSALTION = False
# enable django-ckeditor integration
SIMPLE_MAIL_USE_CKEDITOR = True
# set default email template
SIMPLE_MAIL_DEFAULT_TEMPLATE = 'adminboard/components/email/template.html'
# enable/disable cssutils warning logs
SIMPLE_MAIL_LOG_CSS_WARNING = False
# storage for logo and banner
SIMPLE_MAIL_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '757845931828-5sb180o0q56ib9q9dkrgccaplh58470q.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'JNxWj19LmcVPP9sliL-mgpTN'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '757845931828-5sb180o0q56ib9q9dkrgccaplh58470q.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'JNxWj19LmcVPP9sliL-mgpTN'


SOCIAL_AUTH__KEY = 'ID'
SOCIAL_AUTH__SECRET = 'SECRET'
LOGIN_REDIRECT_URL = '/adminboard/adminhome/'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'analytics@dataflowgroup.com'
# EMAIL_HOST_PASSWORD = 'Dashboards@123'


# Analytics_ses-smtp-user.20210106-230754
# From ID: analytics@dataflowgroup.com
# SMTP Username: AKIA6MOGWBGBCOV7LHE6
# SMTP Password: BNKjckz6iVpFHFWH1T/1WiuHaDuhuO0/JFgbJp0Gwxuz
# SMTP Server:
# email-smtp.eu-west-1.amazonaws.com
# Port:
# 587

# first try
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'AKIA6MOGWBGBCBL3LFR3'
#EMAIL_HOST_PASSWORD = 'BBighTezVs/o++KjQFieuL7sJO+Xe9CmAk96KhcC2eyv'
#EMAIL_USE_TLS = True


# second try
# DEFAULT_FROM_EMAIL = 'analytics@dataflowgroup.com'

# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# MAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com' 
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'AKIA6MOGWBGBCOV7LHE6'
# EMAIL_HOST_PASSWORD = 'BNKjckz6iVpFHFWH1T/1WiuHaDuhuO0/JFgbJp0Gwxuz'
# EMAIL_USE_TLS = True
