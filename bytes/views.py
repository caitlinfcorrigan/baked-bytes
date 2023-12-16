from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import User, Profile, Byte, Order, Order_Detail
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, Sum

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

# Refactor as ListView (CBV) - need to move & rename html file
def bytes_index(request):
    bytes = Byte.objects.all()
    return render(request, 'bytes/index.html', {'bytes': bytes})

# Refactor as ListView (CBV) - need to move & rename html file
def bytes_detail(request, byte_id):
    byte = Byte.objects.get(id=byte_id)
    return render(request, 'bytes/detail.html', {'byte': byte})

# This needs to be a function view bc it's handling complex queries
@login_required
def cart(request):
    user = User.objects.get(username=request.user)
    cart = Order.objects.get(user_id=user.id, purchased = False)
    items = Order_Detail.objects.select_related('byte').filter(order_id=cart.id)
    # queryset = queryset.annotate(
    #          _price=Sum(
    #          ExpressionWrapper(
    #               F('mealingredient__amount') * 
    #               F('mealingredient__ingredient__unit_price'),
    #               output_field=DecimalField()
    #          )
    #     )
    # )
    items = items.annotate(subtotal=F('byte__price')*F('quantity'))
    total = items.aggregate(Sum('subtotal'))
    print(list(items))
    return render(request, 'cart.html', {"items": items,  "total": total})

@login_required
def cart_add(request, byte_id):
    user = User.objects.get(username=request.user)
    byte = Byte.objects.get(id = byte_id)
    # Check if user has a cart
    cart = Order.objects.filter(user_id=user.id, purchased = False)
    if len(cart) == 0:
      cart = Order(user_id=user.id)
      cart.save()
    else:
       cart = Order.objects.get(user_id=user.id, purchased = False)
    # Check cart for item; if there, increment
    cart_item = Order_Detail.objects.filter(byte=byte, order=cart.id)
    if len(cart_item) == 0:
      cart_item =  Order_Detail(order=cart, byte=byte, quantity = 1)
    else:
       cart_item = Order_Detail.objects.get(order=cart.id, byte=byte, quantity = 1)
       cart_item.quantity += 1
    cart_item.save()    
    return redirect('cart')

# CLASS-BASED VIEWS


