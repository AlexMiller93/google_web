# pip install pydrive

'''
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Create local webserver and auto handles authentication.
gauth.LocalWebserverAuth()

try:
    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
    file1.SetContentString('Hello World!') # Set content of the file from given string.
    file1.Upload()

except Exception as e:
    print(f'Something broke, Exception: \n{e}') 
'''

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

# https://www.datalytics.ru/all/rabotaem-s-api-google-drive-s-pomoschyu-python/

pp = pprint.PrettyPrinter(indent=4)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'token.json' # credentials.json, client_secrets.json 

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

'''
# script to show list of files in google drive
results = service.files().list(
    pageSize=3,
    fields="nextPageToken, files(id, name, mimeType)").execute()

pp.pprint(results)

print(len(results.get('files')))

'''

'''
nextPageToken = results.get('nextPageToken')

results_for_next_page = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name, mimeType)",
        pageToken=nextPageToken
    ).execute()

print(results_for_next_page.get('nextPageToken'))

results = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
'''

'''
nextPageToken = results.get('nextPageToken')
while nextPageToken:
    nextPage = service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType, parents)",
            pageToken=nextPageToken
        ).execute()
    nextPageToken = nextPage.get('nextPageToken')
    results['files'] = results['files'] + nextPage['files']
print(len(results.get('files')))
'''

'''
# script to create files
folder_id = '1i6nsy6SHstXkkjYIcXFbZViKzSOKuvQp'
name = 'Test.txt'
file_path = 'Test.txt'
file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
media = MediaFileUpload(file_path, resumable=True)
r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
pp.pprint(r)
'''
