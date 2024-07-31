import hashlib
import random
import json
import urllib.parse
import http.client
import logging
import requests  # Add requests library for Google Translate

class Translator:
    def __init__(self, appid, secret_key, service):
        self.appid = appid
        self.secret_key = secret_key
        self.service = service

    def translate(self, q, from_lang, to_lang):
        if self.service == 'baidu':
            return self.baidu_translate(q, from_lang, to_lang)
        elif self.service == 'google':
            return self.google_translate(q, from_lang, to_lang)
        else:
            logging.error(f"Unsupported translation service: {self.service}")
            return None

    def baidu_translate(self, q, from_lang, to_lang):
        myurl = '/api/trans/vip/translate'
        salt = random.randint(32768, 65536)
        sign = self.appid + q + str(salt) + self.secret_key
        m1 = hashlib.md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        myurl = (myurl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign)

        try:
            http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
            http_client.request('GET', myurl)
            response = http_client.getresponse()
            json_response = response.read().decode('utf-8')
            result = json.loads(json_response)
            print(result)
            return result
        except Exception as e:
            logging.error(f"Translation error: {e}")
            return None
        finally:
            if http_client:
                http_client.close()

    def google_translate(self, q, from_lang, to_lang):
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            'q': q,
            'source': from_lang,
            'target': to_lang,
            'key': self.secret_key 
        }
        try:
            response = requests.get(url, params=params)
            result = response.json()
            print(result)
            return result
        except Exception as e:
            logging.error(f"Translation error: {e}")
            return None
