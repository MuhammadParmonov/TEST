from django.urls import path
from .views import login_view, logout_view
# from django.contrib.auth.views import LoginView, LogoutView
        

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # path("login2/", LoginView.as_view(), name="login2"),
    # path("logout2/", LogoutView.as_view(), name="logout2"),
]