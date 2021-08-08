from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserCustom(AbstractUser):
    username = models.CharField(_('Tài khoản'),max_length=100, primary_key=True)
    company_name = models.CharField(_('Tên công ty'),max_length=150, null=True, blank=True)
    first_name = models.CharField(_('Họ'), max_length=150, blank=True)
    last_name = models.CharField(_('Tên'), max_length=150, blank=True)
    phone_code = models.CharField(_("Mã điện thoại"), max_length=5, null=True)
    phone = models.CharField(_('Số điện thoại'), max_length=11, null=True)
