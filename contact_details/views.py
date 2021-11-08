from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.
def homepage(request):
    return render(request, 'home_view.html')
