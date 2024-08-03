#!/usr/bin/python3

import sys
import ssl
import re
import random
from bs4 import BeautifulSoup
if ssl.OPENSSL_VERSION_INFO[0] < 1 or ssl.OPENSSL_VERSION_INFO[1] < 1 or ssl.OPENSSL_VERSION_INFO[2] < 1:
    user_agent_list = [
				# Chrome
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
				'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
				# Firefox
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
				'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
				# Safari
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
				'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
				# Edge
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
				# Opera
				'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172',
		]

    proxy_list = [
				'http://51.79.23.17:8050',
				'http://187.94.220.85:8080',
				'http://189.51.123.7:80',
				'http://187.109.22.46:8080',
				'http://189.50.9.33:8080',
				'http://179.48.11.6:8085',
				'http://201.20.65.234:9896',
				'http://138.59.20.48:8090',
				'http://45.6.203.224:8080',
				'http://179.106.20.149:9090',
				'http://189.124.85.225:7171',
				'http://201.91.82.155:3128',
				'http://177.70.174.103:8080',
				'http://177.190.189.16:44443',
				'http://191.7.8.246:80'
		]
    import requests
    craw = "requests"
else:
    import cloudscraper
    craw = "cloudscraper"


def request(dd_site):
    url = "https://downdetector.com.br/fora-do-ar/{}/".format(dd_site)
    if not craw:
        print(0)
        exit()
    elif craw == "cloudscraper":
        scraper = cloudscraper.create_scraper()
        return scraper.get(url)
    else:
        return requests.get(url, headers={'User-Agent': random.choice(user_agent_list)})


def parse_result(status_text):
    status_text = status_text.strip()
    if status_text == 'success':
        status_number = 1
    elif status_text == 'warning':
        status_number = 2
    elif status_text == 'danger':
        status_number = 3
    else:
        status_number = 0
    print(status_number)
    exit()


if len(sys.argv) < 2:
    print("Informe o site que gostaria de verificar")
    sys.exit(1)
site = sys.argv[1]

response = request(site)

if response.status_code != 200:
    print(0)
    exit()

bs = BeautifulSoup(response.text, 'html.parser')
dataParse = bs.find("div", {"class": "entry-title"})
status = dataParse.attrs["class"][2].split('-')[1]

if status in ['success', 'warning', 'danger']:
    parse_result(status)
else:
    failover = re.compile(".*status: '(.*)',.*", re.MULTILINE)
    failover_status = failover.findall(response.text).pop()
    parse_result(failover_status)