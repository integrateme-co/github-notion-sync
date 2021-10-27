from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from notion import *
from rest_framework import status
from django.contrib.auth.decorators import login_required
from api_data.models import apiStoreModel, integrationModel
from .serializers import apiStoreSerializer, integrationSerializer

@api_view(['GET', 'POST'])
def get_user(request, intID):
    data = integrationModel.objects.filter(id=intID)
    serializer = integrationSerializer(data, many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET', 'POST'])
def save_apis(request):
    if request.method == 'POST':
        input_data = request.data
        input_data['id'] = request.user.id
        serialized_data = apiStoreSerializer(data=input_data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        data = apiStoreModel.objects.filter(id=request.user.id)
        serializer = apiStoreSerializer(data, many=True)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def save_integration(request):
    if request.method == 'POST':
        input_data = request.data
        input_data['user_id'] = request.user.id
        serialized_data = integrationSerializer(data=input_data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        data = integrationModel.objects.filter(user_id=request.user.id)
        serializer = integrationSerializer(data, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_token(request):
    notionCode = request.GET.get('code', None)
    oAuth_token = get_bearer(notionCode)
    new_record = integrationModel(
        user_id = request.user.id,
        notion_Oauth= oAuth_token,
        notion_pg_id='uzair',
        notion_db_id= 'uzair'
    )

    return Response(new_record.id)