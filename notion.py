import requests, json, os

token = 'secret_5KfCWRI1TLWbTpKrrq3WjoyIcvAww1IYn9sPei3bMOo'
# token = request.COOKIES['oauth_token']
# token = str(token)

databaseId = 'f22775996b054d97ad5eaf15b1e15a30'

# headers = {
#     "Authorization": "Bearer " + token,
#     "Content-Type": "application/json",
#     "Notion-Version": "2021-05-13"
# }

def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    #results[0].properties.ID.number
    # print(res.text)
    for obj in data['results']:
        print(obj['properties']['ID']['number'])
    #print(data['results'][0]['properties']['ID']['number'])

    with open('./NotionDB.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

#readDatabase(databaseId, headers)


def searchDB(database_id, issueID):
    queryURL = f"https://api.notion.com/v1/databases/{database_id}/query"

    headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

    queryParams = {
					"database_id": database_id,
					"filter": {
						"property": 'ID',
						"number": {
							"equals": issueID
						}
					}
				}

    data = json.dumps(queryParams)
    response = requests.request("POST", queryURL, headers=headers, data=data)

    print(response.status_code)
    response = response.json()
    return response['results'][0]['id']


def Move2WithPR(pageId, headers):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    updateData = {
        "properties": {
    "Status":{
  "id": "=_;M",
  "type": "select",
  "select": {
    "id": "2",
    "name": "Issues With Pull Request",
    "color": "yellow"
  }
}
}
    }

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)

#Move2WithPR('0f53f1c2-2917-4ce0-b129-da1605547740', headers)


def Move2Completed(pageId, headers):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    updateData = {
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

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)


#Move2Completed('0f53f1c2-2917-4ce0-b129-da1605547740', headers)


def Move2Open(pageId, headers):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    updateData = {
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

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)

#Move2Open('0f53f1c2-2917-4ce0-b129-da1605547740', headers)


def createPage(databaseId, headers, title, issueURL, issueID):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": databaseId },
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
                "url": f"{issueURL}"
        },

        "ID": {
                "id": "eEq_",
                "type": "number",
                "number": issueID
        }          

        }
    }
    
    data = json.dumps(newPageData)

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print("Status: ", res.status_code)
    print(res.text)


oauth_header = {
    "Authorization": "Basic NzI3NzQxMjUtNmI0Yi00ZTU4LTlkYTYtZmVkOTRkYzUwYjZhOnNlY3JldF84Q25hekF6WXRFWFFjM0xlWTVkRVJnczRFOFBEZ3FFVlFReHpzZ2U1T3NM",
}

def get_bearer(code):
    requestURL = "https://api.notion.com/v1/oauth/token"

    bodyData = {
        "grant_type":"authorization_code",
        "code":f"{code}",
        "redirect_uri": "https://127.0.0.1:8000/notion-github"
    }

    data = json.dumps(bodyData)

    response = requests.post(requestURL, headers=oauth_header, data=data)
    print(response.status_code)
    print(response.text)


oauth_header = {'Authorization': 'Basic NzI3NzQxMjUtNmI0Yi00ZTU4LTlkYTYtZmVkOTRkYzUwYjZhOnNlY3JldF9OS3NnZHFWNVFvOHdQVk93dkc5dUJCQkZjaXp3VnlQWGtXYmVoOTRhM0lx'}

def get_bearer(code):
    requestURL = "https://api.notion.com/v1/oauth/token"

    bodyData = {
        "grant_type" : "authorization_code",
        "code" : f'{code}',
    }

    response = requests.post(requestURL, headers=oauth_header, data=bodyData)
    response = response.json()
    # if response['error']:
    #     error_res = {
    #         'error':"Invalid Grant or Notion Code"
    #     }
    #     return error_res
    return (response['access_token'])

# ans = get_bearer('245762e8-a8ee-4a08-a125-dfc0c893fe5d')
# print(ans)


def get_pageID(OAuth_token):

    searchURL = "https://api.notion.com/v1/search"

    search_header = {
        "Authorization": f"{OAuth_token}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json"
    }

    search_body = {}
    response = requests.post(searchURL, headers=search_header, data=search_body)
    response = response.json()
    return (response)