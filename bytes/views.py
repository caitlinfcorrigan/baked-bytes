from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from .models import Price, Product
from django.http import JsonResponse
import os

import stripe

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
      return redirect('product_list')
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

def product_list(request):
  products = Price.objects.select_related('product').all()
  return render(request, 'bytes/product_list.html', {"products": products})

def create_checkout_session(request, price_id):
    try:
      price = Price.objects.get(id=price_id)
      session = stripe.checkout.Session.create(
        ui_mode = 'embedded',
      line_items=[
        {
          #  Creating the Stripe Price object in-line to leverage Django data models
          "price_data": {
            "currency": "usd",
            "unit_amount": int(price.price) * 100,
            "product_data": {
              "name": price.product.name,
              "description": price.product.desc,
            },
          },
          "quantity": price.product.quantity,
        }
      ],
            mode='payment',
            return_url=os.environ['PAYMENT_SUCCESS_URL'],
        )
    except Exception as e:
        return str(e)

    return JsonResponse(clientSecret=session.client_secret)

# Class-based Views

class ProductDetailView(DetailView):
  model = Product
  context_object_name = "product"
  template_name = "bytes/product_detail.html"

  def get_context_data(self, **kwargs):
    context = super(ProductDetailView, self).get_context_data()
    context["prices"] = Price.objects.filter(product=self.get_object())
    return context

#   Create a checkout session and redirect the user to Stripe's checkout page
# class CreateStripeCheckoutSessionView(View):
#   def post(self, request, *args, **kwargs):
#     price = Price.objects.get(id=self.kwargs["pk"])
#     checkout_session = stripe.checkout.Session.create(
#       payment_method_types=["card"],
#       line_items=[
#         {
#           #  Creating the Stripe Price object in-line to leverage Django data models
#           "price_data": {
#             "currency": "usd",
#             "unit_amount": int(price.price) * 100,
#             "product_data": {
#               "name": price.product.name,
#               "description": price.product.desc,
#             },
#           },
#           "quantity": price.product.quantity,
#         }
#       ],
#       metadata={"product_id": price.product.id},
#       mode="payment",
#       success_url=os.environ['PAYMENT_SUCCESS_URL'],
#       cancel_url=os.environ['PAYMENT_CANCEL_URL'],
#     )
#     return redirect(checkout_session.url)
  

class SuccessView(TemplateView):
  template_name = "bytes/success.html"

class CancelView(TemplateView):
  template_name = "bytes/cancel.html"