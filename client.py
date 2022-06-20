import socket, threading, subprocess
HOST = '192.168.0.103'
PORT = 5050
FORMAT = 'UTF-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send('admin'.encode(FORMAT))

def send():
    msg = input('$ ')
    if len(msg)>0 and msg!='cls' and msg!='clear':client.send(msg.encode(FORMAT))
    else:
        if msg == 'cls' or msg == 'clear': subprocess.call('cls', shell=True)
        send()
    if msg == 'exit':
        client.close()
        exit()

def receive():
    while True:
        output = client.recv(1024).decode(FORMAT)
        print(output)
        send()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send()
