# filepath: /Users/phokin/Documents/Infra-track/sak_infratrack/app/views.py
from django.shortcuts import render
from .models import BranchInfo

def dashboard(request):
    branch_list = BranchInfo.objects.all()
    return render(request, 'dashboard.html', {'branch_list': branch_list})