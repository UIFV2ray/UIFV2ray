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
release_id = respon['id']

quit()
# Upload.
with open(upload_file, 'br') as myfile:
    content = myfile.read()

_json = json.loads(urlopen(Request(
    url_template.format('uploads') + '/' + str(release_id) + '/assets?' \
      + urlencode({'name': os.path.split(upload_file)[1]}),
    content,
    headers={
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token ' + TOKEN,
        'Content-Type': 'application/zip',
    },
)).read().decode())
