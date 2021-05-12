import socket
import threading

nickname = input("Please enter your nickname: ")
if nickname.upper() == "ADMIN":
    nickname = nickname.upper()
    password = input('Enter the password for admin: ')
else:
    password = input('Enter the password for joining chat: ')

host_name = "localhost"
port_number = 34567

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_name, port_number))

stop_thread = False

def encrypt1(x):
    keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#%! ?/><*():-.,1234567890"
    values1 = keys[39:78] + keys[0:39]
    values2 = "$^&_=+|\}{][‰;/`~§£€¥æç©®°±¶•☺♀♪♫☼►◄↕‼↨↑↓→←∟↔☻♥♦♣♠◘○◙♂▲▼ßΓπΣσµτΦΘΩδ∞φε∩≡░≈■¤Þ÷"
    values3 = values2[34:47] + values2[54:78] + values2[0:34] + values2[47:54]

    encryptdict1 = dict(zip(keys, values1))
    encryptdict2 = dict(zip(values1[::-1], values3))

    new_message1 = "".join([encryptdict1[letter] for letter in x])
    new_message2 = "".join([encryptdict2[character] for character in new_message1])
    return new_message2

def decrypt(message1):
    keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#%! ?/><*():-.,1234567890"
    values1 = keys[39:78] + keys[0:39]
    values2 = "$^&_=+|\}{][‰;/`~§£€¥æç©®°±¶•☺♀♪♫☼►◄↕‼↨↑↓→←∟↔☻♥♦♣♠◘○◙♂▲▼ßΓπΣσµτΦΘΩδ∞φε∩≡░≈■¤Þ÷"
    values3 = values2[34:47] + values2[54:78] + values2[0:34] + values2[47:54]

    decryptdict1 = dict(zip(values3, values1))
    decryptdict2 = dict(zip(values1[::-1], keys))

    new_message1 = "".join([decryptdict1[letter] for letter in message1])
    new_message2 = "".join([decryptdict2[character] for character in new_message1])
    return new_message2

def recieve_message():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client_socket.recv(2048).decode("utf-8")
            message_new = decrypt(message)
            if message_new == "NICKNAME":
                client_socket.send(encrypt1(nickname).encode("utf-8"))
                next_message = client_socket.recv(2048).decode("utf-8")
                next_message_new = decrypt(next_message)
                if next_message_new == "PASS":
                    client_socket.send(encrypt1(password).encode("utf-8"))
                    if decrypt(client_socket.recv(2048).decode("utf-8")) == "REFUSE":
                        print("Connection was refused! Wrong Password!!")
                        stop_thread = True
                elif next_message_new == "BAN":
                    print("You are banned from this chat!")
                    client_socket.close()
                    stop_thread = True
            else:
                print(message_new)
        except:
            print("An error was encountered!")
            client_socket.close()
            break

def write_message():
    while True:
        if stop_thread:
            break
        message = f"{nickname}: {input()}"
        if message[len(nickname)+2:].startswith("/"):
            if nickname == "ADMIN":
                if message[len(nickname)+2:].startswith("/kick"):
                    client_socket.send(encrypt1(f"KICK {message[len(nickname)+8:]}").encode("utf-8"))
                elif message[len(nickname)+2:].startswith("/ban"):
                    client_socket.send(encrypt1(f"BAN {message[len(nickname)+7:]}").encode("utf-8"))
            else:
                print("Commands can only be executed by the admins!")
        else:
            client_socket.send(encrypt1(message).encode("utf-8"))

recieve_message_thread = threading.Thread(target=recieve_message)
recieve_message_thread.start()

write_message_thread = threading.Thread(target=write_message)
write_message_thread.start()