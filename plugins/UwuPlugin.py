# UwuPlugin.py

from uwuipy import uwuipy

uwu = uwuipy(None, 0.3, 0.3, 0.3, 1, False)


def on_message_sent(message):
  uwuified_message = uwu.uwuify(message)
  print(f"Sent message: {uwuified_message}")
  return uwuified_message
