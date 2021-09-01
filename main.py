import requests
import time
from datetime import datetime
import json

from tqdm import tqdm

class VKFotos():
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self):
        photos_dict = {}
        photos = self.url + 'photos.get'
        photos_params = {
            'extended': '1',
            'owner_id': '552934290',
            'album_id': 'profile'
            }

        response = requests.get(photos, params={**self.params, **photos_params}).json()
        list_photos = response['response']['items']

        for k in list_photos:
            date_time = datetime.fromtimestamp(k['date'])
            date = str(datetime.date(date_time))
            max_size = 0
            if k['likes']['count'] not in photos_dict:
                likes = k['likes']['count']
            else:
                likes = str(k['likes']['count']) + '_' + date
            for sizes in k['sizes']:
                size = sizes['height'] * sizes['width']
                if size > max_size:
                    x ={}
                    max_size = size
                    url = sizes['url']
                    x[sizes['type']] = url
                    photos_dict[likes] = x
        return photos_dict


class YAfotos():
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, token):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'authorization': f'OAuth {token}'
        }

    def create_folder(self):
        photos_dict = up.get_photos()
        list =[1]
        list_json = []
        name_folder = input('Введите название папки: ')
        requests.put(f'{self.url}', params={'path': {name_folder}}, headers=self.headers)
        for photos in photos_dict:
            name_photo = str(photos)
            for key in photos_dict[photos]:
                response = requests.post(self.url + 'upload', headers=self.headers,
                                         params={'path': f'{name_folder}/{name_photo}.jpg',
                                                 'url': photos_dict[photos][key]})

                if response.ok== True:
                   for i in tqdm(list):
                        time.sleep(1)
                        list_json.append({"file_name":f'{name_photo}.jpeg', "size":key})
                   else:
                       pass
        with open('photo.json', 'w') as outfile:
            json.dump(list_json, outfile)

token_ya = input("Введите токен яндекс диска: ")
up = VKFotos('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008', '5.131')
puting = YAfotos(token_ya)
puting.create_folder()


