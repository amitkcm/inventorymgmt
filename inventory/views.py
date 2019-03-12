from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from .models import Inventory,User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import inventorySerializer


#--------------------------------------------------------
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def invLoginUserToken(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)    
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    manager = 0
    for role in user.role.all():
        if role.is_manager:
            manager = 1
    return Response({'token': token.key,'is_manager':manager},
                    status=HTTP_200_OK)

class inventoryList(viewsets.ModelViewSet):

    serializer_class = inventorySerializer
    queryset = Inventory.objects.all()

    def create(self, request, *args, **kwargs):
        roleQuerySet = request.user.role.all()
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = self.queryset.get(pk=serializer.data.get('id'))
        manager = 0
        for role in roleQuerySet:
            if role.is_manager:
                manager = 1
        if not manager:
            instance.status = 'pending'
            instance.operation = 'create'
            serializer.data.status = 'pending'
            serializer.data.operation = 'create'
        else:
            instance.status = 'approved'
            instance.operation = 'create'
            serializer.status = 'approved'
        instance.save()
        headers = self.get_success_headers(serializer.data)        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        roleQuerySet = request.user.role.all()
        serializer = inventorySerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for role in roleQuerySet:
            if role.is_manager:
                manager = 1
        if not manager:
            instance.status = 'pending'
            instance.operation = 'update'
            serializer.data.status = 'pending'
            serializer.data.operation = 'update'
        else:
            instance.status = 'approved'
            serializer.data.status = 'approved'
        instance.save()        
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        roleQuerySet = request.user.role.all()
        manager = 0
        serializer = inventorySerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for role in roleQuerySet:
            if role.is_manager:
                manager = 1
        if not manager:
            instance.status = 'pending'
            instance.operation = 'update'
            serializer.data.status = 'pending'
            serializer.data.operation = 'update'
        else:
            instance.status = 'approved'
            serializer.data.status = 'approved'
        instance.save()
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        roleQuerySet = request.user.role.all()
        manager = 0
        for role in roleQuerySet:
            if role.is_manager:
                manager = 1
        if not manager:
            record = Inventory.objects.get(pk=pk)
            record.status = 'pending'
            record.operation = 'delete'
            record.save()
            return Response({"Success": "Request Created"}, status=200)
        else:
            return super(inventoryList, self).destroy(request,pk)


def invLoginUser(request):
    return render(request,'inventory/login.html',{'titel':"Login"})

def invRecordList(request):
    return render(request,'inventory/list.html')


# def create_inventory(request):
#     data = request.POST
#     user = request.user
#     if user.is_authenticated():
#       return render(request,'/',{})

# User this method if wishes all records without API
class InventoryListView(ListView):
    queryset = Inventory.objects.all()
    template_name = "inventory/list.html"

# User this method if wishes record by Id without API
class InventoryDetailView(DetailView):
    queryset = Inventory.objects.all()
    template_name = "inventory/detail.html"

