from django.db import models

# Create your models here.

class departments(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

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
    email = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phno = models.CharField(max_length=12)
    role = models.CharField(max_length=20, choices=role_choices, default="staff")
    department = models.ForeignKey(departments, on_delete=models.SET_NULL, null=True )
    
    class Meta:
        db_table = "User Detail"

    def __str__(self):
        return self.name
