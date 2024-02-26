import socket
import random
from datetime import datetime
from colorama import Fore, init
from threading import Thread
from myDiscord.Class.User import User


# Initialize colors
init()

# Set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# Choose a random color for the client
client_color = random.choice(colors)

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
firstname = input("Enter your firstname: ")
lastname = input("Enter your lastname: ")
email = input("Enter your email: ")
password = input("Enter your password: ")

# Create user instance
client = User(firstname, lastname, email, password, 'autre')
client.clientSocket = clientSocket



def listen_for_messages():
    try:
        while True:
            message = clientSocket.recv(1024).decode()
            print("\n" + message)
    except Exception as e:
        print(f"Error occurred while listening for messages: {e}")

# Start listening for messages in a separate thread
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

# Main loop to send messages
while True:
    # Input message to send to the server
    to_send = input("Enter your message ('q' to quit): ")
    
    # Check if the user wants to quit
    if to_send.lower() == 'q':
        break
    
    # Add timestamp, name, and color to the message
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client.channel} {separator_token} {client_color}[{date_now}] {firstname}{separator_token}{to_send}{Fore.RESET}"
    
    # Send the message to the server
    clientSocket.send(to_send.encode())

# Close the socket
clientSocket.close()