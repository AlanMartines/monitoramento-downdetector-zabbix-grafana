from lxml.html import fromstring
import requests
import random

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
            proxy = f"{protocol}://{ip}:{port}"
            
            # Adiciona ao conjunto apropriado
            if https_support:
                https_proxies.append(proxy)
            else:
                http_proxies.append(proxy)
    
    return http_proxies, https_proxies

def fetch_with_proxy(url, proxies_list, headers):
    for attempt in range(5):  # Tenta até 5 vezes
        if not proxies_list:
            print("Nenhum proxy disponível.")
            return None
        # Escolhe um proxy aleatório
        proxy = random.choice(proxies_list)
        proxies = {'http': proxy, 'https': proxy}
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt+1} falhou com o proxy {proxy}. Erro: {e}")
            # Remove o proxy da lista se falhar
            proxies_list.remove(proxy)
    print("Falhou em todas as tentativas.")
    return None

# Testando a função
url = 'https://api.myip.com'  # Troque para 'http://api.myip.com' se quiser usar HTTP
headers = {
    'User-Agent': random.choice(user_agent_list),
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1'
}

http_proxies, https_proxies = get_proxies()
result = fetch_with_proxy(url, https_proxies, headers)

if result:
    print("Resultado:", result)
else:
    print("Não foi possível obter uma resposta válida com os proxies disponíveis.")
