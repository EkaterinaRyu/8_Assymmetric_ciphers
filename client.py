import socket
import random
import sys

import regex as re

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!, '

def get_keys_from_file():
    global closed_key
    with open('client_keys.txt', 'r') as file:
        string = file.readline()
        sample = re.compile(r'\d')

        client_open_key = int(sample.findall(string)[0])
        server_open_key = int(sample.findall(string)[1])
        closed_key = int(sample.findall(string)[2])

        print(f"Default keys:\nClient's open key: {client_open_key}\nServer's open key: {server_open_key}\nSecret key: {closed_key}\n")

def connect():
    sock = socket.socket()
    check = 0
    while check == 0:
        port = int(input('Enter the port: '))
        while (port < 1024 or port > 65535):
            print("Cannot connect to the port")
            port = int(input('Enter the port: '))

        try:
            sock.connect(('127.0.0.1', port))
            check = 1
            return sock
        except ConnectionRefusedError:
            print('Cannot connect to the port, try again')

def exchange_keys(sock):
    
    print('Connected, exchanging the keys\n')

    global closed_key
    #a = random.randint(1, 100)
    a = 6
    g = 5
    p = 7

    client_open_key = g ** a % p
    sock.send(f'{str(client_open_key)};{str(g)};{str(p)}'.encode())

    server_open_key = sock.recv(1024).decode()
    try:
        closed_key = int(server_open_key) ** a % p
    except ValueError:
        print('Connection to the server failed or was dropped')
        sys.exit()

    print(f"Client's open key: {client_open_key}\nServer's open key: {server_open_key}\nSecret key: {closed_key}\n")

def encryption(message):
    message_encrypted = ''
    shift = closed_key

    for symbol in message:
        message_encrypted += alphabet[(alphabet.index(symbol) + shift) % len(alphabet)]

    return message_encrypted

def decryption(message):
    message_decrypted = ''
    shift = closed_key

    for symbol in message:
        message_decrypted += alphabet[(alphabet.index(symbol) - shift) % len(alphabet)]

    return message_decrypted

def exchange_messages(sock1):

    print('Secure connection established\n')

    message_recieved = sock.recv(1024).decode()
    print(f'Message recieved (encoded): {message_recieved}')
    print(f'Message recieved: {decryption(message_recieved)}\n')

    message_sent = 'Hey, Server!'
    sock.send(encryption(message_sent).encode())
    print(f'Message sent: {message_sent}')
    print(f'Message sent (encoded): {encryption(message_sent)}')

sock = connect()
exchange_keys(sock)
#get_keys_from_file()
sock1 = connect()
exchange_messages(sock1)