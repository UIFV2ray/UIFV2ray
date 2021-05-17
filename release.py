#!/usr/bin/env python3

import json
import os
import requests
import datetime
import sys

from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')

NOW_TIME = str(int(datetime.datetime.now().timestamp()))
TOKEN = os.getenv('GITHUB_TOKEN', default='')

repo = 'UIFV2ray/UIFV2ray'
tag = NOW_TIME
name = "UIFV2ray 下载页面"
upload_file = BASE_DIR + '/runtime/linux.zip'

#######################################################################
#                               delete                               #
#######################################################################
respon = requests.get(
    'https://api.github.com/repos/UIFV2ray/UIFV2ray/releases')
respon = json.loads(respon.text)
print(respon)

#######################################################################
#                               new                                #
#######################################################################

url_template = 'https://{}.github.com/repos/' + repo + '/releases'
respon = requests.post(
    'https://api.github.com/repos/UIFV2ray/UIFV2ray/releases',
    json={
        'tag_name': tag,
        'name': name,
        'prerelease': False,
    },
    headers={
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token ' + TOKEN
    })
respon = json.loads(respon.text)
print(respon)
new_release_id = respon['id']


def UploadFile(release_id, file_path):
    upload_files = {'file': open(file_path, 'rb')}
    respon = requests.post(
        'https://api.github.com/repos/UIFV2ray/UIFV2ray/releases/%s/assets' %
        (release_id),
        files=upload_files,
        headers={
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/zip',
            'Authorization': 'token ' + TOKEN
        })
    respon = json.loads(respon.text)
    print(respon)


UploadFile(new_release_id, upload_file)
