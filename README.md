# pebble_timeline_tools

This repository contains scripts that I have constructed to push different things to my pebble timeline. Currently the following project(s) are published here:

- Word of the day (`wod.py`)

# Word of the day

Word of the day scrapes the merriam-webster word of the day webpage, then constructs and sends a RESTful call to a given [timeline-proxy](https://github.com/Willow-Systems/ws-pebble-timeline-services). This will then display as a timeline notification on your pebble device.

## Setup

A token is required to use this tool. The token is an identifier for your specific user / app on the rebble web services. There is a tool on the Rebble store written by the formidable [Will0](https://github.com/Willow-Systems) that allows you to easily generate this token. Aptly named [Generate Token](https://apps.rebble.io/en_US/application/5d9ac26dc393f54d6b5f5445).

You can then populate `variables.py` with this token:
```python
token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
pinproxy_url = 'https://willow.systems/pinproxy-ifttt/'
```

pinproxy_url can also be replaced with an alternative timeline-proxy url if desired.

To run `wod.py`, `requests` and `bs4` need installed as pre-requisites. This can be achieved by doing:
```bash
python3 -m pip install requests bs4
```

After which you can invoke wod by simply running:
```bash
python3 wod.py
```

## Usage

```bash
usage: wod.py [-h] [-d]

get word of the day from merriam-webster

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  suppress notifications
```

## Service files

Some example systemd service files are included in this repository under `/systemd`. These facilitate running the wod script on a daily schedule, specifically on systems that operate on systemd.