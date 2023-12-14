from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def bytes_index(request):
    return render(request, 'bytes/index.html')

def bytes_detail(request):
    return render(request, 'bytes/detail.html')