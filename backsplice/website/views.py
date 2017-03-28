from django.shortcuts import render

# Create your views here.

def create_paperwork(request):
    return render(request, 'create_paperwork.html')

def home(request):
    return HttpResponse('HOME')

def scouts(request):
    return HttpResponse('SCOUTS')

def instructors(request):
    return HttpResponse('INSTRUCTORS')

def pending_requests(request):
    return HttpResponse('PENDING REQUESTS')

