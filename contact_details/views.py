from django.shortcuts import render
from django.contrib.auth import logout
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect

##########HELPER FUNCTIONS START#################
def validate_data_point(data):

    return True


#############HELPER FUNCTIONS END###################



# Create your views here.
def homepage(request):
    return render(request, 'home_view.html')

def access_relation(user):
    relation_rule = relation_table.objects.all().values()[0]
    print(relation_rule)
    if relation_rule[user.role] == 'self':
        user_details = [user]
    elif relation_rule[user.role] == 'dept_staff':
        user_details = user_detail.objects.filter(~Q(role="admin"), department=user.department)
    elif relation_rule[user.role] == 'dept_trust':
        user_details = user_detail.objects.filter(~Q(role="admin"), department__in=department.objects.filter(trust=user.department.trust))
    elif relation_rule[user.role] == 'all':
        user_details = user_detail.objects.all()
    return user_details

def contact_list(request):
    if request.user.is_authenticated:
        user = user_detail.objects.filter(email=request.user.email).first()
        if user != None:
            relation_rule = relation_table.objects.all().values()[0]
            print(relation_rule)
            if relation_rule[user.role] == 'self':
                user_details = [user]
            elif relation_rule[user.role] == 'dept_staff':
                user_details = user_detail.objects.filter(role='staff', department=user.department)
            elif relation_rule[user.role] == 'dept_trust':
                user_details = user_detail.objects.filter(role__in=['dept_head', 'staff'], department__in=department.objects.filter(trust=user.department.trust))
            elif relation_rule[user.role] == 'all':
                user_details = user_detail.objects.all()
        else:
            user_details = []
        data = {
            'user_details': user_details,
            'role': user.role,
            'dept': user.department.name,
        }
        return render(request, 'contact_list.html', context=data)
    else:
        return HttpResponseRedirect('/accounts/google/login/?next=/contact_list')

def upload_bulk_contacts(request):

    return HttpResponseRedirect("/")


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect("/")