import re

from django import forms
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Mật khẩu"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    error_messages = {
        'invalid_login': _(
            "Tài khoản hoặc mật khẩu không đúng."
        ),
        'inactive': _("Tài khoản chưa được kích hoạt."),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"


class AuthUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Mật khẩu"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Xác nhận mật khẩu"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match("^(0)(\d{9,10})$", phone):
            raise forms.ValidationError('Số điện thoại không hợp lệ.')
        return phone

    def clean_phone_code(self):
        phone_code = self.cleaned_data.get('phone_code')
        if not re.match("^\+\d{,4}$", phone_code):
            raise forms.ValidationError('Mã vùng không hợp lệ (ex:+81,+84,...)')
        return phone_code

    class Meta:
        model = User
        fields = (
            'username', 'password1', 'password2', 'phone_code', 'phone', 'first_name', 'last_name', 'company_name',
            'email')
        widgets = {
            'email': forms.EmailInput(attrs={'required': True, }),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'phone_code': forms.TextInput(attrs={'value': '+'}),
            'phone': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AuthUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"
