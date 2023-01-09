import os
import requests
from vk_token import vk_token
import datetime
import json
from tqdm import tqdm


def max_size_photo(photo_dict):
    max_size = 0
    photo = 0
    for i in range(len(photo_dict)):
        file_size = photo_dict[i].get('width') * photo_dict[i].get('height')
        if file_size > max_size:
            max_size = file_size
            photo = i
    return photo_dict[photo].get('url'), photo_dict[photo].get('type')


def time_convert(time_unix):
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return str_time


class VkDownloader:
    def __init__(self, token):
        self.token = token

    def _get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id,
                  'album_id': 'profile',
                  'access_token': vk_token,
                  'photo_sizes': 1,
                  'extended': 1,
                  'rev': 1
                  }
        photo_info = requests.get(url, params={**self.start_params, **params}).json()['response']
        return photo_info['count'], photo_info['items']

    def _get_logs_only(self):
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = max_size_photo(photo_items[i]['sizes'])
            time_warp = time_convert(photo_items[i]['date'])
            new_value = result.get(likes_count, [])
            new_value.append({'likes_count': likes_count,
                              'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        counter = 0
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{value["likes_count"]}.jpeg'
                else:
                    file_name = f'{value["likes_count"]} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                if value["likes_count"] == 0:
                    sorted_dict[file_name] = picture_dict[elem][counter]['url_picture']
                    counter += 1
                else:
                    sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict


class Yandex:
    def __init__(self, folder_name, token, num=5):
        self.token = token
        self.added_files_num = num
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': f'OAuth {ya_token}'}
        self.folder = self._create_folder(folder_name)

    def _create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка {folder_name} создана в каталоге Яндекс диска\n')
        else:
            print(f'\nПапка {folder_name} уже существует.\n')
        return folder_name

    def _in_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem['name'])
        return in_folder_list

    def create_copy(self, dict_files):
        files_in_folder = self._in_folder(self.folder)
        copy_counter = 0
        for key, i in zip(dict_files.keys(), tqdm(range(self.added_files_num))):
            if copy_counter < self.added_files_num:
                if key not in files_in_folder:
                    params = {'path': f'{self.folder}/{key}',
                              'url': dict_files[key],
                              'overwrite': 'false'}
                    requests.post(self.url, headers=self.headers, params=params)
                    copy_counter += 1
                else:
                    print(f'Файл {key} уже существует')
            else:
                break

        print(f'\nНовых файлов: {copy_counter}'
              f'\nВсего файлов альбоме VK: {len(dict_files)}')


if __name__ == '__main__'

    user_id = str(input('Введите id пользователя VK: '))
    downloader = VkDownloader(vk_token)

    with open('VK_photo.json', 'w') as outfile:
        json.dump(VK.json, outfile)

    ya_token = str(input('Введите ваш токен ЯндексДиск: '))
    uploader = Yandex(ya_token)
    uploader._create_folder()