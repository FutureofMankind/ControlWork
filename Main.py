import json
from VK import VkDownloader
from Yandex import Yandex
from VK import vk_token
from Yandex import ya_token

downloader = VkDownloader(vk_token)

with open('VK_photo.json', 'w') as outfile:
    json.dump(downloader.json, outfile)

uploader = Yandex(ya_token, 5)
uploader.create_copy(downloader.export_dict)