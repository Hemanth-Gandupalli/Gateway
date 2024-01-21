import threading
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from datetime import datetime
import importlib
import RPi.GPIO as GPIO

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)

delay_main = 2
delay_internet_off = 3600
delay_compressor_off = 1800
delay_mail = 10
delay_current = 1800

def main():
    while True:
        with open("status.txt",'r') as f:
            status = f.read()
        if status == "True":
            GPIO.output(6, GPIO.HIGH)
            print("Load ON")
        else:
            print("Load off")
            GPIO.output(6, GPIO.LOW)
        time.sleep(delay_main)

def internet():
    while True:
        GPIO.output(5, GPIO.HIGH)
        print("Internet is ON")
        time.sleep(3600)
        GPIO.output(5, GPIO.LOW)
        print("Internet is OFF")  
        time.sleep(3)

def compressor():
    while True:
        GPIO.output(23, GPIO.HIGH)
        print("Compressor is ON")
        time.sleep(1800)
        GPIO.output(23, GPIO.LOW)
        print("Compressor is OFF")
        time.sleep(1800)
def mail():
    global delay_mail
    time.sleep(delay_mail)
    while True:
        try:
            with open("status.txt",'r') as f:
                status = f.read()
            s = status
            print(s)
            email_user = "care.bariflolabs@gmail.com"
            email_password = "ifln keco pdbc hqts"
            # email_send = "data.bariflolabs@gmail.com"
            email_send = "gandupallihemanth86@gmail.com"
            #email_send = "g"
            subject = "IWMS Status"

            msg = MIMEMultipart()
            msg["From"] = email_user
            msg["To"] = email_send
            msg["Subject"] = subject
            if  s == "True":
                with open('data.json', 'r') as file:
                    data = json.load(file)
                sensor1 = data["sensor1"]
                sensor2 = data["sensor2"] 
                sensor3 = data["sensor3"] 
                sensor4 = data["sensor4"]
                x = data["x"]
                y = data["y"]
                z = data["z"]
                print("t")
                #body = f"GW_Status:ON  Aeration:On  CompCurrVal:{current1} Amp  AerationCurrVal:{current2} Amp"
                body = f"GW_Status:ON  Aeration:On  sensor1 :{sensor1} Amp\nsensor2 :{sensor2} Amp\nsensor3 :{sensor3} Amp\nsensor4 :{sensor4} Amp\nX :{x} Amp\nY :{y} Amp\nZ :{z} Amp"
            else:
                print("f")
                body = "GW_status:ON Aeration Device :OFF"


            msg.attach(MIMEText(body,"plain"))

            text = msg.as_string()
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(email_user,email_password)


            server.sendmail(email_user,email_send,text)
            server.quit()
            delay_mail = 5
            time.sleep(1800)
            
        except Exception as e:
            print(e)
        

threading.Thread(target=main).start()
threading.Thread(target=internet).start()
threading.Thread(target=compressor).start()
threading.Thread(target=mail).start()