from django.db import models

# Create your models here.

class user_detail(models.Model):
    role_choices = (
        ("admin", "Admin"),
        ("dept_head", "Department head"),
        ("staff", "Staff"),
    )
    department_choices = (
        ("admin", "Admin"),
        ("kitchen", "Kitchen"),
        ("goshala", "Goshala")
    )
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    phno = models.CharField(max_length=12)
    role = models.CharField(max_length=20, choices=role_choices, default="staff")
    department = models.CharField(max_length=100, choices=department_choices, default="kitchen")

    class Meta:
        db_table = "User Detail"