from pprint import pprint
from datetime import datetime
import requests
import shutil
import os
import json

from tok import ya_token, vk_token
from ya_disk import YandexDisk
from vk_api import VkApiHandler

def loading_photo(data, photo_count=5):
    resul_json = []
    counter = 0
    yd = YandexDisk(token=ya_token)
    for photo in data:
        foto_download = requests.get(photo['url'])
        if foto_download.status_code == 200:
            files = yd.get_files_list()['items']
            #pprint(files)
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
            if status == 201:
                counter += 1
                if len(data) > photo_count:
                    print(f'{counter} from {photo_count} photos saved on the yandex disk')
                else:
                    print(f'{counter} from {len(data)} photos saved on the yandex disk')
                if counter == photo_count:
                    break
    return resul_json

if __name__ == '__main__':
    vk = VkApiHandler(vk_token, '5.131')
    data = vk.search_photos(owner_id=1, album_id='wall')
        
    try:
        shutil.rmtree("downloaded_photo/")
    except OSError as e:
        #print("Error: %s : %s" % ("downloaded_photo/", e.strerror))
        pass
    os.mkdir("downloaded_photo")
    if data != 0:
        resul_json = loading_photo(data, 10)
        
        with open('resul_json.txt', 'w') as f:
            json.dump(resul_json, f)