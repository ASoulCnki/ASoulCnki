import smtplib
from email.header import Header
# 负责构造图片
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
# 负责构造文本
from email.mime.text import MIMEText


class AutoSendErrorMail:
    # 初始化该类
    def __init__(self, mail_host, mail_sender, mail_license, mail_receivers, body_content):
        self.mail_host = mail_host
        self.mail_sender = mail_sender
        self.mail_license = mail_license
        self.mail_receivers = mail_receivers
        self.body_content = body_content

    # 发送错误日志邮件
    def send_email(self):
        mm = MIMEMultipart('related')
        # 邮件主题
        subject_content = """爬虫出现错误！"""
        # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
        mm["From"] = "AsoulCnki<{}>".format(self.mail_sender)
        # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
        mm["To"] = "AsoulCnki_Receiver<{}>".format(self.mail_receivers[0])
        # 设置邮件主题
        mm["Subject"] = Header(subject_content, 'utf-8')

        # 邮件正文内容
        # body_content = """你好，这是一个测试邮件！"""
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(self.body_content, "plain", "utf-8")
        # 向MIMEMultipart对象中添加文本对象
        mm.attach(message_text)
        # stp = smtplib.SMTP()
        stp = smtplib.SMTP_SSL(self.mail_host)
        # 设置发件人邮箱的域名和端口，端口地址为25,ssl端口为465
        stp.connect(self.mail_host, 465)
        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        stp.login(self.mail_sender, self.mail_license)
        # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
        stp.sendmail(self.mail_sender, self.mail_receivers, mm.as_string())
        # 关闭SMTP对象
        stp.quit()


def send_mail(text):
    from app.config.secure import mail_sender, mail_host, mail_license, mail_receivers
    mail_obj = AutoSendErrorMail(mail_host, mail_sender, mail_license, mail_receivers, text)
    mail_obj.send_email()
