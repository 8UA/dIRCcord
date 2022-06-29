import socket
from time import sleep
from random import choice
from threading import Thread
from datetime import datetime
from colorama import init, Fore
import os

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = choice(colors)

print(client_color + '''
      d8b   d8,                                              d8b 
      88P  `8P                                               88P 
     d88                                                    d88  
 d888888    88b  88bd88b d8888b d8888b d8888b   88bd88b d888888  
d8P' ?88    88P  88P'  `d8P' `Pd8P' `Pd8P' ?88  88P'  `d8P' ?88  
88b  ,88b  d88  d88     88b    88b    88b  d88 d88     88b  ,88b 
`?88P'`88bd88' d88'     `?888P'`?888P'`?8888P'd88'     `?88P'`88b - client.
''' + f"{Fore.RESET}")

sleep(1)
os.system('cls' if os.name == 'nt' else 'clear')

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "localhost"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# prompt the client for a name
name = input("Enter your name: ")

print('[TIP] you can close the client by sending "q" \n')

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    sleep(0.2)
    #print(f"{name} > ", end='')
    to_send = input(f"{name} > ")

    # a way to exit the program
    if to_send.lower() == '':
        continue

    # a way to exit the program
    if to_send.lower() == 'q':
        s.send(f"{name} has left the chat.".encode())
        sleep(1)
        break

    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}({date_now}) {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# exiting the program
print("Exiting...")
exit()