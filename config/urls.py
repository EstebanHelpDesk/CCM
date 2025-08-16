from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from avisos.views import SignupView, HomeView
from avisos.views import logout_then_login
from avisos.forms import BootstrapAuthenticationForm

urlpatterns = [
    path("interno/", admin.site.urls),
    path("a/login/", auth_views.LoginView.as_view(template_name="auth/login.html",authentication_form=BootstrapAuthenticationForm), name="login"),
    path("a/logout/", logout_then_login, name="logout"),
    path("a/signup/", SignupView.as_view(), name="signup"),
    path("", HomeView.as_view(), name="home"),
    path("", include("avisos.urls")),
]
