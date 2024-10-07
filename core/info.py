import requests,json,os,time,logging
from core.headers import headers
from urllib.parse import unquote, parse_qs
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    banner = r"""
 ▄▄▄       ██▀███ ▓██   ██▓ ▄▄▄     ▄▄▄█████▓ █    ██ ▒██   ██▒
▒████▄    ▓██ ▒ ██▒▒██  ██▒▒████▄   ▓  ██▒ ▓▒ ██  ▓██▒▒▒ █ █ ▒░
▒██  ▀█▄  ▓██ ░▄█ ▒ ▒██ ██░▒██  ▀█▄ ▒ ▓██░ ▒░▓██  ▒██░░░  █   ░
░██▄▄▄▄██ ▒██▀▀█▄   ░ ▐██▓░░██▄▄▄▄██░ ▓██▓ ░ ▓▓█  ░██░ ░ █ █ ▒ 
 ▓█   ▓██▒░██▓ ▒██▒ ░ ██▒▓░ ▓█   ▓██▒ ▒██▒ ░ ▒▒█████▓ ▒██▒ ▒██▒
 ▒▒   ▓▒█░░ ▒▓ ░▒▓░  ██▒▒▒  ▒▒   ▓▒█░ ▒ ░░   ░▒▓▒ ▒ ▒ ▒▒ ░ ░▓ ░
  ▒   ▒▒ ░  ░▒ ░ ▒░▓██ ░▒░   ▒   ▒▒ ░   ░    ░░▒░ ░ ░ ░░   ░▒ ░
  ░   ▒     ░░   ░ ▒ ▒ ░░    ░   ▒    ░       ░░░ ░ ░  ░    ░  
      ░  ░   ░     ░ ░           ░  ░           ░      ░    ░  
                   ░ ░                                                                                                                                                                                                                  
"""
    print(f"\033[92m{banner}")

def get_info(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    full_name = data.get('full_name', 'No name provided')
    coins = data.get('coins', 'No coins provided')
    energy = data.get('energy', 'No energy provided')
    return full_name, coins, energy

def get_fullname(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    full_name = data.get('full_name', 'No name provided')
    return full_name

def get_info_coin(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    coins = data.get('coins', 'No coins provided')
    return coins

def get_info_energy(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/profile"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    energy = data.get('energy', 'No energy provided')
    return energy

def get_user_dao(token, max_retries=3, initial_delay=1):
    url = (
        "https://app.production.tonxdao.app/api/v1/dao_users"
    )
    auth_headers = headers(token)
    for attempt in range(max_retries):
        try:
            response = requests.get(url=url, headers=auth_headers)
            response.raise_for_status()
            try:
                data = response.json()
                return data
            except json.JSONDecodeError as json_err:
                logger.error(f"JSON decode error: {json_err}")
                logger.debug(f"Raw response: {response.text}")
            
            if attempt == max_retries -1 :
                raise
        except RequestException as req_err:
            logger.error(f"Request Failed: {req_err}")
            
            if attempt == max_retries -1 :
                raise
        delay = initial_delay * (2 ** attempt)
        logger.info(f"Retrying in {delay} seconds...")
        time.sleep(delay)
    
    raise Exception("Max retries reached. Unable to get user DAO information.")

def get_token(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/centrifugo-token"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()["token"]
    return data

def get_username(token):
    tokens = open('data.txt').read().strip().split('\n')
    for data in tokens:
        return json.loads(parse_qs(data)['user'][0]).get('username', '<NOT SET>')

def get_daily_info(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/tasks/daily"
    )
    auth_headers = headers(token)
    response = requests.get(url=url, headers=auth_headers)
    data = response.json()
    is_available = data.get('is_available', 'No data provided')
    return is_available

def get_daily_claim(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/tasks/daily/claim"
    )
    auth_headers = headers(token)
    response = requests.post(url=url, headers=auth_headers)
    data = response.json()
    is_success = data.get('success', 'No data provided')
    return is_success

def get_tiktok_info(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/tasks/80/start"
    )
    auth_headers = headers(token)
    response = requests.post(url=url, headers=auth_headers)
    data = response.json()
    message = data.get('message')
    return message

def get_tiktok_claim(token):
    url = (
        "https://app.production.tonxdao.app/api/v1/tasks/80/claim"
    )
    auth_headers = headers(token)
    response = requests.post(url=url, headers=auth_headers)
    data = response.json()
    message = data.get('message')
    return message

def config(name, default):
    with open("config.json", 'r') as file:
        config = json.load(file)
        return config.get(name, default)