import socket
import threading

host_name = "localhost"
port_number = 34567

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_name, port_number))
server_socket.listen(10)

clients_list = []
nicknames_list = []
bans = []

def encrypt(entered):
    keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#%! ?/><*():-.,1234567890"
    values1 = keys[39:78] + keys[0:39]
    values2 = "$^&_=+|\}{][‰;/`~§£€¥æç©®°±¶•☺♀♪♫☼►◄↕‼↨↑↓→←∟↔☻♥♦♣♠◘○◙♂▲▼ßΓπΣσµτΦΘΩδ∞φε∩≡░≈■¤Þ÷"
    values3 = values2[34:47] + values2[54:78] + values2[0:34] + values2[47:54]

    encryptdict1 = dict(zip(keys, values1))
    encryptdict2 = dict(zip(values1[::-1], values3))

    message = entered

    new_message1 = "".join([encryptdict1[letter] for letter in message])
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

def broadcasting(message):
    for client in clients_list:
        client.send(encrypt(message).encode('utf-8'))

def kick_user(name):
    if name in nicknames_list:
        name_index = nicknames_list.index(name)
        client_to_kick = clients_list[name_index]
        client_to_kick.send(encrypt("You were kicked out by a admin!").encode("utf-8"))
        clients_list.remove(client_to_kick)
        client_to_kick.close()
        nicknames_list.remove(name)
        broadcasting(f"{name} was kicked by an admin!")

def client_handling(client):
    while True:
        try:
            recieved_message = client.recv(2048).decode('utf-8')
            msg = decrypt(recieved_message)
            if msg.startswith("KICK"):
                if nicknames_list[clients_list.index(client)] == "ADMIN":
                    name_to_kick = msg[5:]
                    kick_user(name_to_kick)
                else:
                    client.send(encrypt("Command was refused!").encode("utf-8"))
            elif msg.startswith("BAN"):
                if nicknames_list[clients_list.index(client)] == "ADMIN":
                    name_to_ban = msg[4:]
                    kick_user(name_to_ban)
                    bans.append(name_to_ban)
                    print(f"{name_to_ban} was BANNED!!")
                else:
                    to_encrypt = "Command was refused!"
                    client.send(encrypt(to_encrypt).encode("utf-8"))
            else:
                print(recieved_message)
                broadcasting(msg)
        except:
            if client in clients_list:
                index_value = clients_list.index(client)
                clients_list.remove(client)
                client.close()
                nickname = nicknames_list[index_value]
                broadcasting(f"{nickname} has left the chat!")
                nicknames_list.remove(nickname)
                break

def recieve_message():
    while True:
        client, address = server_socket.accept()
        print(f"Connected with {str(address)}")

        client.send(encrypt("NICKNAME").encode("utf-8"))
        nickname1 = client.recv(2048).decode("utf-8")
        nickname = decrypt(nickname1)

        if nickname in bans:
            client.send(encrypt("BAN").encode("utf-8"))
            client.close()
            continue

        if nickname == "ADMIN":
            client.send(encrypt("PASS").encode("utf-8"))
            password1 = client.recv(2048).decode("utf-8")
            password = decrypt(password1)

            if password != "AdminPassCode@111":
                client.send(encrypt("REFUSE").encode("utf-8"))
                client.close()
                continue
        else:
            client.send(encrypt("PASS").encode("utf-8"))
            password1 = client.recv(2048).decode('utf-8')
            password = decrypt(password1)

            if password != "GeneralPass":
                client.send(encrypt("REFUSE").encode("utf-8"))
                client.close()
                continue

        nicknames_list.append(nickname)
        clients_list.append(client,)

        print(f"Nickname of the client is {nickname}!")
        broadcasting(f"{nickname} has joined the chat!!")
        client.send(encrypt("You are now connected to the chat!").encode("utf-8"))

        thread = threading.Thread(target=client_handling, args=(client,))
        thread.start()

print("Server is created!")
print("Server is listening.....")
recieve_message()