#!/usr/bin/python3
#########################################
#                                       #
# Author: Gabriel Padilha               #
# Email: gabrielvargaspadilha@gmail.com #
#                                       #
#########################################

import sys
import ssl
import re
import random
from bs4 import BeautifulSoup
import requests
import cloudscraper

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

PARAMS = {
    'Relatórios de usuários indicam que não há problemas': 'success',
    'Relatórios de usuários indicam potenciais problemas': 'warning',
    'Relatórios de usuários indicam problemas': 'danger'
}

def request(dd_site):
    url = f"http://downdetector.com.br/fora-do-ar/{dd_site}/"
    scraper = cloudscraper.create_scraper()
    proxy = random.choice(proxy_list)
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    # response = scraper.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})
    response = scraper.get(url, headers=headers)
    return response

def parse_result(status_text):
    status_text = status_text.strip()
    status_number = {'success': 1, 'warning': 2, 'danger': 3}.get(status_text, 0)
    print(status_number)
    sys.exit()

def main():
    if len(sys.argv) < 2:
        print("Informe o site que gostaria de verificar")
        sys.exit(1)
    site = sys.argv[1]

    response = request(site)

    if response.status_code != 200:
        print(0)
        sys.exit()

    try:
        bs = BeautifulSoup(response.text, 'html.parser')
        data_parse = bs.find("div", {"class": "entry-title"})
        status = data_parse.text.strip() if data_parse else None
        result = None

        if not status:
            raise ValueError("Status não encontrado.")

        for param, value in PARAMS.items():
            if re.compile(f"{param}.*").match(status):
                result = value

        if not result:
            raise ValueError("Nenhum resultado correspondente encontrado.")
        
        parse_result(result)
    except Exception as err:
        failover = re.compile(r".*status: '(.*)',.*", re.MULTILINE)
        failover_status = failover.findall(response.text)
        if failover_status:
            parse_result(failover_status.pop())
        else:
            print(0)
            sys.exit()

if __name__ == '__main__':
    main()
