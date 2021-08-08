from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user import forms


class UserRegisterView(CreateView):
    template_name = 'user/register.html' # render template
    form_class = forms.AuthUserCreationForm # khai báo form
    success_url = reverse_lazy('user:login') # success redirect link

    def form_valid(self, form):
        """
        Sau khi đăng ký thành công thì đăng nhập luôn (tránh tình trạng bug)
        :param form:
        :return: data
        """
        data = super(UserRegisterView, self).form_valid(form)
        login(self.request, self.object)
        return data


class UserLoginView(LoginView):
    template_name = 'user/login.html' # render template
    form_class = forms.LoginForm # khai báo form
    redirect_authenticated_user = True # đang login sẽ không vào được trang đăng nhập


