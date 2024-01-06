from django.core.files.storage import FileSystemStorage
from firebase_admin import storage as firebase_storage


class FirebaseStorage(FileSystemStorage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _open(self, name, mode='rb'):
        file = firebase_storage.bucket().blob(name)
        return file.download_as_string()

    def _save(self, name, content):
        file = firebase_storage.bucket().blob(name)
        file.upload_from_file(content)
        file.make_public()
        return name

    def delete(self, name):
        print("Se llamo")
        file = firebase_storage.bucket().blob(name)
        file.delete()

    def url(self, name):
        return firebase_storage.bucket().blob(name).public_url

    def exists(self, name):
        blob = firebase_storage.bucket().blob(name)
        return blob.exists()