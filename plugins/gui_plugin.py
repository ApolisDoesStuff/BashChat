import tkinter as tk
import threading

class ChatApp:
   def __init__(self, root):
       self.root = root
       self.messages = tk.Text(root)
       self.messages.pack()
       self.input_field = tk.Entry(root)
       self.input_field.pack()
       self.input_field.bind("<Return>", self.send_message)

   def send_message(self, event):
       message = self.input_field.get()
       self.input_field.delete(0, tk.END)
       # TODO: Implement sending the message through the network
       self.messages.insert(tk.END, f"Me: {message}\n")

   def receive_message(self, message):
       self.messages.insert(tk.END, f"Other: {message}\n")

def on_startup():
   root = tk.Tk()
   app = ChatApp(root)
   root.mainloop()
