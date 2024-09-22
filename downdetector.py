#!/usr/bin/python3

import sys
import ssl
import re
import random
from bs4 import BeautifulSoup
import requests
import cloudscraper

# Lista de User-Agents para rotação aleatória
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

# # Mapeamento dos textos de status para valores específicos
# PARAMS = {
#     'Relatos de usuários indicam que não há problemas': 'success',
#     'Relatos de usuários indicam potenciais problemas': 'warning',
#     'Relatos de usuários indicam problemas': 'danger'
# }

def request(dd_site):
    # URL do Downdetector para o site alvo
    url = f"http://downdetector.com.br/fora-do-ar/{dd_site}/"
    scraper = cloudscraper.create_scraper()
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    # Faz a requisição à página do site no Downdetector
    response = scraper.get(url, headers=headers)
    return response

def parse_result(status_text):
    # Função para traduzir o status_text para um número de status e imprimir
    status_text = status_text.strip()
    status_number = {'success': 1, 'warning': 2, 'danger': 3}.get(status_text, 0)
    print(status_number)
    sys.exit()

def main():
    if len(sys.argv) < 2:
        print("Informe o site que gostaria de verificar")
        sys.exit(1)
    site = sys.argv[1]

    # Realiza a requisição
    response = request(site)

    if response.status_code != 200:
        # print(f"Erro {response.status_code}")
        print(0)
        sys.exit()

    try:
        # Faz a análise do HTML retornado
        bs = BeautifulSoup(response.text, 'html.parser')

        # Extrai o conteúdo do título onde contém a informação de status
        status_element = bs.find("h2", {"class": "entry-title"})
        if not status_element:
            raise ValueError("Status não encontrado no HTML.")

        # Extrai o texto do span com as classes de status (warning, danger, etc.)
        status_span = status_element.find("span", class_=re.compile(r"color-(success|warning|danger)"))
        if not status_span:
            raise ValueError("Nenhum status relevante encontrado.")

        status_class = status_span['class'][0]  # Pega a classe do span (ex: color-warning)
        status_type = status_class.split('-')[1]  # Extrai o tipo de status (success, warning, danger)

        # Transforma o status em texto correspondente (success, warning, danger)
        parse_result(status_type)

    except Exception as err:
        # Tenta pegar o status a partir de um texto secundário no conteúdo
        failover = re.compile(r".*status: '(.*)',.*", re.MULTILINE)
        failover_status = failover.findall(response.text)
        if failover_status:
            parse_result(failover_status.pop())
        else:
            # print(f"Erro: {err}")
            print(0)
            sys.exit()

if __name__ == '__main__':
    main()
