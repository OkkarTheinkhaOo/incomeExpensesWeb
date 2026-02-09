import pdb
from urllib import request
from django.shortcuts import render
#for reading json file
import os
import json
from django.conf import settings
#for saving user preferences
from .models import UserPreference
from django.contrib import messages
# Create your views here.

def index(request):
    currencyData = []
    filePath = os.path.join(settings.BASE_DIR, 'currencies.json')
    
    with open(filePath, 'r') as f:
        data = json.load(f)
        for k, v in data.items():
            currencyData.append({'name': k, 'value': v})

    if request.method == 'POST':
        currency = request.POST.get('currency')
        preference, created = UserPreference.objects.get_or_create(user=request.user, defaults={'currency': currency})    
        context = {
        'currencies': currencyData,
        'preference': preference
        }
        if not currency:
            messages.error(request, 'Please select a currency')
            return render(request, 'preferences/index.html', context)
        
        
        if not created:
            preference.currency = currency
            preference.save()
            messages.success(request, 'Preferences updated successfully')
        else:
            messages.success(request, 'Preferences saved successfully')
    return render(request, 'preferences/index.html', context)
        


    
    

