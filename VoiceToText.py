#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import json
import uuid
import base64
import requests
import os

dir = '/home/pedestrian/Desktop/VoiceToText/'


class voice_to_text:
    def __init__(self):
        self.recognized_result = ''
        self.voice_to_text_url = 'http://vop.baidu.com/server_api'
        self.apiKey = "1GQyi2TtlQc1xmkAkiaHzNtL"
        self.secretKey = "mcdf5t6QZWNHzGbwFkhjm5nT3KuKrMyf"
        self.auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + self.apiKey + "&client_secret=" + self.secretKey;
        self.access_token = self.get_token()
        self.cuid = uuid.UUID(int=uuid.getnode()).hex[-12:]
        self.baidu_voice_to_text()

    def get_token(self):
        res = urllib.request.urlopen(self.auth_url)
        json_data = res.read()
        return json.loads(json_data.decode())['access_token']

    def baidu_voice_to_text(self):
        for _, _, filenames in os.walk(dir + 'wav/'):
            for filename in filenames:
                wav_file = open(dir + 'wav/' + filename, 'rb')
                text_file = open(dir + 'text/' + filename.split('.')[0] + '.txt', 'w')
                voice_data = wav_file.read()
                wav_file.close()
                data = {'format': 'wav', 'rate': 16000, 'channel': 1, 'cuid': self.cuid, 'token': self.access_token,
                        'lan': 'zh', 'len': len(voice_data), 'speech': base64.b64encode(voice_data).decode('utf-8')}
                result = requests.post(self.voice_to_text_url, json=data, headers={'Content-Type': 'application/json'},
                                       stream=False)
                data_result = result.json()
                if data_result['err_no'] == 0:
                    text_file.write(data_result['result'][0])
                text_file.close()


if __name__ == "__main__":
    voice_to_text()
    print("voice_to_text is over!")
