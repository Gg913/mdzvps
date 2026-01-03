import os
import sys
import httpx
from colorama import Fore, init
init(autoreset=True)

# Definição das cores para o console
fr = Fore.RED
fg = Fore.GREEN
fy = Fore.YELLOW
fw = Fore.WHITE
fre = Fore.RESET

# Lista completa de URLs para download de proxies
list = [
    # Proxies HTTP
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt',
    'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
    'https://api.openproxylist.xyz/http.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous',
    'http://worm.rip/http.txt',
    'https://proxyspace.pro/http.txt',
    'https://multiproxy.org/txt_all/proxy.txt',
    'https://proxy-spider.com/api/proxies.example.txt',

    # Proxies HTTPS
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/https.txt',
    'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/https.txt',
    'https://proxyspace.pro/https.txt',
    'https://openproxylist.xyz/https.txt',

    # Proxies SOCKS4
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
    'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt',
    'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt',
    'https://proxyspace.pro/socks4.txt',
    'https://openproxylist.xyz/socks4.txt',
    'https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt',

    # Proxies SOCKS5
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
    'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt',
    'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt',
    'https://proxyspace.pro/socks5.txt',
    'https://openproxylist.xyz/socks5.txt',
    'https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt',

    # Outras Fontes
    'https://www.proxydocker.com/en/proxylist/download?email=noshare&country=all&city=all&port=all&type=all&anonymity=all&state=all&need=all',
    'https://api.proxyscrape.com/v2/?request=displayproxies',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http',
]  

if __name__ == "__main__":
    file = "proxy.txt"
    
    try:
        # Se o arquivo já existir, remove e informa o usuário
        if os.path.isfile(file):
            os.system('cls' if os.name == 'nt' else 'clear')
            os.remove(file)
            print("{}O arquivo {} já existe!\n{}Baixando uma nova lista de {}!\n".format(fr, file, fy, file))
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("{}O arquivo {} não foi encontrado.\n{}Baixando uma nova lista de {}!\n".format(fy, file, fg, file))

        # Abre o arquivo para escrita e baixa os proxies de cada URL
        with open(file, 'a') as data:
            for proxy_url in list:
                try:
                    response = httpx.get(proxy_url, timeout=10)
                    response.raise_for_status()  # Lança um erro para códigos de status HTTP 4xx/5xx
                    data.write(response.text + '\n')
                    print(f" -| {fg}Obtendo{fre}: {fg}{proxy_url}{fre}")
                except httpx.HTTPError as e:
                    print(f" -| {fr}Erro ao obter{fre}: {fr}{proxy_url}{fre} - {e}")
                except Exception as e:
                    print(f" -| {fr}Erro inesperado com{fre}: {fr}{proxy_url}{fre} - {e}")
    
        # Conta e exibe o total de proxies baixados
        with open(file, 'r') as count:
            total = sum(1 for line in count if line.strip())
        print("\n{}( {}{} {}) {} proxies foram baixados com sucesso.".format(fw, fy, total, fw, fg))
    
    except Exception as e:
        print(f"\n{fr}Ocorreu um erro geral: {e}{fre}")
        sys.exit(1)
