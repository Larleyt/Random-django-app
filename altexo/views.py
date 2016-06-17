from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.cache import never_cache

from django.contrib.auth import get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics, serializers, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import UserProfile, Invoice, Service, Subscription 
from .serializers import InvoiceSerializer, ServiceSerializer, SubscriptionSerializer
from .permissions import IsAdminUserOrReadOnly
import json


# API root for browsable API (wip)
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'invoices': reverse('invoice-list', request=request, format=format),
#         'services': reverse('service-list', request=request, format=format),
#         'subscriptions': reverse('subscription-list', request=request, format=format),       
#     })


# Invoice API
class InvoiceList(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        If current user has is_staff == True, returns a list of all the invoices,
        else returns invoices of the authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Invoice.objects.all() 
        return Invoice.objects.filter(user=user)


class InvoiceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        """
        If current user has is_staff == True, returns any invoice,
        else returns an invoice of just the authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Invoice.objects.all() 
        return Invoice.objects.filter(user=user)
#~


# Service API
class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()    
    serializer_class = ServiceSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()    
    serializer_class = ServiceSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
#~


# Subscription API
class SubscriptionList(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        If current user has is_staff == True, returns a list of all the subscriptions,
        else returns subscriptions of the authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Subscription.objects.all() 
        return Subscription.objects.filter(user=user)


class SubscriptionCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, service_id, format=None):
        serializer = SubscriptionSerializer(data={
                        'user': request.user.pk,
                        'service': Service.objects.get(id=service_id).pk
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionDetail(generics.RetrieveDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        If current user has is_staff == True, returns any subscription,
        else returns a subscription of just the authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Subscription.objects.all() 
        return Subscription.objects.filter(user=user)
#~


@ensure_csrf_cookie
def landing(request):
    return render(request, 'landing/base.html')

# @never_cache
@ensure_csrf_cookie
def streams(request):
    return render(request, 'streams/streams.html')

@ensure_csrf_cookie
def get_csrf(request):
    return HttpResponse()

# @never_cache
# @ensure_csrf_cookie
# def single_stream(request):
#     return render(request, 'streams/single_stream.html')

# @never_cache
# @ensure_csrf_cookie
# def live_stream(request):
#     return render(request, 'streams/live-stream.html')

#@csrf_exempt
#def test(request):
    # if request.method == 'POST':
    #     body_unicode = request.body.decode('utf-8')
    #     json_dt = json.loads(body_unicode)
    #     with open('cube.json', 'w') as outfile:
    #         json.dump(json_dt, outfile)
    #
    #     return HttpResponse(json.dumps({'test':'test'}))


# API methods

