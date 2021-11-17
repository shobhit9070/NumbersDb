from django.shortcuts import render
from django.contrib.auth import logout
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
import pandas as pd
import openpyxl
from io import BytesIO
import re

##########GLOBAL VARS#########

role_choices = {
    "admin": "admin",
    "department head": "dept_head",
    "staff" : "staff",
    "trustee": "trustee",
}

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
##########GLOBAL VARS END##########


##########HELPER FUNCTIONS START#################
def validate_data_point(data):
    #If not valid return False,"error message"

    if str(data[1])[-10:].isnumeric() != True:
        print("return")
        return False, "Invalid phone number"
    # if not re.fullmatch(email_regex, data[2]):
    #     return False, "Invalid email address"
    if not data[3].lower().strip() in role_choices:
        return False, "Invalid role - '" + data[3] + "'. Valid options are " + str(list(role_choices.keys()))
    new_trust = None
    if len(data) == 6 and not trust.objects.filter(name=data[5].lower().strip()).exists():
        new_trust = trust(name=data[5].lower().strip())
        new_trust.save()
    
    if not department.objects.filter(name=data[4].lower().strip()).exists():
        new_dept = department(name=data[4].lower().strip(), trust=new_trust)
        new_dept.save()
    return True,"no error"

def sanitize_phno(phno):
    return str(phno)[-10:]

#############HELPER FUNCTIONS END###################



# Create your views here.

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
        all_depts = department.objects.all()
        data = {
            'user_details': user_details,
            'curr_user': user,
            'all_depts': all_depts,
        }
        return render(request, 'contact_list.html', context=data)
    else:
        return HttpResponseRedirect('/oauth/login/google-oauth2/?next=/')

def upload_bulk_contacts(request):
    if request.user.is_authenticated:
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
                    print(str(row[0].row))
                    row_data = list()
                    for cell in row:
                        row_data.append(str(cell.value))
                    print(row_data)
                    is_valid, reason = validate_data_point(row_data)
                    if not is_valid:
                        error_list.append({'data': row_data, 'status': reason, "row_idx": str(row[0].row)})
                        continue
                    elif user_detail.objects.filter(phno = sanitize_phno(row_data[1].split('.')[0])).exists():
                        error_list.append({'data': row_data, 'status': "Entry with same phone number already exists", "row_idx": str(row[0].row)})
                    else:
                        new_user_detail = user_detail(name=row_data[0],phno=sanitize_phno(row_data[1].split('.')[0]),email=row_data[2])
                        print("dept ",row_data[4].lower().strip())
                        new_user_detail.department = department.objects.get(name=row_data[4].lower().strip())
                        new_user_detail.role =  role_choices[row_data[3].lower().strip()]
                        new_user_detail.save()
                        success_list.append({'data': row_data, 'status': "Successfully added", "row_idx": str(row[0].row)})
            data = {
                "status": 1,
                "error_list": error_list,
                "success_list": success_list
            }
            print(data)
        return render(request, 'contacts_upload_status.html', context=data)
    else:
        return HttpResponseRedirect('/oauth/login/google-oauth2/?next=/')


def auth_logout(request):
    print("logout", request.user.is_authenticated)
    logout(request)
    print("logout", request.user.is_authenticated)

    return HttpResponseRedirect("/")