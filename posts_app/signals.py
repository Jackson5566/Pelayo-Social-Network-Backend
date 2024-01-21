from firebase_admin import storage as firebase_storage


def posts_callback(sender, instance, *args, **kwargs):
    try:
        file = firebase_storage.bucket().blob(instance.image.name)
        file.delete()
    except Exception as e:
        print(f"Error al eliminar el archivo: {e}")