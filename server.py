import configparser
import os
import socket
import threading

CONFIG_FILE = 'config.ini'

def create_default_config():
    config = configparser.ConfigParser()
    config['SERVER'] = {'ip': '', 'port': '', 'start': 'False', 'welcome_message': ''}
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)


if not os.path.exists(CONFIG_FILE):
   create_default_config()

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

class Server:
   def __init__(self, host=None, port=None):
       self.host = host
       self.port = port
       self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.clients = []
       self.nicknames = []
       self.lock = threading.Lock()

   def broadcast(self, message):
       with self.lock:
           for client in self.clients:
               client.send(message)

   def handle(self, client):
       while True:
           try:
               message = client.recv(1024)
               self.broadcast(message)
           except socket.error as e:
               print(f"Socket error: {e}")
               break
           except Exception as e:
               print(f"Unexpected error: {e}")
               break

   def receive(self):
       while True:
           client, address = self.server.accept()
           print(f"Connected with {str(address)}")

           client.send('NICK'.encode('ascii'))
           nickname = client.recv(1024).decode('ascii')
           with self.lock:
               self.nicknames.append(nickname)
               self.clients.append(client)

           print(f"Nickname of the client is {nickname}!")
           self.broadcast(f"{nickname} joined the chat!\n".encode('ascii'))

           # Check if there's a welcome message and send it if not empty
           welcome_message = config.get('SERVER', 'welcome_message', fallback='')
           if welcome_message.strip():
               client.send(welcome_message.encode('ascii'))

           thread = threading.Thread(target=self.handle, args=(client,))
           thread.start()

   def run(self):
       try:
           self.server.bind((self.host, self.port))
           self.server.listen(5)
           print(f"Server started on port {self.port}. Your join code is {self.host}:{self.port}")
           self.receive()
       except OSError as e:
           print(f"Failed to bind to {self.host}:{self.port}. Error: {e}")

# Check if the server should start
if config.getboolean('SERVER', 'start'):
   server = Server(config.get('SERVER', 'ip'), config.getint('SERVER', 'port'))
   server.run()
else:
   print("Server not started due to configuration.")
