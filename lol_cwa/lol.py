import asyncio
import json
import subprocess
import requests
import base64

import websockets


class LOLInfo:

    def __init__(self):
        self.result = {}
        bundle_line = None
        cmd = 'wmic PROCESS WHERE name=\'LeagueClientUx.exe\' GET commandline'
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        with process.stdout as stdout:
            stdout_str = stdout.readlines()
        for cli_out in stdout_str:
            if 'LeagueClientUx.exe' in cli_out:
                bundle_line = cli_out
        if bundle_line is not None:
            for line in bundle_line.split('\" \"'):
                if '--' in line and '=' in line:            # 只获取有用的字符串
                    row = line.strip('--')
                    print(row)
                    k = row.split('=')[0].replace('-', '_')
                    if 'riotgamesapi-settings' in row:      # 因为这个字符串中可能有多个等号，从名称开始分割
                        v = row[row.index('=') + 1:len(row)]
                    else:
                        v = row.split('=')[1]
                    self.result[k] = v
        # print(self.result)


def auth_encode(token):
    return base64.b64encode(f"riot:{token}".encode()).decode()


def lcu_get(port, token, path):
    auth = auth_encode(token)
    url = f"https://127.0.0.1:{port}{path}"
    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(url, headers=headers, verify=False)
    print(response.json())


def message(port, token):
    auth = auth_encode(token)
    print('===' + auth)
    url = f"https://127.0.0.1:{port}/lol-game-client-chat/v1/instant-messages"
    data = {
        "summonerName": "BytoW",
        "message": "111"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {auth}"
    }
    response = requests.post(url, json=data, headers=headers, verify=False)
    print(response.json())


def subscribe(port, token):
    auth = auth_encode(token)
    url = f"https://127.0.0.1:{port}/Subscribe"
    headers = {"Authorization": f"Basic {auth}"}
    data = {
        "eventName": "OnJsonApiEvent_lol-game-client-chat_v2_instant-messages"
    }
    response = requests.get(url, data=data, headers=headers, verify=False)
    print(response.json())


def lcu_help(port, token):
    auth = auth_encode(token)
    url = f"https://127.0.0.1:{port}/help"
    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(url, headers=headers, verify=False)
    print(response.json())


async def listen_lcu_chat(port, token):
    auth = auth_encode(token)

    # WebSocket 连接
    uri = f"wss://127.0.0.1:{port}"
    headers = {"Authorization": f"Basic {auth}"}

    async with websockets.connect(uri, ssl=False, extra_headers=headers, verify=False) as ws:
        # 订阅聊天事件
        subscribe_msg = {
            "event": "OnJsonApiEvent_lol-game-client-chat_v1_instant-messages",
            "data": {
                "uri": "/lol-game-client-chat/v1/instant-messages"
            }
        }
        await ws.send(json.dumps(subscribe_msg))

        await ws.send('help')

        # 持续监听消息
        while True:
            message = await ws.recv()
            event_data = json.loads(message)
            if "data" in event_data:
                print("收到对局聊天:", event_data["data"])


if __name__ == '__main__':
    info = LOLInfo()
    app_port = info.result['app_port']
    auth_token = info.result['remoting_auth_token']

    # subscribe(app_port, auth_token)
    # asyncio.get_event_loop().run_until_complete(listen_lcu_chat(app_port, auth_token))
