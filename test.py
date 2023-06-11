import socket
UDP_IP = "10.33.138.34"
UDP_PORT = 5005

shit = "Jumping Jack"
MESSAGE = (shit).encode()
print(MESSAGE)
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)
while True:
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))