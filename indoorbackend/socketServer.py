# import socket

# sock = socket.socket()
# print ("Socket created ...")

# port = 8080
# sock.bind(('', port))
# sock.listen(5)

# print ('socket is listening')

# while True:
#     c, addr = sock.accept()
#     print ('got connection from ', addr)

#     jsonReceived = c.recv(1024)
#     print ("Json received -->", jsonReceived)

#     c.close()




# first of all import the socket library
import socket			

# next create a socket object
s = socket.socket()		
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

# a forever loop until we interrupt it or
# an error occurs
while True:

    # Establish connection with client.
    c, addr = s.accept()	
    print ('Got connection from', addr )

    # send a thank you message to the client. encoding to send byte type.
    c.send('Thank you for connecting'.encode())

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break








# # An example script to connect to Google using socket
# # programming in Python
# import socket # for socket
# # import sys

# try:
# 	s = socket.socket()
# 	print ("Socket successfully created")
# except socket.error as err:
# 	print ("socket creation failed with error %s" %(err))

# # default port for socket
# port = 8080

# # try:
# # 	host_ip = socket.gethostbyname('www.google.com')
# # except socket.gaierror:

# # 	# this means could not resolve the host
# # 	print ("there was an error resolving the host")
# # 	sys.exit()

# # connecting to the server
# s.connect(port)

# print ("the socket has successfully connected to google")

# sock.listen(5)

# while True:
#     c, addr = sock.accept()
#     print ('got connection from ', addr)

#     jsonReceived = c.recv(1024)
#     print ("Json received -->", jsonReceived)

#     c.close()