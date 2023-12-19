from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from .models import Price, Product
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

# Class-based Views

class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "bytes/product_list.html"

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "bytes/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context["prices"] = Price.objects.filter(product=self.get_object())
        return context


class CreateStripeCheckoutSessionView(View):
  """
  Create a checkout session and redirect the user to Stripe's checkout page
  """

  def post(self, request, *args, **kwargs):
    price = Price.objects.get(id=self.kwargs["pk"])

    checkout_session = stripe.checkout.Session.create(
      payment_method_types=["card"],
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
      metadata={"product_id": price.product.id},
      mode="payment",
      success_url=os.environ['PAYMENT_SUCCESS_URL'],
      cancel_url=os.environ['PAYMENT_CANCEL_URL'],
    )
    return redirect(checkout_session.url)
  

class SuccessView(TemplateView):
  template_name = "bytes/success.html"

class CancelView(TemplateView):
  template_name = "bytes/cancel.html"