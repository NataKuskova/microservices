from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, request, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime
# from django.views.generic.base import View
# from cart.cart import Cart
from django.contrib import admin
import requests
from tea.models import *
from tea.forms import *

DB_URL = 'http://127.0.0.1:8080'


class ProductsList(TemplateView):
    # model = Product
    template_name = 'index.html'
    # context_object_name = 'products'
    # paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        # context['cart'] = Cart(self.request)
        # context['cart'] = ''
        # resp = requests.post(DB_URL + '/api/api-auth/login/',
        #                      {'username': 'admin', 'password': '123456nn'})
        products = requests.get(DB_URL + '/api/products/')
        context['products'] = products.json()
        context['url'] = DB_URL
        return context
    #
    # def get_queryset(self):
    #     queryset = super(ProductsList, self).get_queryset()
    #     search = self.request.GET.get('search', None)
    #     sort = self.request.GET.get('sort', None)
    #     by = self.request.GET.get('by', None)
    #     if search is not None and sort is not None:
    #         return queryset.filter(Q(name__icontains=search) |
    #                                Q(price__icontains=search) |
    #                                Q(quantity__icontains=search)
    #                                ).order_by(by + sort)
    #     if search is not None:
    #         return queryset.filter(Q(name__icontains=search) |
    #                                Q(price__icontains=search) |
    #                                Q(quantity__icontains=search))
    #     if sort is not None:
    #         return queryset.order_by(by + sort)
    #     return queryset


class ProductDetail(View):
    # model = Product
    # pk_url_kwarg = 'id'
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        product = requests.get(DB_URL + '/api/products/' + kwargs['id'])
        context = {'product': product.json()}
        return render(request, self.template_name, context)

    # def get_context_data(self, **kwargs):
    #     context = super(ProductDetail, self).get_context_data(**kwargs)
    #     # context['cart'] = Cart(self.request)
    #     # context['cart'] = ''
    #     return context


class ProductCreate(FormView):
    # model = Product
    template_name = 'add_product.html'
    form_class = CreateProductForm
    # fields = ['name', 'category', 'price', 'quantity', 'photo']
    success_url = reverse_lazy('products_list')

    # def get_context_data(self, **kwargs):
    #     context = super(ProductCreate, self).get_context_data(**kwargs)
    #     # context['cart'] = Cart(self.request)
    #     context['cart'] = ''
    #     return context
    def post(self, request, *args, **kwargs):
        requests.post(DB_URL + '/api/products/', data=request.POST,
                      files=request.FILES)
        return redirect(self.get_success_url())


class ProductDelete(FormView):
    # model = Product
    # pk_url_kwarg = 'id'
    success_url = reverse_lazy('products_list')

    def post(self, request, *args, **kwargs):
        requests.delete(DB_URL + '/api/products/' + kwargs['id'] + '/')
        return redirect(self.get_success_url())


