import requests
from pprint import pprint
import os.path
import json

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()


class VKUser:

     def __init__(self, token, version):
        self.params = {
            'token': token,
            'v': version
        }

     def get_photos(self, vk_id):

        url = 'https://api.vk.com/method/'
        params = {
            'owner_id': vk_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 0,
            'count': 50
        }
        res = requests.get(url=url, params={**self.params, **params}).json()
        profile_list = res['response']['items']
        for i in profile_list:
            dict = (i['sizes'][-1])
            photo_url = (dict['url'])
            file_name = i['likes']['count']
            download_photo = requests.get(photo_url)
            with open(os.path.join('fotos', f'{file_name}.jpg'), 'wb') as file:
                file.write(download_photo.content)
        return "Фотографии скачены"


class YaUploader:

    def __init__(self, token):
        self.token = token

    def folder_creation(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        requests.put(f'{url}?path={path}', headers=headers)

    def file_uploader(self, loadfile, savefile, replace=False):
        url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        res = requests.get(f'{url}/upload?path={savefile}&overwrite={replace}', headers=headers)
        with open(loadfile, 'rb') as f:
            try:
                requests.put(res['href'], files={'file': f})
            except KeyError:
                print(res)

    def upload_photo(self, list_photo, path):
        url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

        logs_list = []

        for photo in list_photo:
            params = {'path': f'{path}/{photo}'}
            get_upload_url = requests.get(url=url, headers=headers, params=params).json()
            file_upload = requests.put(get_upload_url['href'], data=open(f'{path}/{photo}', 'rb'),
                                       headers=headers)
            status = file_upload.status_code

            download_log = {'file_name': photo}
            logs_list.append(download_log)

        with open('log.json', 'a') as file:
            json.dump(logs_list, file, indent=2)

        if 500 > status != 400:
            print('Фотографии загружены')
        else:
            print('Ошибка')


def create_folder(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)


def get_photos_from_folder(folder):
    file_list = os.listdir(folder)
    return file_list


if __name__ == '__main__':
    create_folder('Photos')
    vk_client = VKUser(token, '5.131')
    pprint(vk_client.get_photos(''))
    file_list = get_photos_from_folder('Photos')
    token = ''
    yadisk = YaUploader(token)
    yadisk.folder_creation('photos')
    yadisk.upload_photo(file_list, 'photos')
