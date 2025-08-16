from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from avisos.views import SignupView, HomeView
from avisos.views import logout_then_login
from avisos.forms import BootstrapAuthenticationForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="auth/login.html",authentication_form=BootstrapAuthenticationForm), name="login"),
    path("accounts/logout/", logout_then_login, name="logout"),
    path("accounts/signup/", SignupView.as_view(), name="signup"),
    path("", HomeView.as_view(), name="home"),
    path("", include("avisos.urls")),
]
