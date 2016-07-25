import requests
import time
import misc

from bs4 import BeautifulSoup
from random import randrange


# Gets and stores all profile url's, in a file.
def get_profiles(maxpages):
    print('Starts scraping for profiles..')
    profiles = open('profiles', 'w')
    base_url = 'https://www.blogger.com/profile-find.g?t=l&loc0=SE&start='
    currentpage = 0

    while currentpage <= maxpages:
        url = base_url + str(currentpage)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        for link in soup.select('h2 a[href]'):
            profiles.write(link.get('href') + '\n')
            currentpage += 1
        print(str(r.status_code) + ' ' + str(url))

    profiles.close()
    print('Profiles scraping complete..')


# Gets and stores the first blog url from a profile, in a file.
def get_blog():
    print('Starts scraping for blogs..')
    profiles_unvisited = misc.get_file_lines('profiles')
    blogs = open('blogs', 'w')
    base_url = 'https://www.blogger.com/profile/'
    currentblog = 0

    while len(profiles_unvisited) > 0:
        currentprofile = profiles_unvisited.pop().rsplit('/', 1)[-1]
        url = base_url + currentprofile
        profile = []

        # decrease traffic, prevent 503 error
        ran_seconds = randrange(0, 5)
        time.sleep(ran_seconds)
        r = requests.get(url)

        while r.status_code >= 400:
            r = misc.http_sleeper(r, url)

        soup = BeautifulSoup(r.content, 'html.parser')
        user_single_blog = soup.find('span', {'dir': 'ltr'})

        # Adds url
        if user_single_blog is not None:
            try:
                blog_url = user_single_blog.find('a').get('href')
                profile.append(blog_url)
            except AttributeError:
                profile.append('https://support.google.com/blogger/')
                'Wierd site'
        else:
            profile.append('https://support.google.com/blogger/')

        # Adds gender
        for table in soup.findAll('table'):
            gender_tmp = table.find('td')
            if gender_tmp is not None:
                gender = gender_tmp.text
            else:
                gender = 'None'

            if gender != ('MALE' or 'man') and gender != ('FEMALE' or 'kvinna'):
                profile.append('None')
            else:
                profile.append(gender)

        # Only store informative blogs (valid url, and contains gender)

        if profile[0] == 'https://support.google.com/blogger/' or profile[1] == 'None':
            print('X ' + str(profile))
        else:
            blogs.write(str(profile) + '\n')
            currentblog += 1
            print(str(currentblog) + ' ' + str(profile))

    blogs.close()
    print('Blogs scraping complete..')
