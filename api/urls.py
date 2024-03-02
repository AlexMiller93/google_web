from django.urls import path
from .views import create_google_drive_document_pydrive, create_google_doc

urlpatterns = [
    path('create-google-drive-pydrive/', create_google_drive_document_pydrive, 
        name='create_drive_pydrive'),
    path('create-google-doc/', create_google_doc, 
        name='create_google_doc')
]

# http://127.0.0.1:8000/api/create-google-drive-pydrive/?name=test.txt&data=Test%20content