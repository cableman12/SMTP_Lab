from socket import *

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
CRLF = "\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
# Using Gmail's submission server with STARTTLS (port 587)
mailserver = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
import ssl, base64

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
#Fill in end

# Then it gets decoded for the server to understand
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send EHLO command and print server response.
ehloCommand = 'EHLO Alice\r\n'
clientSocket.send(ehloCommand.encode())
recv1 = clientSocket.recv(4096).decode()
print(recv1)
if not recv1.startswith('250'):
    print('250 reply not received from server (EHLO).')

# Start TLS (required by Gmail on 587), then EHLO again over TLS
clientSocket.send(b"STARTTLS\r\n")
recv_tls = clientSocket.recv(1024).decode()
print(recv_tls)
if recv_tls[:3] != '220':
    print('220 reply not received to STARTTLS.')
    clientSocket.close()
    raise SystemExit

# Wrap socket with TLS and re-EHLO
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver[0])

clientSocket.send(ehloCommand.encode())
recv1b = clientSocket.recv(4096).decode()
print(recv1b)
if not recv1b.startswith('250'):
    print('250 reply not received from server (EHLO after TLS).')

# ---- AUTH LOGIN (use Gmail address + App Password) ----
GMAIL_USER = "alfredodelatorre891@gmail.com"
APP_PASSWORD = "labp qjgw eubb blqw"  # generate in Google Account > Security > App Passwords

clientSocket.send(b"AUTH LOGIN\r\n")
auth_step1 = clientSocket.recv(1024).decode()
print(auth_step1)  # expect 334 (Username:)
clientSocket.send(base64.b64encode(GMAIL_USER.encode()) + CRLF.encode())
auth_step2 = clientSocket.recv(1024).decode()
print(auth_step2)  # expect 334 (Password:)
clientSocket.send(base64.b64encode(APP_PASSWORD.encode()) + CRLF.encode())
auth_ok = clientSocket.recv(1024).decode()
print(auth_ok)     # expect 235 Authentication successful
if auth_ok[:3] != '235':
    print("Authentication failed; cannot proceed.")
    clientSocket.send(b"QUIT\r\n")
    clientSocket.close()
    raise SystemExit

# Send MAIL FROM command and print server response.
# Fill in start
mail_from = f"MAIL FROM:<{GMAIL_USER}>\r\n"
clientSocket.send(mail_from.encode())
recv2 = clientSocket.recv(1024).decode()
print("MAIL FROM:", recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
recipient = "daisydelatorre2011@icloud.com"
rcpt_to = f"RCPT TO:<{recipient}>\r\n"
clientSocket.send(rcpt_to.encode())
recv3 = clientSocket.recv(1024).decode()
print("RCPT TO:", recv3)
if not (recv3[:3] == '250' or recv3[:3] == '251'):
    print('250/251 reply not received from server.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
clientSocket.send(b"DATA\r\n")
recv4 = clientSocket.recv(1024).decode()
print("DATA:", recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')
# Fill in end

# Send message data.
# Fill in start
headers = [
    f"From: {GMAIL_USER}",
    f"To: {recipient}",
    "Subject: SMTP Lab via Gmail 587 STARTTLS",
]
clientSocket.send((CRLF.join(headers) + CRLF + CRLF + msg).encode())
# Fill in end

# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())    # sends "\r\n.\r\n"
recv5 = clientSocket.recv(1024).decode()
print("After message:", recv5)
if recv5[:3] != '250':
    print('250 reply not received after message body.')
# Fill in end

# Send QUIT command and get server response.
# Fill in start
clientSocket.send(b"QUIT\r\n")
recv6 = clientSocket.recv(1024).decode()                                                                                                                             
print("QUIT:", recv6)
clientSocket.close()
# Fill in end