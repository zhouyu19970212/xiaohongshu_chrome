import base64
import imaplib
import time
import log
import Config

mail_host = "imap.163.com"  # 163邮箱收件服务器   # 邮箱授权码
port = 993  # 收件服务器端口


class EmailAccountManager:
    def __init__(self, file_path):
        self._file_path = file_path
        self._accounts = None

    @property
    def accounts(self):
        """
        当访问 accounts 属性时，调用 import_email_accounts 函数。
        """
        if self._accounts is None:
            self._accounts = self.import_email_accounts(self._file_path)
        return self._accounts

    def import_email_accounts(self, file_path):
        """
        从文本文件中导入邮箱账号和密码。

        :param file_path: 文本文件的路径
        :return: 包含邮箱账号和密码的列表，每个元素是一个字典
        """
        accounts = []

        with open(file_path, mode='r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 去除行末的换行符
                if line:  # 忽略空行
                    email, password, name = line.split(':', 2)  # 按照前两个冒号分割
                    accounts.append({'email': email, 'password': password, 'name': name})

        return accounts


def get_phone_code() -> str:
    time.sleep(30)
    with imaplib.IMAP4_SSL(mail_host, port) as serv:
        mail_user = Config.manager.accounts[0]['email']  # 邮箱地址
        mail_pass = Config.manager.accounts[0]['password']
        mail_name = Config.manager.accounts[0]['name']
        serv.login(mail_user, mail_pass)  # 登录邮箱
        # IMAP添加ID指令
        imaplib.Commands['ID'] = ('AUTH')
        args = ("name", mail_name, "contact", mail_user, "version", "1.0.0", "vendor", "python_client")
        serv._simple_command('ID', '("' + '" "'.join(args) + '")')
        # 邮箱中其收到的邮件的数量
        serv.select('INBOX')
        email_count = len(serv.search(None, 'ALL')[1][0].split())
        # 通过fetch(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
        typ, email_content = serv.fetch(f'{email_count}'.encode(), '(RFC822)')
        # 将邮件内存由byte转成str
        email_content = email_content[0][1].decode()
        log.common_logger.info(f'原始邮件内容：{email_content}')
        # 提取邮件内容信息
        key_content_idx = str.find(email_content, 'Content-Transfer-Encoding: base64')
        email_content = email_content[key_content_idx + len('Content-Transfer-Encoding: base64'):]
        log.common_logger.info(f'提取信息：{email_content}')
        # base64解码，并转成utf-8格式
        decoded_content_for_base64 = base64.b64decode(email_content).decode('utf-8')
        log.common_logger.info(f'base64解码：{decoded_content_for_base64}')
        # 从文本中获取验证码
        key_phone_code_idx = str.find(decoded_content_for_base64, '您的验证码是: ')
        phone_code_info = decoded_content_for_base64[key_phone_code_idx + 8:key_phone_code_idx + 14]
        log.common_logger.info(f'从文本中获取验证码：{phone_code_info}')

        Config.phone_code = phone_code_info
        return phone_code_info


# def get_phone_number() -> str:
#     with open(Config.phone_number_file_path, mode='r', encoding='utf-8') as file:
#         for line in file:
#             line = line.strip()  # 去除行末的换行符
#             if line:  # 忽略空行
#                 Config.phone_num = line
#     return Config.phone_num
