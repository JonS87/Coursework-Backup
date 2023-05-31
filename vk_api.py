import time
import requests

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
    
    def search_photos(self, owner_id, album_id='profile'):
        url = self.base_url + 'photos.get'
        params = {
            'owner_id': owner_id,
            'album_id': album_id, #'profile, wall, saved',
            'extended': 1,
            **self.params
        }
        data = requests.get(url, params=params).json()
        photo_info = []
        all_type_width = {
            's': 75,
            'm': 130,
            'x': 604,
            'o': 130,
            'p': 200,
            'q': 320,
            'r': 510,
            'y': 807,
            'z': 1024,
            'w': 2048,
            'a': 0
        }
        try:
            for item in data['response']['items']:
                max_width_url = ''
                max_width_type = 'a'
                for width1 in item['sizes']:
                    if all_type_width[width1['type']] > all_type_width[max_width_type]:
                        max_width_url = width1['url']
                        max_width_type = width1['type']
                    
                photo = {
                    'likes': item['likes']['count'],
                    'size': max_width_type,
                    'url': max_width_url
                }
                photo_info.append(photo)        
            return photo_info
        except KeyError as e:
            print(f'{album_id} photo missing')
            return 0