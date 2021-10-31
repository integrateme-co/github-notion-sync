from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rest_framework import response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, renderer_classes
from drf_yasg import renderers
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from notion import *
from rest_framework import status
from django.contrib.auth.decorators import login_required
from api_data.models import apiStoreModel, integrationModel
from .serializers import apiStoreSerializer, integrationSerializer
domain = "https://api.integrateme.co/github-notion/sync/"


@api_view(['GET'])
def redirect_view(request):
    response = redirect('https://integrateme.co/')
    return response

@api_view(['GET', 'POST'])
def get_user(request, intID):
    data = integrationModel.objects.filter(id=intID)
    serializer = integrationSerializer(data, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=apiStoreSerializer)
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


@login_required
@api_view(['GET'])
def get_url(request):
    data = integrationModel.objects.filter(user_id=request.user.id)
    serizalizer = integrationSerializer(data, many=True)
    return Response(serizalizer.data)

@swagger_auto_schema(method='post', request_body=integrationSerializer)
@api_view(['GET', 'POST'])
def save_integration(request):
    if request.method == 'POST':
        input_data = request.data
        input_data['user_id'] = request.user.id
        serialized_data = integrationSerializer(data=input_data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        data = integrationModel.objects.filter(user_id=request.user.id)
        serializer = integrationSerializer(data, many=True)
        return Response(serializer.data)

@login_required
@api_view(['GET', 'POST'])
def get_token(request):
    notionCode = request.GET.get('code', None)
    oAuth_token = get_bearer(notionCode)
    db_id = get_pageID(oAuth_token)
    new_record = integrationModel.objects.create(
        user_id = request.user.id,
        notion_Oauth= oAuth_token,
        notion_pg_id='null',
        notion_db_id= db_id,
    )
    sync_url = domain + str(new_record.id)
    new_record.save()
    req_record = integrationModel.objects.filter(id=new_record.id).update(sync_url=sync_url)
    return Response(sync_url)


@api_view(['GET', 'POST'])
def get_webhook(request, intID):
    required_rec = integrationModel.objects.filter(id=intID).first()
    oauth_token = required_rec.notion_Oauth
    db_id = required_rec.notion_db_id
    headers = {
    "Authorization": "Bearer " + oauth_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}
    bodyData = request.data
    print(bodyData)
    if request.method == 'POST':
        action = bodyData['action']
        issueTitle = bodyData['issue']['title']
        link = bodyData['issue']['html_url']
        issueID = bodyData['issue']['id']

        if action == 'opened':
            createPage(db_id, headers, issueTitle, link, issueID)
        elif action == 'closed':
            closedIssueID = bodyData['issue']['id']
            closedPageID = searchDB(db_id, closedIssueID, headers)
            Move2Completed(closedPageID, headers)
    return Response(bodyData)
