import requests
from google_auth_oauthlib.flow import InstalledAppFlow

class GooglePhotosHook():
    def __init__(self, secret_file, scopes, token=False):
 
        def get_token(secret_file, scopes):
            flow = InstalledAppFlow.from_client_secrets_file(
                secret_file, scopes)
            credentials = flow.run_local_server()
            print("Obtained new token:", credentials.token)
            return credentials.token
            
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + (token if token else get_token(secret_file, scopes))
        }
        
        self.page_token = None
        return
        
    def browse_images(self):
        
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
        body = {
            "pageSize": 10,
            "filters": {
                "includeArchivedMedia": False,
                "mediaTypeFilter": {
                    "mediaTypes": [
                        "PHOTO"
                    ],
                },
                "contentFilter": {
                    "excludedContentCategories": [
                        "SCREENSHOTS",
                        "DOCUMENTS",
                    ],
                },
            }
        }
        if self.page_token:
            body["pageToken"] = self.page_token
            
        response = requests.post(url, headers=self.headers, json=body)
        response = response.json()
        self.page_token = response.get("nextPageToken")
        return response
        
    
    
if __name__ == '__main__':
    scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']
    
    # create a hook
    hook = GooglePhotosHook("secret.json", scopes)
    print(hook.browse_images()) 
    
    
    
    