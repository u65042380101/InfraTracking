# filepath: /Users/phokin/Documents/Infra-track/sak_infratrack/app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import BranchInfo, InternetLink

def dashboard(request):
    branch_list = BranchInfo.objects.all()
    return render(request, 'dashboard.html', {'branch_list': branch_list})

def internet_links_api(request, branch_code):
    links = InternetLink.objects.filter(branch_id=branch_code)
    data = [
        {
            "proivider": link.proivider,
            "fttx": link.fttx,
            "speed": link.speed,
            "start_date": link.start_date,
            "last_service": link.last_service,
            "service_center": link.service_center,
        }
        for link in links
    ]
    return JsonResponse(data, safe=False)