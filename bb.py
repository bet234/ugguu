import random
import requests
import time
import urllib.parse
import json
import base64
import socket
from datetime import datetime, timedelta
import secrets
from urllib.parse import parse_qs, unquote
from colorama import Fore, Style, init
from tabulate import tabulate

# Khởi tạo colorama
init(autoreset=True)

def load_credentials():
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("Không tìm thấy file query_id.txt.")
        return []
    except Exception as e:
        print(f"Đã xảy ra lỗi khi tải query: {e}")
        return []

def print_(word, color=Fore.WHITE, style=Style.NORMAL):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{Fore.BLUE}{now}{Style.RESET_ALL}] {color}{style}{word}{Style.RESET_ALL}")

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'priority': 'u=1, i',
    'Origin': 'https://www.yescoin.gold',
    'Referer': 'https://www.yescoin.gold/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
}

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Chỉ số nằm ngoài phạm vi"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

def parse_and_reconstruct(url_encoded_string):
    parsed_data = urllib.parse.parse_qs(url_encoded_string)
    user_data_encoded = parsed_data.get('user', [None])[0]
    if user_data_encoded:
        user_data_json = urllib.parse.unquote(user_data_encoded)
    else:
        user_data_json = None
    reconstructed_string = f"user={user_data_json}"
    for key, value in parsed_data.items():
        if key != 'user':
            reconstructed_string += f"&{key}={value[0]}"
    return reconstructed_string

def generate_random_hex(length=32):
    return secrets.token_hex(length // 2)

def login(query, useragent):
    url = 'https://api-backend.yescoin.gold/user/login'
    headers['User-Agent'] = useragent
    payload = {
        'code': f'{query}'
    }
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getgameinfo(token, useragent):
    url = 'https://api-backend.yescoin.gold/game/getGameInfo'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getaccountinfo(token, useragent):
    url = 'https://api-backend.yescoin.gold/account/getAccountInfo'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getspecialboxreloadpage(token, useragent):
    url = 'https://api-backend.yescoin.gold/game/specialBoxReloadPage'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getspecialboxinfo(token, useragent):
    url = 'https://api-backend.yescoin.gold/game/getSpecialBoxInfo'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getacccountbuildinfo(token, useragent):
    url = 'https://api-backend.yescoin.gold/build/getAccountBuildInfo'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def collectCoin(token, useragent, count):
    url = 'https://api-backend.yescoin.gold/game/collectCoin'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers, json=count)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getspecialbox(token, useragent):
    url = 'https://api-backend.yescoin.gold/game/recoverSpecialBox'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getcoinpool(token, useragent):
    url = 'https://api-backend.yescoin.gold/game/recoverCoinPool'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def collectspecialbox(token, useragent, payload):
    url = 'https://api-backend.yescoin.gold/game/collectSpecialBoxCoin'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def getwallet(token, useragent):
    url = 'https://api-backend.yescoin.gold/wallet/getWallet'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def offline(token, useragent):
    url = 'https://api-backend.yescoin.gold/user/offline'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def get_daily(token, useragent):
    url = 'https://api-backend.yescoin.gold/mission/getDailyMission'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def finish_daily(token, useragent, mission_id):
    url = 'https://api-backend.yescoin.gold/mission/finishDailyMission'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers, json=mission_id)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def get_finish_status_task(token, useragent):
    url = 'https://api-backend.yescoin.gold/task/getFinishTaskBonusInfo'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def get_account_build_info(token, useragent):
    url = 'https://api-backend.yescoin.gold/build/getAccountBuildInfo'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None

def get_task_list(token, useragent):
    url = 'https://api-backend.yescoin.gold/task/getTaskList'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None


def check_task_status(token, useragent, task_id):
    url = 'https://api-backend.yescoin.gold/task/checkTask'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers, json=task_id)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None


def claim_reward_task(token, useragent, task_id):
    url = 'https://api-backend.yescoin.gold/task/claimTaskReward'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers, json=task_id)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None


def claim_bonus_task(token, useragent, id):
    url = 'https://api-backend.yescoin.gold/task/claimBonus'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers, json=id)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None


