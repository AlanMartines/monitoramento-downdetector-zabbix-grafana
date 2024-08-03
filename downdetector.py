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
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

PARAMS = {
    'Relatórios de usuários indicam que não há problemas': 'success',
    'Relatórios de usuários indicam potenciais problemas': 'warning',
    'Relatórios de usuários indicam problemas': 'danger'
}

def request(dd_site):
    url = f"http://downdetector.com.br/fora-do-ar/{dd_site}/"
    scraper = cloudscraper.create_scraper()
    return scraper.get(url, headers={'User-Agent': random.choice(user_agent_list)})

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
