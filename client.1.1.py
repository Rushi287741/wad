from pydoc import cli
from Crypto.PublicKey import RSA
from binascii import hexlify,unhexlify
from Crypto.Cipher import PKCS1_OAEP
import sys
import threading
import socket
#Kali

global priv_key,pub_key, privKeyObj, pubKeyObj, pubKeyObj_client

key = RSA.generate(2048)

priv_key = key.exportKey(format='PEM', passphrase=None, pkcs=1)
pub_key = key.publickey().exportKey(format='PEM',passphrase=None,pkcs=1)
privKeyObj = RSA.importKey(priv_key)
pubKeyObj = RSA.importKey(pub_key)
print ("Private Key Generated : ",priv_key)
print ("Public Key Generated : ",pub_key)
input('Press Enter to connect to server...')

def client_receive():
    while True:
            message = client.recv(2048)
            cipher = PKCS1_OAEP.new(privKeyObj)
            message = cipher.decrypt(message).decode('utf-8')
            if message == 'bye':
                client.close()
                sys.exit()
            else:
                print("Received from Alice : "+message)
                print(">>",end=" ")

def client_send():
    while True:
        message = input(">> ")
        cipher = PKCS1_OAEP.new(pubKeyObj_client)
        ciphertext = cipher.encrypt(message.encode())
        #print(ciphertext)
        client.send(ciphertext)

host = '127.0.0.1'               #Ubuntu mac Ip
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 12345))
client.send(pubKeyObj.exportKey(format='PEM',passphrase=None,pkcs=1))
pubKeyObj_client =  RSA.importKey(client.recv(2048), passphrase=None).publickey().exportKey('PEM')
pubKeyObj_client = RSA.importKey(pubKeyObj_client)
    # Listener Thread
receive_thread = threading.Thread(target = client_receive)
receive_thread.start()
    # Sender Thread
send_thread = threading.Thread(target = client_send)
send_thread.start()
