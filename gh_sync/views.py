from rest_framework.response import Response
from rest_framework.decorators import api_view
from api_data.models import integrationModel
from notion import Move2Completed, createPage, searchDB

DOMAIN = "https://api.integrateme.co/github-notion/sync/"

@api_view(['GET', 'POST'])
def get_webhook(request, int_id):
    """Listen for wehooks from github"""
    required_rec = integrationModel.objects.filter(id=int_id).first()
    oauth_token = required_rec.notion_Oauth
    db_id = required_rec.notion_db_id
    headers = {
    "Authorization": "Bearer " + oauth_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}
    body_data = request.data
    print(body_data)
    if request.method == 'POST':
        action = body_data['action']
        issue_title = body_data['issue']['title']
        link = body_data['issue']['html_url']
        issue_id = body_data['issue']['id']

        if action == 'opened':
            createPage(db_id, headers, issue_title, link, issue_id)
        elif action == 'closed':
            closed_issue_id = body_data['issue']['id']
            closed_page_id = searchDB(db_id, closed_issue_id, headers)
            Move2Completed(closed_page_id, headers)
    return Response(body_data)
