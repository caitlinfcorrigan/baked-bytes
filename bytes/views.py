from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Profile, Byte
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    #  Create a new user
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Add user to db and login
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again.'
  # For a bad POST or GET request, refresh the form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def bytes_index(request):
    bytes = Byte.objects.all()
    return render(request, 'bytes/index.html', {'bytes': bytes})

def bytes_detail(request, byte_id):
    byte = Byte.objects.get(id=byte_id)
    return render(request, 'bytes/detail.html', {'byte': byte})

def cart(request):
    cart = Order.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart': cart})
