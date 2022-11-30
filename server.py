import random
import socket
import sys
import regex as re

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQESTUVWXYZ!, '
certified_client_keys = [3]
ports = [1025, 1026]

def connect():
    sock = socket.socket()
    port = int(input('Enter the port: '))
    if (port < 1024 or port > 65535):
        print('Cannot connect to the port')
        port = 1025
        while port in ports:
            port += 1
        ports.append(port)
        print(f'Set to nearest free value: {port}')

    sock.bind(('', port))
    sock.listen(5)
    print('Server is running')
    conn, addr = sock.accept()
    print(f'Connected: {addr}\n')
    return conn, addr

def get_keys_from_file():
    global closed_key
    with open('server_keys.txt', 'r') as file:
        string = file.readline()
        sample = re.compile(r'\d')

        client_open_key = int(sample.findall(string)[0])
        server_open_key = int(sample.findall(string)[1])
        closed_key = int(sample.findall(string)[2])
        
        print(f"Default keys:\nClient's open key: {client_open_key}\nServer's open key: {server_open_key}\nSecret key: {closed_key}\n")
        
def exchange_keys(conn1, addr1):
    
    global closed_key
    b = random.randint(1, 100)

    message = conn.recv(1024).decode().split(';')
    client_open_key = message[0]
    #if client_open_key not in certified_client_keys:
        #print('Клиент не прошел сертификацию')
        #conn.close()
        #sys.exit()
    g = message[1]
    p = message[2]

    server_open_key = int(g) ** b % int(p)
    conn.send(str(server_open_key).encode())

    closed_key = int(client_open_key) ** b % int(p)

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

def exchange_messages(conn, addr):

    message_sent = 'Hello, Client!'
    conn.send(encryption(message_sent).encode())
    print(f'Message sent: {message_sent}')
    print(f'Message sent (encoded): {encryption(message_sent)}\n')

    message_recieved = conn.recv(1024).decode()
    print(f'Message recieved (encoded): {message_recieved}')
    print(f'Message recieved: {decryption(message_recieved)}')

conn, addr = connect()
exchange_keys(conn, addr)
#get_keys_from_file()
conn1, addr1 = connect()
exchange_messages(conn1, addr1)