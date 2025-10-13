import requests
from django.core.files.base import ContentFile

def download_avatar(user, url):
    response = requests.get(url)
    print("url: ", url)
    print("response: ", response)
    print("status:", response.status_code)

    if response.status_code == 200:
        # Creo un ContentFile con los bytes descargados
        content = ContentFile(response.content)

        # Guardo en un ImageField de un modelo
        user._profile_image.save("avatar.jpg", content)
        user.save()