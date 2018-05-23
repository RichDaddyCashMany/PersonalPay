from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email import utils
import socket

class EmailUtil:
    @classmethod
    def send_html_email(cls, title, html, receiver):
        socket.setdefaulttimeout(10)

        sender = ''
        server = 'smtp.exmail.qq.com'
        smtp_port = 465
        user = sender
        passwd = ''

        # 设定root信息
        msg_root = MIMEMultipart('related')
        msg_root['Subject'] = title
        msg_root['From'] = sender
        msg_root['To'] = receiver

        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)

        # 构造MIMEMultipart对象做为根容器
        main_msg = MIMEMultipart()

        html_msg = MIMEText(
            html,
            'html',
            'utf-8'
        )

        main_msg.attach(html_msg)
        # 设置根容器属性
        main_msg['From'] = sender
        main_msg['To'] = receiver
        main_msg['Subject'] = title
        main_msg['Date'] = utils.formatdate()

        # 得到格式化后的完整文本
        full_text = main_msg.as_string()

        try:
            # 发送邮件
            smtp = smtplib.SMTP_SSL(server, smtp_port)
            smtp.login(user, passwd)
            smtp.sendmail(sender, [receiver], full_text)
            smtp.quit()
            print("邮件发送成功!")
            return True
        except BaseException as e:
            print("邮件发送失败!")
            print(e)
            return False
