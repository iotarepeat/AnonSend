import csv
import json
import os
import pickle
import string
import urllib.request
from datetime import datetime
from hashlib import sha1
from random import shuffle
from zipfile import ZipFile

import bcrypt
import user_agents


def hashPassword(password):
    """
    - Hash a password using bcrypt
    - If password is blank (== '' ), do not hash
    :param password:
    :return: b_string
    """
    if password == '':
        return ''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def getQuestions():
    """
    Load questions from questions.json and return it
    :return: Dictionary of questions
    :rtype: dict
    """
    if not os.path.exists("questions.json"):
        print("WARNING: No questions.json found")
        return {"": ""}

    else:
        with open("questions.json", "r") as f:
            return json.load(f)


def verifyPassword(password, hashed):
    """
    Verify password, blank or hashed
    :rtype: bool
    :param password: 
    :param hashed: 
    :return: If the password is same as hash
    """
    if hashed == '':
        return password == ''
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def queryToCsv(query):
    """
    :param fname: The fileName
    :type query: QuerySet
    """
    header = ["os", "device_type", "browser", "country", "time_clicked"]
    with open("/tmp/csvData.csv", "w") as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(header)
        for row in query.values_list(*header):
            csvWriter.writerow(row)
    return "/tmp/csvData.csv"


def compress_to_zip(files):
    """
    Compress  multiple django uploaded files
    Returns suitable kwargs for UploadedFiles <django_class>
    :type files: List[<InMemoryFiles> or <TemporaryUploadedFiles>]
    :param files:
    :return:
    """

    # TODO: Fix bug where same files produce different hash
    zip_file = ZipFile('tmp.zip', "w")
    for f in files:
        zip_file.writestr(f.name, f.read())

    zip_file.close()
    try:
        return {"name": "anonSend.zip", "file": open('tmp.zip', 'rb'), "content_type": "application/zip",
                "size": os.path.getsize('tmp.zip'), "charset": "utf-8"}
    finally:
        os.remove('tmp.zip')


def get_analytics(meta):
    """
    Extracts various information from user-agent and ip-address

    From User-Agent:
        - OS
        - Device Type
        - Browser

    From Ip-Address:
        - Country
        - City
        - State
    :rtype: dict
    :type meta: dict
    :param meta: A django request.META dictionary
    :return: dict of extracted information
    """
    # Ip address
    try:
        ip_address = meta['REMOTE_ADDR']
        response = urllib.request.urlopen('https://ipapi.co/' + ip_address + "/json/")
        ip_info = json.loads(response.read().decode('utf-8'))
        country = ip_info["country"]
    except:
        country = "Unknown"
        region = "Unknown"
        city = "Unknown"

    # User Agent
    ua = user_agents.parse(meta.get('HTTP_USER_AGENT', ''))
    device_type = "Unknown"
    if ua.is_mobile:
        device_type = "Mobile"
    elif ua.is_tablet:
        device_type = "Tablet"
    elif ua.is_pc:
        device_type = "Personal Computer"

    return {"os": ua.os.family, "device_type": device_type, "browser": ua.browser.family,
            "country": country, }


def get_hash(file_stream):
    """
    Return SHA1 hash of given file
    :rtype: str
    :param file_stream: A django uploaded file that has chunks method
    :return: Hexdigest of given file
    """
    hash_algorithm = sha1()
    for chunk in file_stream.chunks():
        hash_algorithm.update(chunk)
    return hash_algorithm.hexdigest()


def gen_base62(name):
    """
    Create a base62 (ASCII letters and numbers) dict and picklize it
    The dict is shuffled to increase entropy
    :type name: str
    :param name:name of file to save as
    """
    base62 = list(string.digits + string.ascii_letters)
    shuffle(base62)
    dict_62 = {str(i).zfill(2): base62[i] for i in range(62)}
    for i in range(62, 100):
        dict_62[str(i)] = base62[i // 10] + base62[i % 10]
    with open(name, "wb") as f:
        pickle.dump(dict_62, f)


def gen_analytic_link():
    """
    Generate and return  link
    - Read base62_analytic_dict, create if does not exist
    - Encode current timestamp as bas62
    - Shuffle base62 encoded timestamp
    :rtype: str
    :return: analytic_link
    """
    name = "base62_analytic_dict.pkl"
    if not os.path.exists(name):
        gen_base62(name)
    with open(name, 'rb') as f:
        base62 = pickle.load(f)
    current_timestamp = str(datetime.timestamp(datetime.now())).replace(".", "")
    link = [base62[current_timestamp[i:i + 2].zfill(2)] for i in range(0, len(current_timestamp), 2)]
    shuffle(link)
    link = "".join(link)
    return link


def gen_link():
    """
    TODO: Add a random character to links to remove collision for same time
    Generate and return public link
    - Read base62_public_link, create if does not exist
    - Encode current timestamp as bas62
    - Shuffle base62 encoded timestamp
    :rtype: str
    :return: public_link
    """
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
