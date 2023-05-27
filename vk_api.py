import os
import requests

from dotenv import load_dotenv

from test_data import TEXT_COMMENT, GROUP_URL, API_VERSION

load_dotenv()


class VkAPI:
    vk_token = os.getenv('VK_TOKEN')
    api_url = "https://api.vk.com/method/"
    version = API_VERSION

    @staticmethod
    def get_object_id(url: str) -> int:
        """
        Метод принимает url станицы со скриннэймом и возвращает
        её id если это страница пользователя, и -id для страницы сообщества.
        """
        screen_name = url.split('/')[-1]
        params = {'access_token': VkAPI.vk_token,
                  'screen_name': screen_name,
                  'v': VkAPI.version}
        response = requests.get(url=f'{VkAPI.api_url}utils.resolveScreenName?', params=params)
        result = response.json()['response']
        return result['object_id'] if result['type'] == 'user' else -result['object_id']

    @staticmethod
    def create_comment(photo_id: int, **kwargs) -> None:
        """
        Метод оставляет комментарий к фото
        """
        params = {'access_token': VkAPI.vk_token,
                  'photo_id': photo_id,
                  'v': VkAPI.version}
        params.update(kwargs)
        requests.get(url=f'{VkAPI.api_url}photos.createComment?', params=params)

    @staticmethod
    def get_avatar_id(**kwargs) -> int:
        """
        Метод возвращает id аватара страницы
        """
        params = {'access_token': VkAPI.vk_token,
                  'album_id': 'profile',
                  'v': VkAPI.version}
        params.update(kwargs)
        response = requests.get(url=f'{VkAPI.api_url}photos.get?', params=params)
        return response.json()['response']['items'][-1]['id']


if __name__ == "__main__":
    owner_id = VkAPI.get_object_id(GROUP_URL)
    avatar_id = VkAPI.get_avatar_id(owner_id=owner_id)
    VkAPI.create_comment(avatar_id, owner_id=owner_id, message=TEXT_COMMENT)
