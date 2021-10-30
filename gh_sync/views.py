from django.shortcuts import render
from rest_framework.response import Response
from api_data.models import integrationModel
from rest_framework.decorators import api_view, renderer_classes
from drf_yasg import renderers
from notion import Move2Completed, createPage, searchDB

domain = "http://api-integrateme.herokuapp.com/github-notion/sync/"


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