#!/usr/bin/python3

import sys
import ssl
import random
import re
from bs4 import BeautifulSoup

# Lista de user agents para simular diferentes navegadores
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

# Determina o melhor crawler baseado na versão do SSL
if ssl.OPENSSL_VERSION_INFO[0] >= 1 and ssl.OPENSSL_VERSION_INFO[1] >= 1 and ssl.OPENSSL_VERSION_INFO[2] >= 1:
    import cloudscraper
    craw = "cloudscraper"
else:
    import requests
    craw = "requests"

def request(dd_site):
    url = f"https://downdetector.com.br/fora-do-ar/{dd_site}/"
    
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        if craw == "cloudscraper":
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url)
        else:
            response = requests.get(url, headers=headers)
        
        response.raise_for_status()  # Levanta um erro para códigos de status ruins
        return response
    except Exception as e:
        # print(f"Erro ao buscar URL: {e}")
        print(0)
        sys.exit()

def parse_result(status_text):
    status_number = {'success': 1, 'warning': 2, 'danger': 3}.get(status_text.strip(), 0)
    print(status_number)
    sys.exit()

def main():
    if len(sys.argv) < 2:
        # print("Informe o site que gostaria de verificar")
        print(0)
        sys.exit()
    
    site = sys.argv[1]
    response = request(site)

    try:
        bs = BeautifulSoup(response.text, 'html.parser')
        # Busca pelo elemento <span> que contém o status
        status_element = bs.find("span", class_=re.compile("color-(success|warning|danger)"))
        
        if status_element:
            status_class = status_element['class'][0]
            status = status_class.split('-')[1]  # Extrai o status (success, warning, danger)
            parse_result(status)

        # Failover caso o método acima falhe
        failover = re.compile(r".*status: '(.*)',.*", re.MULTILINE)
        failover_status = failover.findall(response.text)
        if failover_status:
            parse_result(failover_status.pop())
        else:
            print(0)
            sys.exit()
    except Exception as err:
        # print(f"Erro ao processar a resposta: {err}")
        print(0)
        sys.exit()

if __name__ == '__main__':
    main()
