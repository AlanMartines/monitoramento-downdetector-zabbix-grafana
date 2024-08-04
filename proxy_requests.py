from lxml.html import fromstring
import requests
import random
import json

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    http_proxies = []
    https_proxies = []
    
    # Itera sobre cada linha da tabela de proxies
    for row in parser.xpath('//tbody/tr')[:299]:  # 299 proxies no máximo
        # Obtém o IP
        ip = row.xpath('.//td[1]/text()')
        # Obtém a porta
        port = row.xpath('.//td[2]/text()')
        # Verifica se suporta HTTPS
        https_support = row.xpath('.//td[7]/text()')
        
        # Certifica-se de que todos os elementos estão presentes
        if ip and port and https_support:
            ip = ip[0].strip()
            port = port[0].strip()
            https_support = https_support[0].strip().lower() == 'yes'
            
            # Define o protocolo
            protocol = 'https' if https_support else 'http'
            
            # Cria a string de proxy
            proxy = f"{protocol}//{ip}:{port}"
            
            # Adiciona ao conjunto apropriado
            if https_support:
                https_proxies.append(proxy)
            else:
                http_proxies.append(proxy)
            
    # Adiciona o proxy ao conjunto
    proxiesList = {
				'http': http_proxies,
				'https': https_proxies,  # Use o mesmo proxy para HTTPS, se necessário
		}
    
    return proxiesList

try:
    proxies = get_proxies()
    print(proxies)
    url = 'https://httpbin.org/ip'
    response = requests.get(url, timeout=10)
    print(response.json())
except:
    print ("ERROR")
    
