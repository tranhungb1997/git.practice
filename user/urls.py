from django.contrib.auth.views import LogoutView
from django.urls import path
from user import views

app_name = "user"
urlpatterns = [
    path('dang-nhap/', views.UserLoginView.as_view(), name="login"),
    path('dang-ky/', views.UserRegisterView.as_view(), name="register"),
    path('dang-xuat/', LogoutView.as_view(), name="logout"),
]
