import json
import os
import pickle
import string
import urllib.request
from datetime import datetime
from hashlib import sha1
from random import shuffle
from zipfile import ZipFile

import user_agents


def compress_to_zip(files):
    zip_file = ZipFile('tmp.zip', "w")
    for f in files:
        zip_file.writestr(f.name, f.read())

    zip_file.close()
    try:
        return {"name": "anonSend.zip", "file": open('tmp.zip', 'rb'), "content_type": "application/zip",
                "size": os.path.getsize("/tmp/anonSend.zip"), "charset": "utf-8"}
    finally:
        os.remove('tmp.zip')


def get_analytics(request):
    # Ip address
    try:
        ip_address = request.META['REMOTE_ADDR']
        response = urllib.request.urlopen('http://ip-api.com/json/' + ip_address)
        ip_info = json.loads(response.read())
        country = ip_info["country"]
        region = ip_info["regionName"]
        city = ip_info["city"]
    except KeyError or urllib.request.HTTPError:
        country = "Unknown"
        region = "Unknown"
        city = "Unknown"

    # User Agent
    ua = user_agents.parse(request.META.get('HTTP_USER_AGENT', ''))
    device_type = "Unknown"
    if ua.is_mobile:
        device_type = "Mobile"
    elif ua.is_tablet:
        device_type = "Tablet"
    elif ua.is_pc:
        device_type = "Personal Computer"

    return {"os": ua.os.family, "device_type": device_type, "browser": ua.browser.family, "region": region,
            "country": country, "city": city}


def get_hash(file_stream):
    hash_algorithm = sha1()
    for chunk in file_stream.chunks():
        hash_algorithm.update(chunk)
    return hash_algorithm.hexdigest()


def gen_base62(name):
    base62 = list(string.digits + string.ascii_letters)
    shuffle(base62)
    dict_62 = {str(i).zfill(2): base62[i] for i in range(62)}
    for i in range(62, 100):
        dict_62[str(i)] = base62[i // 10] + base62[i % 10]
    with open(name, "wb") as f:
        pickle.dump(dict_62, f)


def gen_analytic_link():
    name = "base62_analytic_dict.pkl"
    if not os.path.exists(name):
        gen_base62(name)
    with open(name, 'rb') as f:
        base62 = pickle.load(f)
    current_timestamp = str(datetime.timestamp(datetime.now())).replace(".", "")
    shuffle(list(current_timestamp))
    current_timestamp = "".join(current_timestamp)
    link = [base62[current_timestamp[i:i + 2].zfill(2)] for i in range(0, len(current_timestamp), 2)]
    shuffle(link)
    link = "".join(link)
    return link


def gen_link():
    name = "base62_public_dict.pkl"
    if not os.path.exists(name):
        gen_base62(name)
    with open(name, 'rb') as f:
        base62 = pickle.load(f)
    current_timestamp = str(datetime.timestamp(datetime.now())).replace(".", "")
    link = [base62[current_timestamp[i:i + 2].zfill(2)] for i in range(0, len(current_timestamp), 2)]
    shuffle(link)
    link = "".join(link)
    return link
