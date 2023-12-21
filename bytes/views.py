from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import User, Photo, Byte, Order, Order_Detail
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from .forms import OrderQuantityForm, CheckoutForm

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

def bytes_index(request):
    bytes = Byte.objects.all()
    return render(request, 'bytes/index.html', {'bytes': bytes})

def bytes_detail(request, byte_id):
    byte = Byte.objects.get(id = byte_id)
    image = Photo.objects.get(byte_id=byte.id)
    return render(request, 'bytes/detail.html', {'byte': byte, "image": image})

# This needs to be a function view bc it's handling complex queries
@login_required
def cart(request):
    user = User.objects.get(username=request.user)
    cart = Order.objects.filter(user_id=user.id, purchased = False)
    if len(cart) == 0:
      cart = Order(user_id=user.id, purchased = False)
      cart.save()
      total = 0
    else:
      cart = Order.objects.get(user_id=user.id, purchased = False)
      items = Order_Detail.objects.select_related('byte').filter(order_id=cart.id)
      items = items.annotate(subtotal=F('byte__price')*F('quantity'))
      total = items.aggregate(Sum('subtotal'))
      form = OrderQuantityForm()
      buy = CheckoutForm()
    return render(request, 'cart.html', {"cart": cart, "items": items,  "total": total, "form": form, "buy": buy})

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
       cart_item = Order_Detail.objects.get(order=cart.id, byte=byte)
       cart_item.quantity += 1
    cart_item.save()    
    return redirect('cart')

@login_required
def cart_checkout(request):
  user = User.objects.get(username=request.user)
  cart = Order.objects.get(user_id=user.id, purchased = False)
  cart.purchased = True
  cart.save()
  return redirect('orders')

@login_required
def orders(request):
  user = User.objects.get(username=request.user)
  orders = Order.objects.filter(user_id=user.id, purchased = True)
  # Update to calculate total in an accessible manner
  totals = []
  for order in orders:
    detail = Order_Detail.objects.select_related('byte').filter(order_id=order.id)
    detail = detail.annotate(subtotal=F('byte__price')*F('quantity'))
    total = detail.aggregate(Sum('subtotal'))
    totals.append({'order_id': order.id, 'total': total})
  # if len(orders) == 0:
  #   return redirect('cart')
  return render(request, 'orders.html', {"orders": orders, "totals": totals})

@login_required
def order_detail(request, order_id):
  order = Order.objects.get(id=order_id)
  items = Order_Detail.objects.select_related('byte').filter(order_id=order_id)
  items = items.annotate(subtotal=F('byte__price')*F('quantity'))
  total = items.aggregate(Sum('subtotal'))
  return render(request, 'order_detail.html', {'items': items, 'total': total, 'order':order})

@login_required
def item_delete(request, order_detail_id):
  print(request)
  print(order_detail_id)
  item = Order_Detail.objects.get(id=order_detail_id)
  item.delete()
  return redirect('cart')

@login_required
def item_update(request, order_detail_id):
  item = Order_Detail.objects.get(id = order_detail_id)
  # Process POST req
  if request.method == 'POST':
    form = OrderQuantityForm(request.POST)
    print(request.POST['quantity'])
    if form.is_valid():
      item.quantity = request.POST['quantity']
      item.save()
      return redirect('cart')
    else:
      form = OrderQuantityForm()
  return render(request, 'cart.html')
