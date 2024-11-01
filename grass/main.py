
from colorama import Fore, Style, init
import asyncio
import os
import random
import ssl
import json
import time
import uuid
import requests
import shutil
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent
import websockets


init(autoreset=True)


print(Fore.CYAN + Style.BRIGHT + "   █████████   █████ ███████████   ██████████   ███████████      ███████    ███████████       █████████    █████████    █████████")
print(Fore.CYAN + Style.BRIGHT + "  ███░░░░░███ ░░███ ░░███░░░░░███ ░░███░░░░███ ░░███░░░░░███   ███░░░░░███ ░░███░░░░░███     ███░░░░░███  ███░░░░░███  ███░░░░░███")
print(Fore.CYAN + Style.BRIGHT + " ░███    ░███  ░███  ░███    ░███  ░███   ░░███ ░███    ░███  ███     ░░███ ░███    ░███    ░███    ░███ ░███    ░░░  ███     ░░░")
print(Fore.CYAN + Style.BRIGHT + " ░███████████  ░███  ░██████████   ░███    ░███ ░██████████  ░███      ░███ ░██████████     ░███████████ ░░█████████ ░███         ")
print(Fore.CYAN + Style.BRIGHT + " ░███░░░░░███  ░███  ░███░░░░░███  ░███    ░███ ░███░░░░░███ ░███      ░███ ░███░░░░░░      ░███░░░░░███  ░░░░░░░░███░███         ")
print(Fore.CYAN + Style.BRIGHT + " ░███    ░███  ░███  ░███    ░███  ░███    ███  ░███    ░███ ░░███     ███  ░███            ░███    ░███  ███    ░███░░███     ███")
print(Fore.CYAN + Style.BRIGHT + " █████   █████ █████ █████   █████ ██████████   █████   █████ ░░░███████░   █████           █████   █████░░█████████  ░░█████████")
print(Fore.CYAN + Style.BRIGHT + " ░░░░░   ░░░░░ ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░   ░░░░░    ░░░░░░░    ░░░░░           ░░░░░   ░░░░░  ░░░░░░░░░    ░░░░░░░░░")
print(Fore.CYAN + Style.BRIGHT + "==============================================")
print(Fore.CYAN + Style.BRIGHT + "    NODE             : GRASS CLI ")
print(Fore.CYAN + Style.BRIGHT + "    Telegram Channel : @airdropasc")
print(Fore.CYAN + Style.BRIGHT + "    Telegram Group   : @autosultan_group")
print(Fore.CYAN + Style.BRIGHT + "==============================================")


user_agent = UserAgent()
random_user_agent = user_agent.random

async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy)) if socks5_proxy else "NoProxyDeviceID"
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
                "Origin": "chrome-extension://ilehaonighjijnmpnagapkhpcdbhclfg"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            uri = "wss://proxy.wynd.network:4650"
            proxy = Proxy.from_url(socks5_proxy) if socks5_proxy else None

            async with websockets.connect(uri, ssl=ssl_context, extra_headers=custom_headers) as websocket:
                logger.info("Connected to websocket")

                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(5)

                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "4.0.3",
                                "extension_id": "ilehaonighjijnmpnagapkhpcdbhclfg"
                            }
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)
            logger.error(socks5_proxy)

async def main():
    _user_id = input('Please Enter your user ID: ')

    
    if os.path.exists('proxy.txt'):
        with open('proxy.txt', 'r') as file:
            local_proxies = file.read().splitlines()
    else:
        local_proxies = []

    
    if not local_proxies:
        print(Fore.YELLOW + "Tidak ada proxy ditemukan. Menghubungkan tanpa proxy...")
        await connect_to_wss(None, _user_id)
    else:
        
        tasks = [asyncio.ensure_future(connect_to_wss(proxy, _user_id)) for proxy in local_proxies]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
