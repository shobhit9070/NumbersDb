from django.shortcuts import render
from django.contrib.auth import logout
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
import pandas as pd
import openpyxl
from io import BytesIO


##########GLOBAL VARS#########

role_choices = {
    "Admin": "admin",
    "Department head": "dept_head",
    "Staff" : "staff"
}

##########GLOBAL VARS END##########


##########HELPER FUNCTIONS START#################
def validate_data_point(data):
    #If not valid return False,"error message"
    return True,"no error"


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
        return HttpResponseRedirect('/oauth/login/google-oauth2/?next=/contact_list')

def upload_bulk_contacts(request):
    if request.method != "POST" or not "fileInput" in request.FILES:
        data = {
            "status":0
        }
    else:
        wb = openpyxl.load_workbook(request.FILES["fileInput"])
        print(wb.sheetnames)
        error_list = []
        success_list = []
        for sheet in wb.sheetnames:
            worksheet = wb[sheet]
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                print(row_data)
                is_valid, reason = validate_data_point(row_data)
                if not is_valid:
                    error_list.append((row_data,reason))
                    continue
                elif user_detail.objects.filter(phno = row_data[1].split('.')[0]).exists():
                    error_list.append((row_data,"entry with same phno exists"))
                else:
                    new_user_detail = user_detail(name=row_data[0],phno=row_data[1].split('.')[0],email=row_data[2])
                    print("dept ",row_data[3].lower().strip())
                    new_user_detail.department = departments.objects.get(name=row_data[3].lower().strip())
                    new_user_detail.role =  role_choices[row_data[4]]
                    new_user_detail.save()
                    success_list.append((row_data,"Success"))
        data = {
            "status":1,
            "error_list":error_list,
            "success_list":success_list
        }
        print(data)
    return render(request, 'contacts_upload_status.html', context=data)


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect("/")