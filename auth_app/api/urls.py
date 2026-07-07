from django.urls import path

from .views import RegistrationView, EmailLoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', EmailLoginView.as_view(), name='login'),
]