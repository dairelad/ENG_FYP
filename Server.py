import socket
import sys

# the ip address or hostname of the server, the receiver
host = "169.254.124.252"
# the port, let's use 5001
port = 5001

s = socket.socket()

print("[*] Connecting...")
s.connect((host, port))
print("[+] Connected")

f = open ("mytext.txt", "rb")
l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)
s.close()
print("[>] File sent")