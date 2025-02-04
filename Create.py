import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from ai_req import get_ai_content, get_language_db, get_two_random_elements

import os.path
import time
import Config
import log
import tool


def create(create_css_elements):
    log.common_logger.info(f"等待资源上传……")
    time.sleep(10)
    create_js = Config.Browser.find_elements(By.CSS_SELECTOR, value=create_css_elements)
    Config.Browser.execute_script('arguments[0].click();', create_js[0])
    log.common_logger.info(f"发布成功！")
    # 发布计数器
    Config.publish_count = Config.publish_count + 1
    log.common_logger.info(f"当前发布次数：{Config.publish_count}")
    log.common_logger.info(f"等待页面返回！")
    time.sleep(5)


def input_content():
    # Config.title = input("请输入标题：")
    # 随机种子
    rand_seed = random.randint(1, 3)
    title_req = ""
    get_language_db()
    a_college, b_college = get_two_random_elements(Config.language_db['211_college'])
    if rand_seed == 1:
        title_req = f"对比{a_college}和{b_college}的控制工程学科就业，用少于20个字来询问大家怎么选择考研学校。"
    elif rand_seed == 2:
        title_req = f"对比{a_college}和{b_college}的自动化专业，用少于20个字来询问大家怎么选择高考学校。"
    elif rand_seed == 3:
        title_req = f"对比{a_college}和{b_college}的自动化专业就业，用少于20个字来询问大家怎么选择考研学校。"
    Config.title = tool.filter_bmp(get_ai_content(title_req))
    log.common_logger.info("BAIDU ERNIE 4.0, 生成AI标题为：")
    log.common_logger.info(Config.title)
    # Config.describe = input("请输入描述：")
    Config.describe = tool.filter_bmp(
        get_ai_content("生成关于【" + Config.title + "】、50字以内的问题。"))
    log.common_logger.info("BAIDU ERNIE 4.0, 生成AI内容为：")
    log.common_logger.info(Config.describe)
    # TODO: 没调试好
    # Config.Browser.find_element(By.CSS_SELECTOR, ".d-input.--color-text-title.--color-bg-fill").send_keys(Config.title)
    log.common_logger.info("输入标题成功")
    tool.waiting_and_log(2)
    Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea").send_keys(Config.describe)
    log.common_logger.info("输入内容成功")


def get_video():
    while True:
        path_mp4 = input("视频路径：")
        path_cover = input("封面路径(不输入使用默认封面)：")
        if not os.path.isfile(path_mp4):
            log.common_logger.info(f"视频不存在！")
        elif path_cover != '':
            if not os.path.isfile(path_cover):
                log.common_logger.info(f"封面图片不存在")
            else:
                return path_mp4, path_cover
        else:
            return path_mp4


def create_video():
    path_mp4, path_cover = get_video()

    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(1)")).click()
    except TimeoutException:
        log.common_logger.info(f"网页好像加载失败了！请重试！")

    # 点击上传视频
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-input").send_keys(path_mp4)
    time.sleep(10)
    WebDriverWait(Config.Browser, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[contains(text(),"重新上传")]'))
    )
    while True:
        time.sleep(3)
        try:
            Config.Browser.find_element(By.XPATH, r'//*[contains(text(),"重新上传")]')
            break
        except Exception:
            log.common_logger.info(f"视频还在上传中···")

    if path_cover != "":
        Config.Browser.find_element(By.CSS_SELECTOR, "button.css-k3hpu2:nth-child(3)").click()

        Config.Browser.find_element(By.XPATH, r'//*[text()="上传封面"]').click()
        # 上传封面
        Config.Browser.find_element(By.CSS_SELECTOR, "div.upload-wrapper:nth-child(2) > input:nth-child(1)").send_keys(
            path_cover)

        # 提交封面
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".css-8mz9r9 > div:nth-child(1) > button:nth-child(2)")).click()
    input_content()
    # 发布
    create(".publishBtn")


def get_image():
    # while True:
    #     path_image = input("图片路径：").split(",")
    #     if 0 < len(path_image) <= 9:
    #         for i in path_image:
    #             if not os.path.isfile(i):
    #                 log.common_logger.info(f"图片不存在！")
    #                 break
    #         else:
    #             return "\n".join(path_image)
    #     else:
    #         log.common_logger.info(f"图片最少1张，最多9张")
    #         continue
    random_number = random.randint(1, 6)
    path_image = Config.catalog_image + f"\\photo{random_number}.jpg"
    return path_image


def create_image():
    path_image = get_image()
    log.common_logger.info("获取图片地址成功：" + path_image)
    tool.waiting_and_log(3)  # TODO: 等待页面加载完成，需要优化一下，不能写死
    image_creator_tab = Config.Browser.find_elements(By.XPATH, "//div[contains(@class, 'creator-tab')]")
    log.common_logger.info("通过XPATH切换到“上传图片”页面：")
    log.common_logger.info(image_creator_tab[1])
    Config.Browser.execute_script('arguments[0].click()', image_creator_tab[1])
    log.common_logger.info("切换成功")
    #  上传图片
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-wrapper > div:nth-child(1) > input:nth-child(1)").send_keys(
        path_image)
    log.common_logger.info("上传图片成功")
    input_content()

    # css定位器
    create('.el-button.publishBtn')
