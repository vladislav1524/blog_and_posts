from .models import UserProfile
from datetime import datetime
from django.core.files.base import ContentFile
import requests

def create_profile(backend, user, response, *args, **kwargs):
    """
    Создание профиля пользователя для социальной аутентификации
    """
    default_date_of_birth = datetime(2000, 1, 1).date()

    # Получаем или создаем профиль пользователя
    user_profile, created = UserProfile.objects.get_or_create(user=user, defaults={'date_of_birth': default_date_of_birth})

    # Получаем имя пользователя из ответа
    first_name = response.get('first_name', '') or response.get('given_name', '')
    last_name = response.get('last_name', '') or response.get('family_name', '')
    user_profile.user.username = f"{first_name} {last_name}"  # Устанавливаем имя профиля

    # Проверяем, откуда пришел пользователь
    if backend.name == 'vk-oauth2':
        # Получаем access_token
        access_token = response.get('access_token')

        # Запрос данных пользователя с использованием access_token
        if access_token:
            user_info_response = requests.get(
                "https://api.vk.com/method/users.get",
                params={
                    "fields": "bdate,photo_max",
                    "access_token": access_token,
                    "v": "5.131"  # Версия API
                }
            )

            user_info = user_info_response.json().get('response', [{}])[0]

            # Получаем дату рождения
            bdate = user_info.get('bdate')
            if bdate:
                try:
                    # Предполагаем, что дата приходит в формате "DD.MM.YYYY"
                    date_of_birth = datetime.strptime(bdate, '%d.%m.%Y').date()
                    user_profile.date_of_birth = date_of_birth
                except ValueError:
                    # Обработка ошибки, если формат даты неверный
                    print("Неверный формат даты рождения:", bdate)

            # Получаем фото профиля
            photo_url = user_info.get('photo_max')  # Или используйте 'photo_200'

    elif backend.name == 'google-oauth2':
        # Получаем фото профиля от Google
        photo_url = response.get('picture')  # URL фото профиля от Google
        # Google не предоставляет дату рождения, поэтому можно оставить поле пустым или использовать другое поле

    if photo_url:
        # Загружаем изображение и сохраняем его в поле image
        image_response = requests.get(photo_url)
        if image_response.status_code == 200:
            user_profile.image.save(f"{user.username}_avatar.jpg", ContentFile(image_response.content))

    user_profile.save()
