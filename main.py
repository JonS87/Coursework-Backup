from pprint import pprint
from datetime import datetime
import requests
import shutil
import os
import json
from progress.bar import FillingCirclesBar

from tok import ya_token, vk_token
from ya_disk import YandexDisk
from vk_api import VkApiHandler

def loading_photo(data, photo_count=5):
    resul_json = []
    counter = 0
    yd = YandexDisk(token=ya_token)
    df = yd.folder_create('/Netology homework')
    if len(data) > photo_count:
        max_photo_count = photo_count
    else:
        max_photo_count = len(data)
    bar = FillingCirclesBar('Countdown', max = max_photo_count)
    bar.start()
    for photo in data:
        foto_download = requests.get(photo['url'])
        if foto_download.status_code == 200:
            files = yd.get_files_list()['items']
            check = 0
            for el in files:
                if el['path'][ :24] == 'disk:/Netology homework/' and el['name'] == f"{photo['likes']}.jpg":
                    check = 1
            
            if check == 0:
                file_name = f"{photo['likes']}.jpg"
            else:
                file_name = f"{photo['likes']}__{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            file = {
                    'file_name': file_name,
                    'size': photo['size']
                }
            with open(f"downloaded_photo/{file_name}", 'wb') as f:
                f.write(foto_download.content)
            
            resul_json.append(file)
            status = yd.upload_file_to_disk(f"Netology homework/{file_name}", f"downloaded_photo/{file_name}")
            
            bar.next()
    bar.finish()
    return resul_json

if __name__ == '__main__':
    photo_count = int(input('Введите количество фотографий для загрузки: '))
    
    vk = VkApiHandler(vk_token, '5.131')
    data = vk.search_photos(owner_id=1, photo_count=photo_count, album_id='wall')
        
    try:
        shutil.rmtree("downloaded_photo/")
    except OSError as e:
        #print("Error: %s : %s" % ("downloaded_photo/", e.strerror))
        pass
    os.mkdir("downloaded_photo")
    if data != 0:        
        result_json = loading_photo(data, photo_count)
        
        with open('result.json', 'w') as f:
            json.dump(result_json, f)