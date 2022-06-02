#!/usr/bin/env python3

import requests
import argparse
import os
import sys
import pickle
from bs4 import BeautifulSoup
from datetime import datetime,timedelta,date
from time import sleep
from variables import token, pinproxy_url

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

parser = argparse.ArgumentParser(description='get word of the day from merriam-webster')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='suppress notifications')
args = parser.parse_args()

while True:
    url = 'https://www.merriam-webster.com/word-of-the-day'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    title = soup.find('div', class_='word-and-pronunciation').h1.text

    old_title = None
    if os.path.isfile('last_word/.last_word'):
        with open('last_word/.last_word', 'rb') as file:
            old_title = pickle.load(file)
    if old_title == title and not args.debug:
        wait_time = 15 * 60
        print(f"Word has not changed yet, retrying in {wait_time}s")
        sleep(wait_time)
        continue

    body = f"{soup.find('div', {'class': 'wod-definition-container'}).p.text}\n"
    body += '\n'.join(i.text for i in list(filter(lambda s: s.text.startswith("//"), soup.find('div', {'class': 'wod-definition-container'})('p'))))
    if not args.debug:
        print(f"Sending word: {title}")
        requests.post(pinproxy_url, json={"time":"A","meta":{"clocktime":{"hour":22,"minute":59},"notifyOnArrival":False},"layout":{"type":"genericPin","title":"Todays word:","body": body,"subtitle": title,"tinyIcon":"system://images/NEWS_EVENT"},"token": token})
    else:
      print(f"{title}\n{body}")

    with open('last_word/.last_word', 'wb') as file:
        pickle.dump(title, file, protocol=pickle.HIGHEST_PROTOCOL)
    break
  



