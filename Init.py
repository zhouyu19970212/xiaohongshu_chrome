import json
import os
import log
import Config

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# 关闭浏览器实例
def close_browser():
    if Config.Browser:
        Config.Browser.quit()


def init_browser():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 无头模式，锁屏运行
    options.add_argument(f'user-agent=={UserAgent().random}')
    # 无界面模式
    # options.add_argument('--headless')

    try:
        log.common_logger.info(f"正在实例化webdriver...")
        service = ChromeService(executable_path=r"D:\coding\robot\chromedriver-win64\chromedriver.exe")
        Config.Browser = webdriver.Chrome(options=options, service=service)
        Config.Browser.maximize_window()
    except Exception as e:
        log.common_logger.info(f"Failed to initialize browser: {e}")


def init_cookie():
    """读取本地 Cookie"""
    if os.path.isfile("cookies.json"):
        with open("cookies.json", "r+", encoding="utf-8") as f:
            content = f.read()
            if content:
                Config.CookiesDict.update(json.loads(content))
            else:
                print("Cookie 文件为空！")
                Config.login_status = True
                return
    else:
        print("Cookie 文件不存在！")
        Config.login_status = True
        return


def init_user():
    """初始化 UserList"""
    for k, _ in Config.CookiesDict.items():
        Config.UserList.append(k)


def init():
    # 读取本地 cookie
    init_cookie()
    # 初始化所有用户
    init_user()
    # 初始化浏览器
    init_browser()