def level_up(token, useragent, id):
    url = 'https://api-backend.yescoin.gold/build/levelUp'
    headers['Token'] = token
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, headers=headers, json=id)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print_(f"{Fore.RED}{response.text}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f"{Fore.RED}Mã trạng thái không mong muốn: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_(f"{Fore.RED}Lỗi thực hiện yêu cầu: {e}")
        return None


def printdelay(delay):
    now = datetime.now().isoformat(" ").split(".")[0]
    target_time = datetime.now() + timedelta(seconds=delay)
    print_(f"{Fore.CYAN}Trong lúc chờ đợi hãy vào nhóm tìm tool tiếp nhé :) {Fore.YELLOW}https://t.me/toolcodecheat", style=Style.BRIGHT)
    while datetime.now() < target_time:
        remaining_time = target_time - datetime.now()
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{Fore.BLUE}[{now}]{Style.RESET_ALL} | {Fore.CYAN}Thời gian chờ: {hours} giờ, {minutes} phút, {seconds} giây{Style.RESET_ALL}\r", end="")
        time.sleep(1)
    print()


def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query



def main():
    queries = load_credentials()
    tokens = [None] * len(queries)
    walletaddr = [None] * len(queries)
    giftboxs = [0] * len(queries)

    print_(f"{Fore.GREEN}Đang chạy với {len(queries)} tài khoản.", style=Style.BRIGHT)

    selector_upgrade = input("Tự động nâng cấp level c/k  : ").strip().lower()
    interval_giftbox = 3600

    while True:
        for index, query in enumerate(queries):
            table_data = []
            parse = parse_query(query)
            user = parse.get('user')
            currentTime = int(time.time())
            useragent = getuseragent(index)
            user_data = parse_and_reconstruct(query)
            token = tokens[index]

            if token is None:
                datalogin = login(user_data, useragent)
                if datalogin is not None:
                    codelogin = datalogin.get('code')
                    if codelogin == 0:
                        data = datalogin.get('data')
                        tokendata = data.get('token')
                        tokens[index] = tokendata
                        print_("Làm mới Token", Fore.GREEN)
                    else:
                        print_(f"{datalogin.get('message')}", Fore.RED)

            token = tokens[index]
            # LẤY THÔNG TIN TÀI KHOẢN # GET ACCOUNT INFO
            data_account_info = getaccountinfo(token, useragent)

            if data_account_info is not None:
                code = data_account_info.get('code')
                if code == 0:
                    username = user.get('username')
                    data = data_account_info.get('data')
                    currentAmount = data.get('currentAmount')
                    levelInfo = data.get('levelInfo')
                    rankName = levelInfo.get('rankName')
                    level = levelInfo.get('level')
                    table_data.append([username, f"{rankName} - {level}", currentAmount])

            # Nhiệm vụ hàng ngày # Daily Mission
            daily = get_daily(token, useragent)
            if daily is not None:
                print_('Lấy nhiệm vụ hàng ngày', Fore.GREEN)
                data = daily.get('data')
                for da in data:
                    missionStatus = da.get('missionStatus')
                    name = da.get('name')
                    missionId = da.get('missionId')
                    if missionStatus == 0:
                        time.sleep(2)
                        finish_ = finish_daily(token, useragent, missionId)
                        if finish_ is not None:
                            code = finish_.get('code')
                            if code == 0:
                                data = finish_.get('data')
                                reward = data.get('reward')
                                print_(f"Nhiệm vụ: {name} | Phần thưởng: {reward}", Fore.CYAN)
                    else:
                        print_(f"Nhiệm vụ: {name} Đã hoàn thành", Fore.GREEN)

            # Lấy danh sách nhiệm vụ # Get List Task
            time.sleep(2)
            data_list_task = get_task_list(token, useragent)
            if data_list_task is not None:
                print_('Lấy Danh sách Nhiệm vụ', Fore.GREEN)
                code = data_list_task.get('code', 500)
                if code == 0:
                    data = data_list_task.get('data', {})
                    taskList = data.get('taskList', [])
                    specialTaskList = data.get('specialTaskList', [])

                    for task in taskList:
                        taskStatus = task.get('taskStatus', 0)
                        checkStatus = task.get('checkStatus', 0)
                        taskId = task.get('taskId', '')
                        taskDetail = task.get('taskDetail', '')

                        if checkStatus == 0:
                            time.sleep(2)
                            data_check_status_task = check_task_status(token, useragent, taskId)
                            if data_check_status_task is not None:
                                code = data_check_status_task.get('code', 500)
                                if code == 0:
                                    data = data_check_status_task.get('data', False)
                                    if data:
                                        time.sleep(2)
                                        data_reward_task = claim_reward_task(token, useragent, taskId)
                                        if data_reward_task is not None:
                                            code = data_reward_task.get('code', 500)
                                            if code == 0:
                                                print_(f"Nhiệm vụ {taskDetail} Hoàn thành, Phần thưởng {data_reward_task.get('data').get('bonusAmount')}", Fore.CYAN)
                        elif taskStatus == 0:
                            time.sleep(2)
                            data_reward_task = claim_reward_task(token, useragent, taskId)
                            if data_reward_task is not None:
                                code = data_reward_task.get('code', 500)
                                if code == 0:
                                    print_(f"Nhiệm vụ {taskDetail} Hoàn thành, Phần thưởng {data_reward_task.get('data').get('bonusAmount')}", Fore.CYAN)
                        else:
                            print_(f"Nhiệm vụ {taskDetail} Đã hoàn thành", Fore.GREEN)

                    for task in specialTaskList:
                        taskStatus = task.get('taskStatus', 0)
                        checkStatus = task.get('checkStatus', 0)
                        taskId = task.get('taskId', '')
                        taskDetail = task.get('taskDetail', '')
                        if checkStatus == 0:
                            time.sleep(2)
                            data_check_status_task = check_task_status(token, useragent, taskId)
                            if data_check_status_task is not None:
                                code = data_check_status_task.get('code', 500)
                                if code == 0:
                                    data = data_check_status_task.get('data', False)
                                    if data:
                                        time.sleep(2)
                                        data_reward_task = claim_reward_task(token, useragent, taskId)
                                        if data_reward_task is not None:
                                            code = data_reward_task.get('code', 500)
                                            if code == 0:
                                                print_(f"Nhiệm vụ {taskDetail} Hoàn thành, Phần thưởng {data_reward_task.get('data').get('bonusAmount')}", Fore.CYAN)
                        elif taskStatus == 0:
                            time.sleep(2)
                            data_reward_task = claim_reward_task(token, useragent, taskId)
                            if data_reward_task is not None:
                                code = data_reward_task.get('code', 500)
                                if code == 0:
                                    print_(f"Nhiệm vụ {taskDetail} Hoàn thành, Phần thưởng {data_reward_task.get('data').get('bonusAmount')}", Fore.CYAN)
                        else:
                            print_(f"Nhiệm vụ {taskDetail} Đã hoàn thành", Fore.GREEN)

            # Kiểm tra phần thưởng nhiệm vụ # Check Task Reward
            time.sleep(2)
            data_check_task = get_finish_status_task(token, useragent)
            if data_check_task is not None:
                code = data_check_task.get('code', 500)
                if code == 0:
                    data = data_check_task.get('data')
                    dailyTaskBonusStatus = data.get('dailyTaskBonusStatus')
                    if dailyTaskBonusStatus == 1:
                        time.sleep(2)
                        data_claim_task = claim_bonus_task(token, useragent, 1)
                        if data_claim_task is not None:
                            code = data_claim_task.get('code')
                            if code == 0:
                                print_(f"Nhận phần thưởng nhiệm vụ hàng ngày thành công, Phần thưởng {data_claim_task.get('data').get('bonusAmount')}", Fore.CYAN)
                    commonTaskBonusStatus = data.get('commonTaskBonusStatus')
                    if commonTaskBonusStatus == 1:
                        time.sleep(2)
                        data_claim_task = claim_bonus_task(token, useragent, 2)
                        if data_claim_task is not None:
                            code = data_claim_task.get('code')
                            if code == 0:
                                print_(f"Nhận phần thưởng nhiệm vụ thành công, Phần thưởng {data_claim_task.get('data').get('bonusAmount')}", Fore.CYAN)

            if currentTime - giftboxs[index] >= interval_giftbox:
                giftboxs[index] = currentTime
                datalogin = login(user_data, useragent)
                if datalogin is not None:
                    codelogin = datalogin.get('code')
                    if codelogin == 0:
                        data = datalogin.get('data')
                        tokendata = data.get('token')
                        token = tokendata
                        tokens[index] = tokendata
                    else:
                        print_(f"{datalogin.get('message')}", Fore.RED)

                data_getaccountbuild = getacccountbuildinfo(token, useragent)
                if data_getaccountbuild is not None:
                    data = data_getaccountbuild.get('data')
                    specialbox = data.get('specialBoxLeftRecoveryCount')
                    coinpool = data.get('coinPoolLeftRecoveryCount')
                    time.sleep(2)

                    if specialbox > 0:
                        data_specialbox = getspecialbox(token, useragent)
                        if data_specialbox is not None:
                            code = data_specialbox.get('code')
                            if code == 0:
                                print_("Đã áp dụng hộp đặc biệt", Fore.GREEN)
                                time.sleep(10)

                    if selector_upgrade == 'c':
                        singleCoinLevel = data.get('singleCoinLevel')
                        singleCoinUpgradeCost = data.get('singleCoinUpgradeCost')

                        if singleCoinUpgradeCost <= currentAmount:
                            time.sleep(2)
                            data_level_up = level_up(token, useragent, 1)
                            if data_level_up is not None:
                                code = data_level_up.get('code')
                                if code == 0:
                                    currentAmount -= singleCoinUpgradeCost
                                    print_(f"Nâng cấp Đồng xu đơn thành công, Cấp độ hiện tại {singleCoinLevel + 1}", Fore.MAGENTA)

                        coinPoolRecoveryLevel = data.get('coinPoolRecoveryLevel')
                        coinPoolRecoveryUpgradeCost = data.get('coinPoolRecoveryUpgradeCost')
                        if coinPoolRecoveryUpgradeCost <= currentAmount:
                            time.sleep(2)
                            data_level_up = level_up(token, useragent, 2)
                            if data_level_up is not None:
                                code = data_level_up.get('code')
                                if code == 0:
                                    currentAmount -= coinPoolRecoveryUpgradeCost
                                    print_(f"Nâng cấp Phục hồi Đồng xu thành công, Cấp độ hiện tại {coinPoolRecoveryLevel + 1}", Fore.MAGENTA)

                        coinPoolTotalLevel = data.get('coinPoolTotalLevel')
                        coinPoolTotalUpgradeCost = data.get('coinPoolTotalUpgradeCost')
                        if coinPoolTotalUpgradeCost <= currentAmount:
                            time.sleep(2)
                            data_level_up = level_up(token, useragent, 3)
                            if data_level_up is not None:
                                code = data_level_up.get('code')
                                if code == 0:
                                    currentAmount -= coinPoolTotalUpgradeCost
                                    print_(f"Nâng cấp Đồng xu tổng thành công, Cấp độ hiện tại {coinPoolTotalLevel + 1}", Fore.MAGENTA)


            data_getspecialboxreload = getspecialboxreloadpage(token, useragent)
            if data_getspecialboxreload is not None:
                code = data_getspecialboxreload.get('code')
                time.sleep(2)

                if code == 0:
                    data_giftbox = getspecialboxinfo(token, useragent)
                    if data_giftbox is not None:
                        data = data_giftbox.get('data')
                        autobox = data.get('autoBox')
                        recoverybox = data.get('recoveryBox')

                        if autobox is not None:
                            payload = {
                                'boxType': 1,
                                'cointCount': autobox.get('specialBoxTotalCount')
                            }
                            data_collectbox = collectspecialbox(token, useragent, payload)
                            if data_collectbox is not None:
                                data = data_collectbox.get('data')
                                print_(f"Nhận Hộp: {data.get('collectAmount')}", Fore.BLUE)
                                time.sleep(5)

                        if recoverybox is not None:
                            payload = {
                                'boxType': 2,
                                'coinCount': recoverybox.get('specialBoxTotalCount')
                            }
                            data_collectbox = collectspecialbox(token, useragent, payload)
                            if data_collectbox is not None:
                                data = data_collectbox.get('data')
                                print_(f"Nhận Hộp: {data.get('collectAmount')}", Fore.BLUE)
                                time.sleep(5)


            defcount = 250
            while True:
                takecount = random.randint(5, 15)
                defcount = defcount - takecount
                data_collectcoin = collectCoin(token, useragent, defcount)


                if data_collectcoin is not None:
                    code = data_collectcoin.get('code')
                    message = data_collectcoin.get('message')


                    if code == 0:
                        data = data_collectcoin.get('data')
                        data_accountinfo = getaccountinfo(token, useragent)

                        if data_accountinfo is not None:
                            code = data_accountinfo.get('code')
                            if code == 0:
                                dataacc = data_accountinfo.get('data')
                                if dataacc is not None:
                                    print_(f"Đã thu thập: {data['collectAmount']} || Đồng xu hiện tại: {dataacc['currentAmount']}", Fore.YELLOW)
                        else:
                            print_("Lỗi thu thập", Fore.RED)

                    else:
                        if coinpool > 0:
                            datagetcoin = getcoinpool(token, useragent)
                            if datagetcoin is not None:
                                code = datagetcoin.get('code')
                                if code == 0:
                                    print_("Đã sử dụng phần thưởng Coin Pool", Fore.GREEN)
                                    coinpool -= 1
                                    defcount = 250
                            time.sleep(2)
                        else:
                            print_(f"Thông báo: {message}", Fore.RED)
                            time.sleep(2)
                            print_("Chuyển sang tài khoản khác", Fore.YELLOW)
                            break
                time.sleep(5)

            if table_data:
                print(tabulate(table_data, headers=["Tên người dùng", "Cấp độ", "Số dư"], tablefmt="fancy_grid"))

        delay = random.randint(600, 700)
        printdelay(delay)
        time.sleep(delay)


if __name__ == "__main__":
    main()