import socket
import time

headerSize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(4)

while True:
    clientSocket, address = s.accept()
    newMsg = clientSocket.recv(2048).decode()
    if not newMsg:
        break
    print("From connected user: " + str(newMsg))
    newMsg = input("->")
    clientSocket.send(newMsg.encode())
s.close()
