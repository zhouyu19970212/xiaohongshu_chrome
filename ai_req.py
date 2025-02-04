import os.path
import random

import requests
import json
import Config
import log


def get_two_random_elements(lst):
    """
    从列表中随机取出两个不同的元素。

    :param lst: 输入的列表
    :return: 包含两个不同元素的元组
    """
    if len(lst) < 2:
        raise ValueError("列表中元素数量必须大于或等于2")
    # 随机选择两个不同的索引
    indices = random.sample(range(len(lst)), 2)
    # 返回对应的两个元素
    return lst[indices[0]], lst[indices[1]]


def get_language_db():
    if not os.path.exists(Config.language_db_path):
        log.common_logger.info("路径下面不存在此文件" + Config.language_db_path)
    with open(Config.language_db_path, encoding='utf-8') as f:
        e_list = []
        for line in f:
            # 处理每一行数据
            stripped_line = line.strip()
            if stripped_line == "":
                continue
            e_list.append(stripped_line)
        Config.language_db['211_college'] = e_list
        print(Config.language_db['211_college'])


def get_ai_content(content: str) -> str:
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-turbo-8k?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "penalty_score": 1,
        "enable_system_memory": False,
        "disable_search": False,
        "enable_citation": False,
        "enable_trace": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    _text = response.text
    data = json.loads(_text)
    result = data['result']
    return result


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    API_KEY = Config.client_id
    SECRET_KEY = Config.secret_id
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
