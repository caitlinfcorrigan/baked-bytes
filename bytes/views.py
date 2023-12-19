from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import User, Profile, Byte, Order, Order_Detail
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.forms import modelformset_factory
from .forms import OrderQuantityForm, CheckoutForm
import os
# from flask import Flask, jsonify, redirect, request
from django.http import JsonResponse
import stripe
from django.views import View

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

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
       cart_item = Order_Detail.objects.get(order=cart.id, byte=byte, quantity = 1)
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
  items = Order_Detail.objects.select_related('byte').filter(order_id=order_id)
  items = items.annotate(subtotal=F('byte__price')*F('quantity'))
  total = items.aggregate(Sum('subtotal'))
  return render(request, 'order_detail.html', {'items': items, 'total': total})

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

# Stripe API
def create_checkout_session(request):
  try:
    session = stripe.checkout.Session.create(
      ui_mode = 'embedded',
        line_items=[
          {
              # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
              'price': '{{PRICE_ID}}',
              'quantity': 1,
          },
        ],
      mode='payment',
      return_url='/orders.html?session_id={CHECKOUT_SESSION_ID}',
    )
  except Exception as e:
        print('exception :( )')
        return str(e)
  return JsonResponse(clientSecret=session.client_secret)

def session_status(request):
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
  return JsonResponse(status=session.status, customer_email=session.customer_details.email)

# CLASS-BASED VIEWS


# class ItemUpdate(LoginRequiredMixin, UpdateView):
#   model = Order_Detail
#   fields = ['quantity']

# class ByteDetail(DetailView):
#   model = Byte   

class CreateStripeCheckoutSessionView(View):
  """
  Create a checkout session and redirect the user to Stripe's checkout page
  """
  def post(self, request, *args, **kwargs):
    order = Order_Detail.objects.get(id=23)
    product = Order_Detail.objects.select_related('byte').filter(order_id=order.id)
    print(product[0].byte.price)
    checkout_session = stripe.checkout.Session.create(
      payment_method_types=["card"],
      line_items=[
        {
          # "currency": "usd",
          "price": product[0].byte.price,
          # "name": product[0].byte.item,
          "description": product[0].byte.description,
          # Revisit to dynamically charge according to order
          "quantity": product[0].byte.id
        }
      ],
      metadata={"product_id": product[0].byte.id},
      mode="payment",
      success_url='orders',
      cancel_url='cart',
    )
    return redirect(checkout_session.url)