import socket
import threading

server_ip = input("Enter an ip for the server to bind to: ")
server_port = int(input("Enter a port for the server to bind to: "))


class Server:
   def __init__(self, host=server_ip):
       self.host = host
       self.port = server_port # Hardcoded port number
       self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.clients = []
       self.nicknames = []

   def broadcast(self, message):
       for client in self.clients:
           client.send(message)

   def handle(self, client):
       while True:
           try:
               message = client.recv(1024)
               self.broadcast(message)
           except:
               index = self.clients.index(client)
               self.clients.remove(client)
               client.close()
               nickname = self.nicknames[index]
               self.nicknames.remove(nickname)
               self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
               break

   def receive(self):
       while True:
           client, address = self.server.accept()
           print(f"Connected with {str(address)}")

           client.send('NICK'.encode('ascii'))
           nickname = client.recv(1024).decode('ascii')
           self.nicknames.append(nickname)
           self.clients.append(client)

           print(f"Nickname of the client is {nickname}!")
           self.broadcast(f"{nickname} joined the chat!".encode('ascii'))
           client.send('Connected to the server!'.encode('ascii'))

           thread = threading.Thread(target=self.handle, args=(client,))
           thread.start()

   def run(self):
       try:
           self.server.bind((self.host, self.port))
           self.server.listen()
           print(f"Server started on port {self.port}. Your join code is {self.host}:{self.port}")
           self.receive()
       except OSError as e:
           print(f"Failed to bind to {self.host}:{self.port}. Error: {e}")

server = Server()
server.run()
