import os
import pickle
import string
from datetime import datetime
from hashlib import sha1
from random import shuffle


def get_hash(file_stream):
    hash_algorithm = sha1()
    for chunk in file_stream.chunks():
        hash_algorithm.update(chunk)
    return hash_algorithm.hexdigest()


def gen_base62():
    base62 = list(string.digits + string.ascii_letters)
    shuffle(base62)
    dict_62 = {str(i).zfill(2): base62[i] for i in range(62)}
    for i in range(62, 100):
        dict_62[str(i)] = base62[i // 10] + base62[i % 10]
    with open("base62_dict.pkl", "wb") as f:
        pickle.dump(dict_62, f)


def gen_analytic_link():
    if not os.path.exists("base62_dict.pkl"):
        gen_base62()
    with open("base62_dict.pkl", 'rb') as f:
        base62 = pickle.load(f)
    current_timestamp = str(datetime.timestamp(datetime.now())).replace(".", "")
    shuffle(list(current_timestamp))
    current_timestamp = "".join(current_timestamp)
    link = [base62[current_timestamp[i:i + 2].zfill(2)] for i in range(0, len(current_timestamp), 2)]
    shuffle(link)
    link = "".join(link)
    return link


def gen_link():
    if not os.path.exists("base62_dict.pkl"):
        gen_base62()
    with open("base62_dict.pkl", 'rb') as f:
        base62 = pickle.load(f)
    current_timestamp = str(datetime.timestamp(datetime.now())).replace(".", "")
    link = [base62[current_timestamp[i:i + 2].zfill(2)] for i in range(0, len(current_timestamp), 2)]
    shuffle(link)
    link = "".join(link)
    return link
