#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta,date
import argparse
from variables import token, address
from urllib.parse import quote_plus

class Bin:

  def __init__(self, name, lookup, date=None):
    self.name = name
    self.lookup = lookup
    self.date = date

  def get_date(self, soup):
    self.date = datetime.strptime(soup.find("h2", string=self.lookup).parent.div.text.strip(), '%A %d/%m/%Y')

  @property
  def format_date(self):
    return f"{self.date.strftime('%d/%m/%Y')}"


parser = argparse.ArgumentParser(description='checks bin collection days and sends notifications when they are close')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='suppress notifications')
parser.add_argument('-f', '--force', action='store_true', default=False, help='force notification')
args = parser.parse_args()


search_url= f'https://www.midlothian.gov.uk/site/scripts/directory_search.php?directoryID=35&keywords={quote_plus(address)}&search=Search'
soup = BeautifulSoup(requests.get(search_url).text, 'html.parser')
url = f'https://www.midlothian.gov.uk{soup.find("a", string=address).get("href")}'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')
bins = []
bins.append(Bin("recycling", "Next recycling collection"))
bins.append(Bin("grey", "Next grey bin collection"))
bins.append(Bin("brown", "Next brown bin collection"))
bins.append(Bin("food", "Next food bin collection"))


for b in bins:
  b.get_date(soup)
#  next_monday = date.today() + timedelta(days=-date.today().weekday(), weeks=1)
#  if next_monday == b.date.date():
  if (b.date.date() - date.today()).days <= 1 or args.force:
    if not args.debug:
        print(f"{b.lookup} is tomorrow, sending notification")
        requests.post("https://kennedn.com/pinproxy/ifttt", json={"time":"A","meta":{"clocktime":{"hour":23,"minute":59},"notifyOnArrival":True},"layout":{"type":"genericPin","title":"Bin Alert","body":f"{b.lookup} is due {b.format_date}","subtitle":f"{b.name.capitalize()} collection tomorrow","tinyIcon":"system://images/SCHEDULED_EVENT"},"token": f"{token}"})
    else:
        print(f"{b.lookup} is tomorrow!")
  else:
    print(f"{b.lookup} is on {b.format_date}")
  



