import sys
import ssl
import re
import random
from bs4 import BeautifulSoup
import cloudscraper

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
    'Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
    'Safari/537.36',
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
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; '
    '.NET CLR 3.5.30729) '
]

def request(dd_site):
    scraper = cloudscraper.create_scraper()
    return scraper.get(dd_site, headers={'User-Agent': random.choice(user_agent_list)})

# Função para obter o link da imagem do logo de um serviço
def get_logo(service_id):
    site = f"https://downdetector.com.br/fora-do-ar/{service_id}/"
    response = request(site)
    
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tag = soup.find("img", {"class": "img-fluid"})
            if img_tag and 'src' in img_tag.attrs:
                logo_url = img_tag['src']
                print("Logo obtida com sucesso.")
                return logo_url
            else:
                return None
        except Exception as err:
            print(f"Erro ao obter a logo para {service_id}: {err}")
            return None
    else:
        print(f"Falha ao acessar a página para {service_id}. Status code: {response.status_code}")
        return None

def get_service():
    # Faz a requisição para a página
    site = "https://downdetector.com.br/fora-do-ar/"
    response = request(site)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200 or response.status_code == 404:
        # Faz o parsing do HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra todos os elementos <li> na página que contém os serviços
        li_elements = soup.find_all('li')
        
        # Cria uma lista para armazenar os serviços fora do ar
        services = []
    
        # Itera sobre todos os elementos <li> encontrados
        for li in li_elements:
            # Encontra o elemento <a> dentro do <li> (se existir)
            a_tag = li.find('a')
            if a_tag:
                href = a_tag.get('href')
                if 'fora-do-ar' in href:
                    name = a_tag.text.strip()
                    service_id = href.split('/')[-2]
                    services.append(f"1;{service_id};{name}")
                    # logo = get_logo(service_id)
    
        # Escreve a lista de serviços fora do ar em um arquivo
        with open("downdetectorlist.list", "w", encoding="utf-8") as f:
            for service in services:
                f.write(service + "\n")
    
        # Imprime a lista de serviços fora do ar no console
        print("\nServiços:\n")
        for service in services:
            print(service)
    
        print("\nLista de serviços fora do ar gerada com sucesso.")
    else:
        print("Falha ao obter a página. Status code:", response.status_code)

if __name__ == "__main__":
    get_service()