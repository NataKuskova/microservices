from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from api.serializers import *
from db_tea.models import *
from cart import models
from cart import cart
import json


class ProductList(APIView):

    # List all products, or create a new product.

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):
        product = Product.objects.get(pk=request.data['id'])
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    #
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class ProductViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field = 'name'
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BuyerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ListOfOrderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = ListOfOrder.objects.all()
    serializer_class = ListOfOrderSerializer


class CartView(APIView):
    queryset = models.Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request, format=None):
        carts = models.Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cart_ = cart.Cart(request)
        try:
            product = Product.objects.get(id=request.data['id'])
            quantity = 1
            cart_.add(product, product.price, quantity)
            return Response(json.dumps({'count': cart_.count(),
                                        'cart_id': self.request.session.get(
                                            'CART-ID')
                                        }))
        except:
            return Response(json.dumps({'count': cart_.count(),
                                        'cart_id': self.request.session.get(
                                            'CART-ID')
                                        }))
        # serializer = CartSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CartViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = models.Cart.objects.all()
#     serializer_class = CartSerializer
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CartDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = models.Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        cart_ = cart.Cart(request)
        return Response(cart_)
        # return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.Item.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
