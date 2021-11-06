import json
import requests

def readDatabase(database_id, headers):
    """Read the whole Notion DB"""
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"

    res = requests.request("POST", read_url, headers=headers)
    data = res.json()
    for obj in data['results']:
        print(obj['properties']['ID']['number'])




def searchDB(database_id, issue_id, headers):
    """Search for a Card in Notion DB"""
    query_url = f"https://api.notion.com/v1/databases/{database_id}/query"


    query_params = {
					"database_id": database_id,
					"filter": {
						"property": 'ID',
						"number": {
							"equals": issue_id
						}
					}
				}

    data = json.dumps(query_params)
    response = requests.request("POST", query_url, headers=headers, data=data)

    print(response.status_code)
    response = response.json()
    return response['results'][0]['id']

def Move2Completed(page_id, headers):
    """Move a page or card to completed coloum"""
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    update_data = {
                "properties": {
            "Status":{
            "id": "=_;M",
            "type": "select",
            "select": {
                "id": "3",
                "name": "Completed",
                "color": "green"
            }
          }
        }
    }

    data = json.dumps(update_data)

    response = requests.request("PATCH", update_url, headers=headers, data=data)

    print(response.status_code)
    print(response.text)





def Move2Open(page_id, headers):
    """Add a new page or card in open coloum"""
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    update_data = {
        "properties": {
    "Status":{
  "id": "=_;M",
  "type": "select",
  "select": {
    "id": "1",
    "name": "Open Issues",
    "color": "red"
  }
}
}
    }

    data = json.dumps(update_data)

    response = requests.request("PATCH", update_url, headers=headers, data=data)

    print(response.status_code)
    print(response.text)




def createPage(database_id, headers, title, issue_url, issue_id):
    """Create a new Page"""
    create_url = 'https://api.notion.com/v1/pages'

    new_page_data = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": f"{title}"
                        }
                    }
                ]
            },

            "Status":{
                "id": "=_;M",
                "type": "select",
                "select": {
                    "id": "1",
                    "name": "Open Issues",
                    "color": "red"
                }
        },

            "URL": {
                "id": "U>Vt",
                "type": "url",
                "url": f"{issue_url}"
        },

        "ID": {
                "id": "eEq_",
                "type": "number",
                "number": issue_id}}
    }
    data = json.dumps(new_page_data)

    res = requests.request("POST", create_url, headers=headers, data=data)

    print("Status: ", res.status_code)
    print(res.text)


def get_bearer(code):
    """Get User's Bearer Code"""
    request_url = "https://api.notion.com/v1/oauth/token"

    body_data = {
        "grant_type" : "authorization_code",
        "code" : f'{code}',
    }
    oauth_header = {
    'Authorization': 'Basic NzI3NzQxMjUtNmI0Yi00ZTU4LTlkYTYtZmVkOTRkYzUwYjZhOnNlY3JldF9OS3NnZHFWNVFvOHdQVk93dkc5dUJCQkZjaXp3VnlQWGtXYmVoOTRhM0lx'
}

    response = requests.post(request_url, headers=oauth_header, data=body_data)
    response = response.json()
    return response['access_token']


def get_pageID(auth_token):
    """Get Notion's Page ID"""
    search_url = "https://api.notion.com/v1/search"

    search_header = {
        "Authorization": f"{auth_token}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json"
    }

    search_body = {}
    response = requests.post(search_url, headers=search_header, data=search_body)
    response = response.json()
    db_id = response['results'][0]['id']
    return db_id
