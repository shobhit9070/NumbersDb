from django.db import models

# Create your models here.

class trust(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class location(models.Model):
    name = models.CharField(max_length=100)
    trust = models.ForeignKey(trust, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class department(models.Model):
    name = models.CharField(max_length=100)
    trust = models.ForeignKey(trust, null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(location, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name

class relation_table(models.Model):
    relations = (
        ("all", "All"),
        ("dept_trust", "Departments under a trust"),
        ("dept_staff", "Departmental staff"),
        ("self", "Self"),
        ("loc_depts", "Departments under a location")
    )
    admin = models.CharField(max_length=20, choices=relations, default="all")
    trustee = models.CharField(max_length=20, choices=relations, default="dept_trust")
    dept_head = models.CharField(max_length=20, choices=relations, default="dept_staff")
    staff = models.CharField(max_length=20, choices=relations, default="self")
    location_admin = models.CharField(max_length=20, choices=relations, default="loc_depts")



class user_detail(models.Model):
    role_choices = (
        ("admin", "Admin"),
        ("trustee", "Trustee"),
        ("dept_head", "Head of Department"),
        ("staff", "Staff"),
        ("location_admin", "Location Admin")
    )
    email = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phno = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=20, choices=role_choices, default="staff")
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True )

    location = models.ForeignKey(location, on_delete=models.SET_NULL, null=True )
    def __str__(self):
        return self.name