class ProductUpdate(FormView):
    # model = Product
    # pk_url_kwarg = 'id'
    template_name = 'edit_product.html'
    # fields = ['name', 'category', 'price', 'quantity', 'photo']

    def get(self, request, *args, **kwargs):
        product = requests.get(DB_URL + '/api/products/' + kwargs['id'])
        context = {'product': product.json()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        requests.put(DB_URL + '/api/products/' + kwargs['id'] + '/',
                     data=request.POST,
                     files=request.FILES)
        product = requests.get(DB_URL + '/api/products/' + kwargs['id'])
        context = {'product': product.json()}
        return render(request, 'product.html', context)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    # form_class = RegistrForm
    # success_url = reverse_lazy('login')
    template_name = "register.html"

    # def form_valid(self, form):
    #     # self.object = form.save(commit=False)
    #     # self.object.first_name = self.request.POST.get('first_name', None)
    #     # self.object.last_name = self.request.POST.get('last_name', None)
    #     self.object = form.save()
    #     # address = self.request.POST.get('address', None)
    #     # phone = self.request.POST.get('phone', None)
    #     # Buyer.objects.create(address=address,
    #     #                      phone=phone)
    #     return super(RegisterFormView, self).form_valid(form)
    #
    def get_context_data(self, **kwargs):
        context = super(RegisterFormView, self).get_context_data(**kwargs)
        # context['cart'] = Cart(self.request)
        context['cart'] = ''
        return context


class LoginFormView(FormView):
    # form_class = AuthenticationForm
    template_name = "login.html"
    # success_url = reverse_lazy('products_list')
    #
    # def form_valid(self, form):
    #     # self.user = form.get_user()
    #     # login(self.request, self.user)
    #     # return super(LoginFormView, self).form_valid(form)
    #     resp = requests.post(DB_URL + '/api/api-auth/login/',
    #                          {'username': 'admin', 'password': '123456nn'})

    # def get_context_data(self, **kwargs):
    #     context = super(LoginFormView, self).get_context_data(**kwargs)
    #     # context['cart'] = Cart(self.request)
    #     context['cart'] = ''
    #     return context


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("products_list")


class BuyerCreate(FormView):
    template_name = 'edit_user.html'
    # form_class = CreateUserForm
    # success_url = reverse_lazy('products_list')

    # def form_valid(self, form):
    #     self.object = form.save()
    #     return redirect(self.get_success_url())
    #
    def get_context_data(self, **kwargs):
        context = super(BuyerCreate, self).get_context_data(**kwargs)
        # context['cart'] = Cart(self.request)
        context['cart'] = ''
        return context


class CartView(TemplateView):
    template_name = "cart.html"
    # form_class = UpdateCartForm

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        # context['cart'] = Cart(self.request)
        # print(requests.get(DB_URL + '/api/cart/', self.request))
        context['cart'] = ''
        return context


class AddToCart(View):
    def get(self, request, **kwargs):
        if request.is_ajax:
            # cart = Cart(request)
            # try:
            #     product = Product.objects.get(id=kwargs['id'])
            #     quantity = 1
            #     cart.add(product, product.price, quantity)
            #     return HttpResponse(json.dumps({'count': cart.count()}))
            # except:
            #     return HttpResponse(json.dumps({'count': cart.count()}))
            response = requests.post(DB_URL + '/api/cart/',
                                     {'id': kwargs['id'],
                                      'data': request})
            result = response.json()
            # cart_id ???
            # request.session['CART-ID'] = result['cart_id']
            return HttpResponse(result)



class DeleteFromCart(View):
    pass
    # def get(self, request, **kwargs):
    #     product = Product.objects.get(id=kwargs['id'])
    #     cart = Cart(self.request)
    #     cart.remove(product)
    #     return redirect("cart")


class ClearCart(View):
    pass
    # def get(self, request, **kwargs):
    #     cart = Cart(self.request)
    #     cart.clear()
    #     return redirect("cart")


class UpdateCart(TemplateView):
    pass
    # def post(self, request, *args, **kwargs):
    #     cart = Cart(self.request)
    #     for item in cart:
    #         quantity = request.POST.get('q_'+str(item.product.id), None)
    #         if quantity is not None:
    #             cart.update(item.product, quantity, item.product.price)
    #     return redirect("cart")


class OrderView(FormView):

    template_name = 'order.html'
    # form_class = CreateUserForm
    # success_url = reverse_lazy('order')
    #
    # def form_valid(self, form):
    #     self.object = form.save()
    #     cart = Cart(self.request)
    #     date_order = datetime.now()
    #     order = Order.objects.create(user=self.object,
    #                                  date_order=date_order,
    #                                  sum=cart.summary())
    #     for item in cart:
    #         product = get_object_or_404(Product, id=item.product.id)
    #         list_of_order = ListOfOrder.objects.create(order=order,
    #                                                    product=product,
    #                                                    price=item.product.price,
    #                                                    quantity=item.quantity,
    #                                                    sum=item.total_price)
    #         quantity_for_update = product.quantity - item.quantity*50
    #         Product.objects.filter(id=item.product.id).update(quantity=quantity_for_update)
    #     cart.clear()
    #     return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        # cart = Cart(self.request)
        prod = []
        # for item in cart:
        #     product = get_object_or_404(Product, id=item.product.id)
        #     if product.quantity / 50 < item.quantity:
        #        prod.append(product)
        # context['product'] = prod
        # context['cart'] = cart
        context['product'] = ''
        context['cart'] = ''
        return context
