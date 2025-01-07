import requests
import json
import random
import time
import os
from colorama import Fore, Style, init
import urllib3
import asyncio

init()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Colors:
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL

ascii_art = f""" {Fore.BLUE}

   █████████   █████ ███████████   ██████████   ███████████      ███████    ███████████       █████████    █████████    █████████
  ███░░░░░███ ░░███ ░░███░░░░░███ ░░███░░░░███ ░░███░░░░░███   ███░░░░░███ ░░███░░░░░███     ███░░░░░███  ███░░░░░███  ███░░░░░███
 ░███    ░███  ░███  ░███    ░███  ░███   ░░███ ░███    ░███  ███     ░░███ ░███    ░███    ░███    ░███ ░███    ░░░  ███     ░░░
 ░███████████  ░███  ░██████████   ░███    ░███ ░██████████  ░███      ░███ ░██████████     ░███████████ ░░█████████ ░███         
 ░███░░░░░███  ░███  ░███░░░░░███  ░███    ░███ ░███░░░░░███ ░███      ░███ ░███░░░░░░      ░███░░░░░███  ░░░░░░░░███░███         
 ░███    ░███  ░███  ░███    ░███  ░███    ███  ░███    ░███ ░░███     ███  ░███            ░███    ░███  ███    ░███░░███     ███
 █████   █████ █████ █████   █████ ██████████   █████   █████ ░░░███████░   █████           █████   █████░░█████████  ░░█████████
 ░░░░░   ░░░░░ ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░   ░░░░░    ░░░░░░░    ░░░░░           ░░░░░   ░░░░░  ░░░░░░░░░    ░░░░░░░░░  
==============================================
    BOT              : Open Loop
    Telegram Channel : @airdropasc               
    Telegram Group   : @autosultan_group         
==============================================
"""

print(ascii_art)


def logger(message, level='info', value=""):
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    colors = {
        'info': Colors.GREEN,
        'warn': Colors.YELLOW,
        'error': Colors.RED,
        'success': Colors.BLUE,
        'debug': Colors.WHITE,
    }
    color = colors.get(level, Colors.WHITE)
    print(f"{color}[{now}] [{level.upper()}]: {message}{Colors.RESET}", f"{Colors.YELLOW}{value}{Colors.RESET}")

def ask_question(query):
    return input(query)

def get_random_quality():
    return random.randint(60, 99)

