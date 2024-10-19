import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import log
import Config
import Cookie
import Init
import Create
import tool


def select_user():
    while Config.UserList:
        for i, v in enumerate(Config.UserList):
            print(f"{i + 1}.{v}", end="\t")
        # select = input("\n请选择用户(输入'n'使用手机号登录)：")
        # 没有做其他登录方式，目前只能用手机号登录，暂时用control_flow控制
        select = Config.control_flow.get()
        if select == 'n':
            # 手机号登录
            Config.login_status = True
            return
        try:
            Config.CurrentUser = Config.UserList[int(select) - 1]
            return
        except (ValueError, IndexError):
            print("请输入正确的值！")


def login_successful():
    # 获取昵称
    name_content = WebDriverWait(Config.Browser, 10, 0.2).until(
        lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
    print(f"{name_content},登录成功!")
    Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
    Config.CurrentUser = name_content
    # 获取Cookie
    Cookie.get_new_cookie()
    Cookie.save_cookie()


def cookie_login():
    Cookie.set_cookie()
    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
    except TimeoutException:
        Config.login_status = True
        return
    login_successful()


def login():
    log.common_logger.info(f'准备打开小红书创作者中心登录页面...')
    Config.Browser.get("https://creator.xiaohongshu.com/login")
    if not Config.login_status:
        cookie_login()
        return
    # 访问登陆页面
    # while True:
    #     phone_number = input("请输入手机号：")
    #     if len(phone_number) == 11:
    #         break
    #     print("手机号码不合法！")
    with open(Config.phone_number_file_path, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 去除行末的换行符
            if line:  # 忽略空行
                Config.phone_num = line
    phone_number = Config.phone_num
    input_phone = WebDriverWait(Config.Browser, 10, 0.2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-19z0sa3'))
    )
    log.common_logger.info(f'准备发送手机号')
    input_phone[1].send_keys(phone_number)
    log.common_logger.info(f'success!{phone_number}')

    # 发送验证码
    log.common_logger.info(f'准备发送验证码')
    WebDriverWait(Config.Browser, 10, 0.2).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'css-uyobdj'))
    ).click()
    # Config.Browser.find_element(By.CLASS_NAME, value='css-uyobdj').click()

    # while True:
    #     # 输入验证码
    #     code_1 = input("请输入验证码：")
    #     if len(code_1) == 6:
    #         break
    #     print("验证码不合法！")
    # 输入验证码
    code = tool.get_phone_code()

    WebDriverWait(Config.Browser, 10, 0.2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.css-19z0sa3.css-1ge5flv.dyn'))
    ).send_keys(code)
    log.common_logger.info(f'success!{code}')
    # input_code = Config.Browser.find_element(By.CSS_SELECTOR, '.css-19z0sa3.css-1ge5flv.dyn')
    # input_code.send_keys(code)

    # 登录
    WebDriverWait(Config.Browser, 10, 0.2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1jgt0wa.css-kyhkf6.dyn.beer-login-btn'))
    ).click()
    # Config.Browser.find_element(By.CSS_SELECTOR, '.css-1jgt0wa.css-kyhkf6.dyn.beer-login-btn').click()
    login_successful()


def switch_users():
    print("正在清除Cookie")
    Config.Browser.delete_all_cookies()
    select_user()
    login()


def Quit():
    Cookie.save_cookie()
    print("Bye!")
    Config.Browser.quit()
    sys.exit(0)


def select_create():
    while True:
        if Config.publish_count != 0:
            time.sleep(1800)
        if Config.Browser.current_url != "https://creator.xiaohongshu.com/publish/publish":
            Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
        print("1. 视频上传  2.图文上传  3. 切换用户 4.退出")
        # 功能选择，暂时只做了图文上传，现在用control_flow控制
        # select = input("请选择功能：")
        select = Config.control_flow.get()
        match select:
            case '1':
                Create.create_video()
                return
            case '2':
                Create.create_image()
                return
            case '3':
                switch_users()
                return
            case '4':
                Quit()
                return
            case default:
                print("请输入合法的数字！")


def start():
    try:
        # 初始化程序
        log.common_logger.info(f'正在初始化程序...')
        print("正在初始化程序……")
        Init.init()
        # 选择用户
        select_user()
        # 登录
        login()
        while True:
            # 选择功能
            select_create()
    except KeyboardInterrupt:
        print("\nBye!")
    except Exception as e:
        print(f"发生了一些错误：\n{e}")
