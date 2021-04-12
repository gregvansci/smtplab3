from socket import *
from base64 import *
import ssl

YOUR_EMAIL = input("Enter Your Email Address : ")
YOUR_PASSWORD = input("Enter Your Password : ")
YOUR_DESTINATION_EMAIL = input("Enter Email Destination : ")

msg = "\r\nI love computer networks!"
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailServer)
#Fill in end

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')


#SSL AUTH
strtlscmd = "STARTTLS\r\n".encode()
clientSocket.send(strtlscmd)
recvTLS = clientSocket.recv(1024)
print(recvTLS)

sslClientSocket = ssl.wrap_socket(clientSocket)

MAIL_USERNAME = b64encode(YOUR_EMAIL.encode())
MAIL_PASSWORD = b64encode(YOUR_PASSWORD.encode())

authorizationcmd = "AUTH LOGIN\r\n"

sslClientSocket.send(authorizationcmd.encode())
recvAUTH = sslClientSocket.recv(1024)
print(recvAUTH)

sslClientSocket.send(MAIL_USERNAME + "\r\n".encode())
recvUSERNAME = sslClientSocket.recv(1024)
print(recvUSERNAME)

sslClientSocket.send(MAIL_PASSWORD + "\r\n".encode())
recvPASSWORD = sslClientSocket.recv(1024)
print(recvPASSWORD)

# Send MAIL FROM command and print server response.

mailfrom = "MAIL FROM: <{}>\r\n".format(YOUR_EMAIL)
sslClientSocket.send(mailfrom.encode())
recv2 = sslClientSocket.recv(1024)
print(recv2)


# Send RCPT TO command and print server response.

rcptto = "RCPT TO: <{}>\r\n".format(YOUR_DESTINATION_EMAIL)
sslClientSocket.send(rcptto.encode())
recv3 = sslClientSocket.recv(1024)
print(recv3)

# Send DATA command and print server response.

data = 'DATA\r\n'
sslClientSocket.send(data.encode())
recv4 = sslClientSocket.recv(1024)
print(recv4)


# Send message data.

#sslClientSocket.send("Subject: {}\n\n{}".format(YOUR_SUBJECT_EMAIL, msg).encode())
sslClientSocket.send(msg.encode())


# Message ends with a single period.

sslClientSocket.send(endmsg.encode())


# Send QUIT command and get server response.

quitcommand = 'QUIT\r\n'
sslClientSocket.send(quitcommand.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5)
sslClientSocket.close()
print('End of Code!')