def get_proxies():
    if not os.path.exists('proxy.txt'):
        logger("代理文件 proxy.txt 未找到!", 'error')
        return []
    with open('proxy.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_tokens():
    if not os.path.exists('token.txt'):
        logger("Token 文件 token.txt 未找到!", 'error')
        return []
    with open('token.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

async def share_bandwidth(token, proxy=None):
    try:
        quality = get_random_quality()
        proxies = {'https': f'http://{proxy}'} if proxy else None

        response = requests.post('https://api.openloop.so/bandwidth/share',
                                 headers={'Authorization': f'Bearer {token}',
                                          'Content-Type': 'application/json'},
                                 json={'quality': quality},
                                 proxies=proxies,
                                 verify=False)

        response.raise_for_status()
        data = response.json()

        if 'data' in data and 'balances' in data['data']:
            balance = data['data']['balances'].get('POINT', 'N/A')
            logger(f"分享带宽成功 信息: {Colors.YELLOW}{data.get('message', '无信息')}{Colors.RESET} | "
                   f"分数: {Colors.YELLOW}{quality}{Colors.RESET} | "
                   f"总收益: {Colors.YELLOW}{balance}{Colors.RESET}")
        else:
            logger(f"意外的响应格式: {data}", 'warning')

    except requests.RequestException as e:
        logger(f"分享带宽时出错: {e}", 'error')

async def share_bandwidth_for_all_tokens(proxies=None):
    tokens = get_tokens()
    for index, token in enumerate(tokens):
        proxy = proxies[index] if proxies and index < len(proxies) else None
        logger(f"正在为第 {index + 1} 个账号分享带宽...", 'info')
        await share_bandwidth(token, proxy)

def get_account_info():
    if not os.path.exists('accounts.txt'):
        logger("账户信息文件 accounts.txt 未找到!", 'error')
        return []
    with open('accounts.txt', 'r') as file:
        return [line.strip().split(',') for line in file if line.strip()]

def login_user(email, password, use_proxy=True):
    try:
        login_payload = {'username': email, 'password': password}
        proxies = None if not use_proxy else {'https': f'http://{get_proxies()[0]}'}

        login_response = requests.post('https://api.openloop.so/users/login',
                                       headers={'Content-Type': 'application/json'},
                                       data=json.dumps(login_payload),
                                       proxies=proxies,
                                       verify=False)

        if login_response.status_code != 200:
            raise requests.HTTPError(f"登录失败，状态码: {login_response.status_code}")

        login_data = login_response.json()
        access_token = login_data.get('data', {}).get('accessToken', '')
        if access_token:
            logger('登录成功，获取到 Token:', 'success', access_token)
            with open('token.txt', 'a') as token_file:
                token_file.write(f"{access_token}\n")
            logger('访问令牌已保存到 token.txt')
        else:
            logger('从登录响应中提取访问令牌失败。', 'error')
    except requests.RequestException as e:
        logger('登录过程中出错:', 'error', e)

def register_user():
    try:
        accounts = get_account_info()
        if not accounts:
            logger("账户信息文件 accounts.txt 为空!", 'error')
            return

        use_proxy_choice = ask_question('是否使用代理进行注册？(y/n): ').lower()
        invite_code = ask_question('请输入您的邀请码（所有账户将使用这个邀请码）: ')

        for email, password in accounts:
            registration_payload = {'name': email, 'username': email, 'password': password, 'inviteCode': invite_code}
            proxies = {'https': f'http://{get_proxies()[0]}'} if use_proxy_choice == 'y' else None

            try:
                register_response = requests.post('https://api.openloop.so/users/register',
                                                  headers={'Content-Type': 'application/json'},
                                                  data=json.dumps(registration_payload),
                                                  proxies=proxies,
                                                  verify=False)

                if register_response.status_code == 401:
                    logger(f'邮箱 {email} 已存在。尝试登录...')
                    login_user(email, password, use_proxy_choice == 'y')
                elif register_response.status_code == 200:
                    logger(f'注册 {email} 成功:', 'success')
                    login_user(email, password, use_proxy_choice == 'y')
                else:
                    raise requests.HTTPError(f"注册 {email} 失败，状态码: {register_response.status_code}")
            except requests.RequestException as e:
                logger(f'为 {email} 注册或登录时出错:', 'error', e)

    except KeyboardInterrupt:
        logger('用户中断了进程。', 'info')

def main_menu():
    while True:
        print(Colors.MAGENTA + banner + Colors.RESET)
        print(f"{Colors.YELLOW}1. Boot Node")
        print(f"2. Get Token")
        print(f"3. Exit")
        choice = ask_question(f"{Colors.WHITE}请选择 (1, 2, 或 3): {Colors.RESET}")

        if choice == '1':
            use_proxy_choice = ask_question('Proxy ga？(y/n): ').lower()
            proxies = get_proxies() if use_proxy_choice == 'y' else None
            if use_proxy_choice == 'y' and not proxies:
                logger("没有可用的代理，将不使用代理。", 'warn')

            logger('开始分享带宽...')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(share_bandwidth_for_all_tokens(proxies))

            while True:
                time.sleep(60)
                loop.run_until_complete(share_bandwidth_for_all_tokens(proxies))

        elif choice == '2':
            register_user()
        elif choice == '3':
            logger('退出应用程序...')
            break
        else:
            logger('无效选项，请重试。', 'warn')

if __name__ == "__main__":
    main_menu()
