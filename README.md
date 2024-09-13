# Monitoramento Downdetector
 Visualização em tempo real de problemas e falhas em todos os tipos de serviço. Está tendo problemas? Ajudamos você a descobrir o que há de errado.

### Requisitos
```
Python 3
beautifulsoup4
cloudscraper
requests
openssl 1.1.1
```

### Uso
```sh
./downdetector.py {nome site}
./downdetector.py whatsapp
```

#### Debian /Ubuntu ####
```sh
apt install python3-pip
pip3 install bs4
pip3 install requests
pip3 install cloudscraper
pip install six
pip install --upgrade urllib3 chardet requests
```

Caso já tenha o pip instalado e queira instalar as dependencias rode:

```sh
pip3 install requirements.txt
```

Copie os arquivos downdetectorDiscovery.py downdetectorlist.list downdetector.py para ```/usr/lib/zabbix/externalscripts```, altere suas permissões para o usuários zabbix. 

```sh
chown zabbix. /usr/lib/zabbix/externalscripts/downdetector*
chmod a+x /usr/lib/zabbix/externalscripts/downdetector*.py
```

## Discovery/Auto Configuração

Edite o arquivo downdetectorlist.list e altere para 1 os sites/host que deseja monitorar.

#### downdetectordiscoverylist.list
```sh
1 ATIVO
0 INATIVO

0;caixa;Caixa Econômica Federal
1;caixa;TIM
```

## ⚠️ Aviso Importante: Limitação nas Consultas ao Downdetector

Devido a várias solicitações consecutivas enviadas via script, o site Downdetector recusou as consultas subsequentes, impossibilitando a captura do status dos serviços monitorados.

Recomendamos as seguintes ações:
- Reduzir a frequência de consultas automatizadas.
- Considerar métodos alternativos de monitoramento de status.
- Revisar scripts para evitar bloqueios futuros.
