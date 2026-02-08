from .views import *
from django.urls import path
# To test CSRF exemption
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', Registration.as_view(), name='register'),
    path('login', login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uid>/<token>', verification.as_view(), name='activate'),
    
]