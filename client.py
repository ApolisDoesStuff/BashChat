import socket
import threading
import importlib.util
import os

nickname = input("Enter your nickname: ")
join_code = input("Enter the join code: ")

host, port = join_code.split(":")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Plugin system
def load_plugin(file_path):
  try:
    spec = importlib.util.spec_from_file_location("", file_path)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    return plugin
  except Exception as e:
    print(f"Failed to load plugin at {file_path}: {str(e)}")
    return None


def load_plugins_from_dir(directory):
  plugins = []
  for filename in os.listdir(directory):
    if filename.endswith(".py"):
      file_path = os.path.join(directory, filename)
      plugin = load_plugin(file_path)
      if plugin is not None:
        plugins.append(plugin)
  return plugins


plugins = load_plugins_from_dir("./plugins/")

while True:
  try:
    client.connect((host, int(port)))
    break
  except ConnectionRefusedError:
    print(
        "Failed to connect to the server. Please ensure the server is running and accessible."
    )
    host, port = join_code.split(":")  # Reset the host and port
    join_code = input("Enter the join code: ")  # Ask for the join code again


def receive():
  while True:
    try:
      message = client.recv(1024).decode('utf-8')
      if message == 'NICK':
        client.send(nickname.encode('utf-8'))
      else:
        for plugin in plugins:
          if hasattr(plugin, 'on_message_received'):
            message = plugin.on_message_received(message)
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
    for plugin in plugins:
      if hasattr(plugin, 'on_message_sent'):
        message = plugin.on_message_sent(message)
    client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
