import requests
import time
import io
from random import randrange


def get_file_lines(fname):
    with open(fname) as p:
        return p.read().splitlines()


def http_sleeper(r, url):
    stuck = 0
    if stuck < 4:
        ran_minutes = randrange(1, 5)
        print('Response: ' + str(r.status_code))
        print('F*ck you google, sleeping for : ' + str(ran_minutes / 60) + ' minutes...')
        time.sleep(ran_minutes)
        # Prevent adding a bad r.
        try:
            return requests.get(url)

        except requests.exceptions.ConnectionError:
            print('Connection refused')
            stuck += 1
    else:
        ran_minutes = randrange(2040, 7200)
        print('Response: ' + str(r.status_code))
        print('We seem to be stuck, taking a long nap for ' + str(ran_minutes / 60) + ' minutes...')
        print('Stuck status: ' + str(stuck))
        time.sleep(ran_minutes)
        try:
            return requests.get(url)

        except requests.exceptions.ConnectionError:
            print('Connection refused')


def write_vocab_to_file(filename, vocab):
    i = 0
    while i < len(vocab):
        with io.open(filename, 'a',
                     encoding='utf-8') as data:
            tmp = str(vocab[i:i + 1]).decode('unicode-escape')
            data.write(tmp.replace('[u'', '').replace('']', '') + '\n')
            i += 1
