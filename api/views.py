from rest_framework.decorators import api_view
from rest_framework.response import Response

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from django.http import HttpResponse, JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from apiclient.http import MediaInMemoryUpload

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# https://djangokatya.com/2022/02/16/google-drive-api-with-python-upload-download-a-file/

# @api_view(['POST'])
def create_google_drive_document_pydrive(request):
    
    # Получаем параметры из POST запроса
    data = request.POST.get('data')
    name = request.POST.get('name')
    
    # аутентификация в Google Auth
    try:
        gauth = GoogleAuth()
        gauth.LocalWebServerAuth()
        
    except Exception as e:
        return f'Local server doesn\'t create, Exception: \n{e}' 
    
    finally:
        print('Auth!')
    
    # 
    try:
        drive = GoogleDrive(gauth)
        
        my_file = drive.CreateFile({'title': name})
        my_file.SetContentString(data)
        my_file.Upload()
    
    except Exception as e:
        return f'Something broke, exception: \n{e}' 
    
    finally:
        print(f'File successfully uploaded!')
        
    print('Finish')
    # return 'All done!'
    
    ''' 
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=SCOPES
        )
    drive_service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.document'
    }

    media = {
        'mimeType': 'text/plain',
        'body': data
    }

    file = drive_service.files().create(body=file_metadata, media_body=media).execute()
    return Response({'file_id': file.get('id')})
    '''
    
def create_google_doc(request):
    
    #! Функция работает, выдает словарь message, но в google drive ничего создается 
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    # Получаем параметры из POST запроса
    data = request.POST.get('data')
    name = request.POST.get('name')

    try:
        # Авторизация с помощью учетных данных Google
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)

        # Создание экземпляра клиента для работы с Google Drive API
        drive_service = build('drive', 'v3', credentials=credentials)

        # Создание документа в Google Drive
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        media = MediaInMemoryUpload(data, mimetype='text/plain')
        file = drive_service.files().create(body=file_metadata, media_body=media).execute()

        # Возвращение успешного результата
        return JsonResponse({'message': f'Document {name} successfully created'}, status=201)

    except Exception as e:
        # Ошибка в случае возникновения исключения
        return JsonResponse({'error': str(e)}, status=500)
    
