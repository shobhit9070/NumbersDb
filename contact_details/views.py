from django.shortcuts import render
from django.contrib.auth import logout
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect

# Create your views here.
def homepage(request):
    return render(request, 'home_view.html')

def contact_list(request):
    if request.user.is_authenticated:
        print(request.user.email)
        
        user = user_detail.objects.filter(email=request.user.email).first()
        if user != None:
            if user.role == 'staff':
                user_details = user_detail.objects.filter(email=request.user.email)
            elif user.role == 'dept_head':
                user_details = user_detail.objects.filter( ~Q(role="admin"), department=user.department)
            else:
                user_details = user_detail.objects.all()
            print(user_details.values())
        else:
            user_details = []
        data = {
            'user_details': user_details,
        }
        return render(request, 'contact_list.html', context=data)
    else:
        return HttpResponseRedirect('/accounts/google/login/?next=/contact_list')
