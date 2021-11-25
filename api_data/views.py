from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from api_data.models import apiStoreModel, integrationModel
from .serializers import apiStoreSerializer, integrationSerializer
from notion import *
DOMAIN = "https://api.integrateme.co/github-notion/sync/"


@api_view(['GET'])
def redirect_view(request):
    """Redirect To Homepage"""
    response = redirect('https://integrateme.co/')
    return response

@api_view(['GET', 'POST'])
def get_user(request, int_id):
    """Get User Data"""
    data = integrationModel.objects.filter(id=int_id)
    serializer = integrationSerializer(data, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=apiStoreSerializer)
@login_required
@api_view(['GET', 'POST'])
def save_apis(request):
    """Save API Keys into API Store"""
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
    """Get Sync URL"""
    data = integrationModel.objects.filter(user_id=request.user.id)
    serizalizer = integrationSerializer(data, many=True)
    return Response(serizalizer.data)

@swagger_auto_schema(method='post', request_body=integrationSerializer)
@api_view(['GET', 'POST'])
def save_integration(request):
    """Saves integration Record"""
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
    """Get User's Token"""
    notion_code = request.GET.get('code', None)
    oauth_token = get_bearer(notion_code)
    db_id = get_page_id(oauth_token)
    new_record = integrationModel.objects.create(
        user_id = request.user.id,
        notion_Oauth= oauth_token,
        notion_pg_id='null',
        notion_db_id= db_id,
    )
    sync_url = DOMAIN + str(new_record.id)
    new_record.save()
    return Response(sync_url)


@api_view(['GET', 'POST'])
def get_webhook(request, int_id):
    """Listen for webhooks from GitHub"""
    required_rec = integrationModel.objects.filter(id=int_id).first()
    oauth_token = required_rec.notion_Oauth
    db_id = required_rec.notion_db_id
    headers = {
    "Authorization": "Bearer " + oauth_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}
    body_data = request.data
    if request.method == 'POST':
        action = body_data['action']
        issue_title = body_data['issue']['title']
        link = body_data['issue']['html_url']
        issue_id = body_data['issue']['id']

        if action == 'opened':
            create_page(db_id, headers, issue_title, link, issue_id)
        elif action == 'closed':
            closed_issue_id = body_data['issue']['id']
            closed_page_id = search_db(db_id, closed_issue_id, headers)
            move_2_completed(closed_page_id, headers)
    return Response(body_data)
