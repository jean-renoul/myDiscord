import socket
import random
from datetime import datetime
from threading import Thread
from Class.User import user
from Class.login import Login
from Class.register import Register
from Class.Graphic import Graphic


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
    client = user(user_info[0], user_info[1], user_info[2], user_info[3])
    print (user_info[0], user_info[1], user_info[2], user_info[3])
else:
    client = user(user_info[2], user_info[1], user_info[3], user_info[4])
    print (user_info[2], user_info[1], user_info[3], user_info[4])

client.clientSocket = clientSocket

app = Graphic()



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

# Main loop to send messages

def send_message(message):
    if message.lower() == 'q':
        # Close the socket and exit the program
        clientSocket.close()
        exit()
    
    # Add timestamp, name, and color to the message
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client.channel}{separator_token}[{date_now}]{separator_token}{client.firstname}{separator_token}{message}"
    
    # Send the message to the server
    clientSocket.send(to_send.encode())

# Function to handle the "Send" button click event
def handle_send_button():
    message = app.send_message()
    send_message(message)

# Set the "Send" button command to the handle_send_button function
app.send_button.config(command=handle_send_button)

app.afficher()


# Close the socket
#clientSocket.close()