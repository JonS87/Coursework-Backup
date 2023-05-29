from pprint import pprint
import time
from tok import TOKEN, vk_token
#from ya_disk import YandexDisk

import pandas as pd
import requests

#yd = YandexDisk(token=TOKEN)
#yd.upload_file_to_disk("Netology homework/test.txt", "test.txt")

class VkApiHandler:
    base_url = 'https://api.vk.com/method/'
    def __init__(self, access_token, version='5.131'):
        self.params = {
            'access_token': access_token,
            'v': version
        }
    
    def get_user_data(self, user_ids):
        url = self.base_url + 'users.get'
        params ={'user_ids': user_ids,
                 **self.params
                }
        data = requests.get(url,params=params).json()
        return data

    def get_user_data_extended(self, user_ids, fields):
        url = self.base_url + 'users.get'
        params ={'user_ids': user_ids,
                'fields': fields,
                **self.params
                }
        data = requests.get(url,params=params).json()
        return data
    
    def search_groups(self, q, sort, count):
        url = self.base_url + 'groups.search'
        params = {
            'q': q,
            'sort': sort,
            'count': count,
            **self.params
        }
        data = requests.get(url, params=params).json()
        return data['response']
    
    def search_news(self, q):
        url = self.base_url + 'newsfeed.search'
        params = {
            'q': q,
            'count': 5,
            **self.params
        }
        #news_frame = pd.DataFrame()
        news = []
        while True:
            time.sleep(0.34)
            data = requests.get(url, params=params).json()
            #news_frame = pd.concat([news_frame, pd.DataFrame(data['response']['items'])])
            news.extend(data['response']['items'])
            if 'next_from' in data['response']:
                params.update({'start_from':data['response']['next_from']})
            else:
                pass
            print(len(news))
            break
        #return news_frame
        return news
    
if __name__ == '__main__':
    #data = get_user_data(vk_token)
    vk = VkApiHandler(vk_token, '5.131')
    #data = vk.get_user_data_extended('1', 'bdate,city,followers_count')
    #data = vk.search_groups('python', 6, 10)
    data = vk.search_news('авто')
    pprint(data)
    #print(pd.DataFrame(data['items']))