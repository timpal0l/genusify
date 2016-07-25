import requests
import misc
import os
import io
import re

from bs4 import BeautifulSoup
from langdetect import detect


def get_text():
    print('Starts scraping text from blogs..')
    blogs_unvisited = misc.get_file_lines('blogs')
    path = os.path.expanduser('~') + '/PycharmProjects/web_crawler/texts/'
    currentblog = 0

    while len(blogs_unvisited) > 0:
        blog = blogs_unvisited.pop().split()
        url = blog[0].replace('[u'', '').replace('',', '')
        gender = blog[1].replace('u'', '').replace('']', '')

        try:
            r = requests.get(url + '/search?max-results=1000')
        except requests.exceptions.ConnectionError as e:
            print(e)

        print(str(url) + ' ' + str(r))

        while r.status_code == 503:
            r = misc.http_sleeper(r, url)

        soup = BeautifulSoup(r.content, 'html.parser')

        # writes blog texts to file
        for postbody in soup.find_all('div', {'class': 'post-body entry-content'}):
            with io.open(path + gender.lower() + '_' + str(currentblog), 'a',
                         encoding='utf-8') as data:
                tmp = prep_div(postbody.text)
                # noinspection PyBroadException
                try:
                    if detect(tmp) == 'sv':
                        data.write(tmp)
                        print(tmp)

                except Exception:
                    print('No language features in <div>.. \n')
        currentblog += 1
    remove_empty_files(path)


def prep_div(text):
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    #    text = text.replace('\xc2\xa0', '')
    return text


def remove_empty_files(path):
    print('\nRemoving empty blogs..')
    for filename in os.listdir(path):
        if os.stat(path + filename).st_size < 1000:
            os.remove(path + filename)
