# timestamp_plugin.py

import datetime

def on_message_sent(message):
   timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   return f"[{timestamp}] {message}"

