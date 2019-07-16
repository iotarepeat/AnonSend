import string
from hashlib import sha1
from random import choices, randint


def get_hash(file_stream):
    hash_algo = sha1()
    for chunk in file_stream.chunks():
        hash_algo.update(chunk)
    return hash_algo.hexdigest()


def gen_link(a=6, b=12):
    base62_list = list(string.digits + string.ascii_letters)
    return ''.join(choices(base62_list, k=randint(a, b)))
