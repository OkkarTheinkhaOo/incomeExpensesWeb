import token
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
# for showing Messages
from django.contrib import messages
# for email validation
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import *
#for login verification
from django.contrib import auth
# Create your views here.



class Registration(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #Get user data
        username = request.POST['username']
        userEmail = request.POST['email']
        password = request.POST['password']
        
        context = {
            'fieldValues': request.POST
        }
        # Validating user data
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'authentication/register.html', context)
        
        if User.objects.filter(email=userEmail).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'authentication/register.html', context)
        
        if len(password) < 6:
            messages.error(request, 'Password should be at least 6 character')
            return render(request, 'authentication/register.html', context)
            
        # create user account
        user = User.objects.create_user(username=username,email=userEmail)
        user.set_password(password)
        user.is_active=False
        user.save()
        
        #for activation link
        domain=get_current_site(request).domain
        link = reverse('activate', kwargs={
            'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
            'token': token_generator.make_token(user)
        })
        activateUrl = f"{request.scheme}://{domain}{link}"
        # for sending email
        emailSubject = 'Activate your account'
        emailBody = 'Hi ' + user.username + ', Please use this link to verify your account\n' + activateUrl
        
        
        emailMessage = EmailMessage(
            emailSubject,
            emailBody,
            settings.EMAIL_HOST_USER,
            [userEmail],
        )
        emailMessage.send(fail_silently=False)
        messages.success(request, 'Account created successfully. Check your email')
        return redirect('register')

class verification(View):
    def get(self, request, uid, token):
        try:
            id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Invalid activation link')
            return redirect('login')
                        
        if user.is_active:
            messages.info(request, "Account already activated")
            return redirect('login')
        
        if not token_generator.check_token(user, token):
            messages.error(request, 'Invalid or expired token')
            return redirect('login')
        
        user.is_active = True
        user.save()
        
        messages.success(request, 'Account activated successfully')
        return redirect('login')    
        
    
class login(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if not username or not password:
            messages.error(request, 'Please fill all the fields')
            return redirect('login')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User does not exist')
            return redirect('login')
        
        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'Wrong password, try again')
            return render(request, 'authentication/login.html', {'fieldValues': request.POST})
        
        if not user.is_active:
            messages.error(request, 'Account not activated. Please check your email for activation link')
            return redirect('login')
        
        auth.login(request, user)
        return redirect('expenses')
        
                

class UsernameValidationView(View): 
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is already taken'}, status=409)
        return JsonResponse({'username_valid': True})
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is already taken'}, status=409)
        return JsonResponse({'email_valid': True})

class Logout(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')