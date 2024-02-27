import socket
from datetime import datetime
from threading import Thread
from Class.User import User
from Class.Login import Login
from Class.Register import Register
from Class.Graphic import Graphic
from Class.Db import Db


db_instance = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')
# Server's IP address and port
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
separator_token = "<SEP>" # Separator token for messages

# Initialize TCP socket
clientSocket = socket.socket()

try:
    # Connect to the server
    clientSocket.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")
except Exception as e:
    print(f"Error connecting to the server: {e}")
    exit()

# Get user information
#firstname = input("Enter your firstname: ")
#lastname = input("Enter your lastname: ")
#email = input("Enter your email: ")
#password = input("Enter your password: ")

# Create user instance
    
app = Login()
app.windows.mainloop()
user_info = app.userInfo
if user_info == []:
    app = Register()
    app.windows.mainloop()
    user_info = app.userInfo
    client = User(user_info[0], user_info[1], user_info[2], user_info[3])
    app = Graphic(user_info[2])

else:
    client = User(user_info[2], user_info[1], user_info[3], user_info[4])
    app = Graphic(user_info[3])


client.clientSocket = clientSocket

def listen_for_messages():
    try:
        while True:
            message = clientSocket.recv(1024).decode()
            app.receive_message(message)
    except Exception as e:
        print(f"Error occurred while listening for messages: {e}")

# Start listening for messages in a separate thread
t1 = Thread(target=listen_for_messages)
t1.daemon = True
t1.start()


def send_message(message):    
    # Add timestamp, name, and color to the message
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client.channel}{separator_token}{date_now}{separator_token}{client.firstname}{separator_token}{client.lastname}{separator_token}{message}"
    print (to_send)
    
    # Send the message to the server
    clientSocket.send(to_send.encode())

# Function to handle the "Send" button click event
def handle_send_button():
    message = app.send_message()
    send_message(message)

def handle_switch_channel(channel_name):
    channel_name = app.select_channel(channel_name)
    if channel_name != None:
        client.joinChannel(channel_name)
        send_message("<COMMAND>switch")

def handle_create_channel():
    new_channel_name = app.create_channel()
    if new_channel_name:
        send_message(f"<COMMAND>create_channel | {new_channel_name}")
        handle_switch_channel(new_channel_name)
        app.text_rooms_menu.configure(command=handle_switch_channel)  # Update command
        app.text_rooms_menu.set(new_channel_name)




# Set the "Send" button command to the handle_send_button function
app.send_button.config(command=handle_send_button)
app.text_rooms_menu.configure(command=handle_switch_channel)
app.create_channel_button.config(command=handle_create_channel)

app.show()


# Close the socket
#clientSocket.close()