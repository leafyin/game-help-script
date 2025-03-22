# encoding=utf-8
import hashlib
import random
import requests

app_id = '20250321002311115'
private_key = '2CIieDd6J1OvEWpSyoej'


def sign(q, salt):
    text = app_id + q + salt + private_key
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode("utf-8"))
    return md5_hash.hexdigest()


def trans(text, src, to):
    salt = str(random.randint(10 ** 7, 10 ** 8 - 1))
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "q": text,
        "from": src,
        "to": to,
        "appid": app_id,
        "salt": salt,
        "sign": sign(text, salt)
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        result = response.json()
        return result['trans_result'][0]['dst']
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


if __name__ == '__main__':
    trans("火药", "zh", "jp")
    pass

