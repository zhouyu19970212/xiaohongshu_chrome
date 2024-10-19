"""
配置文件
"""
from queue import Queue

from tool import EmailAccountManager

# 当前登录用户
CurrentUser = None

# 用户列表
UserList = []

# Cookies字典
CookiesDict = {}

# 实例
Browser = None

# 是否需要登陆，默认读取Cookie登录
login_status = False

# 标题，描述
title = ""
describe = ""

# 图片存放路径
catalog_image = r"E:\Project\Python\小红书\image"
# 邮件账号存放路径
email_accounts_file_path = r'D:\xiaohongshu\config\email_account.txt'
# 手机号存放路径
phone_number_file_path = r'D:\xiaohongshu\config\phone_number.txt'

# 文件后缀
suffix = ['.jpg', '.jpeg', '.png', '.webp']


# 导入邮箱账号密码
# 配置文件格式：账号1:密码1:用户名1
manager = EmailAccountManager(email_accounts_file_path)

# 导入手机号
phone_num = ""

# 手机登录验证码
phone_code = ""

# control_flow
control_flow = Queue()
publish_num = 30
for i in range(publish_num):
    control_flow.put('n')
    control_flow.put('2')

# 发布计数器
publish_count = 0
