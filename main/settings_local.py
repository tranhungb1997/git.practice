from os import path
from main.settings import BASE_DIR

STATIC_URL = '/static/'
STATICFILES_DIRS = [path.join(BASE_DIR, "statics/")]

# User config
AUTH_USER_MODEL = 'user.UserCustom'
LOGIN_URL = 'user:login'
LOGIN_REDIRECT_URL = "shipment_app:home"
LOGOUT_REDIRECT_URL = "user:login"

# Password validate
AUTH_PASSWORD_VALIDATORS = []

# Config email server
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '' # Email Local
EMAIL_HOST_PASSWORD = '' # app password
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ADMIN_EMAIL = '' # Email gửi Admin