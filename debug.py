import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

nickname = input("Enter your nickname: ")
join_code = input("Enter the join code: ")

host, port = join_code.split(":")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
   try:
       client.connect((host, int(port)))
       logging.info("Connected to the server")
       break
   except ConnectionRefusedError:
       logging.error("Failed to connect to the server. Please ensure the server is running and accessible.")
       host, port = join_code.split(":") # Reset the host and port
       join_code = input("Enter the join code: ") # Ask for the join code again

def receive():
 while True:
      try:
          message = client.recv(1024).decode('ascii')
          if message == 'NICK':
              client.send(nickname.encode('ascii'))
              logging.info("Sent nickname to the server")
          else:
              logging.info(f"Received message: {message}")
      except BrokenPipeError:
          logging.error("Server closed the connection.")
          break
      except ConnectionResetError:
          logging.error("Lost connection to the server.")
          break
      except Exception as e:
          logging.error(f"An error occurred: {str(e)}")
          break

def write():
 while True:
      message = f'{nickname}: {input("> ")}'
      client.send(message.encode('ascii'))
      logging.info(f"Sent message to the server: {message}")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
