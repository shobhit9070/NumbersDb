from django.shortcuts import render

def view_name(request):
    return render(request, 'home_view.html', {})