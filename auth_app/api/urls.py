from django.urls import path

from .views import RegistrationView, EmailLoginView, EmailCheckView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]