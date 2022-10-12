import socket

headerSize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

msg = input("->")

while msg.lower().strip() != "bye":
    s.send(msg.encode())
    msg = s.recv(2048).decode()

    print("Received from server: " + msg)

    msg = input("->")
s.close()
