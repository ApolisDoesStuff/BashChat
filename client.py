import socket
import threading

nickname = input("Enter your nickname: ")
join_code = input("Enter the join code: ")

host, port = join_code.split(":")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
   try:
       client.connect((host, int(port)))
       break
   except ConnectionRefusedError:
       print("Failed to connect to the server. Please ensure the server is running and accessible.")
       host, port = join_code.split(":") # Reset the host and port
       join_code = input("Enter the join code: ") # Ask for the join code again

def receive():
  while True:
      try:
          message = client.recv(1024).decode('ascii')
          if message == 'NICK':
              client.send(nickname.encode('ascii'))
          else:
              print(message)
      except BrokenPipeError:
          print("Server closed the connection.")
          break
      except ConnectionResetError:
          print("Lost connection to the server.")
          break
      except Exception as e:
          print(f"An error occurred: {str(e)}")
          break

def write():
  while True:
      message = f'{nickname}: {input("> ")}'
      client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
