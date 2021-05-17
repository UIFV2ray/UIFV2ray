#!/usr/bin/env python3

import json
import os
import datetime
import sys

from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')

NOW_TIME = str(int(datetime.datetime.now().timestamp()))
repo = 'UIFV2ray/UIFV2ray'
tag = NOW_TIME
upload_file = BASE_DIR + '/runtime/linux.zip'

TOKEN = os.getenv('GITHUB_TOKEN', default='')

url_template = 'https://{}.github.com/repos/' + repo + '/releases'

# Create.
_json = json.loads(
    urlopen(
        Request(
            url_template.format('api'),
            json.dumps({
                'tag_name': tag,
                'name': tag,
                'prerelease': True,
            }).encode(),
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token ' + TOKEN,
            },
        )).read().decode())
release_id = _json['id']

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
