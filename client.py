import socket
from datetime import datetime
from threading import Thread
from Class.User import User
from Class.Login import Login
from Class.Register import Register
from Class.Graphic import Graphic
from Class.Db import Db
from plyer import notification
import pyaudio

db_instance = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')
# Server's IP address and port
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
VOCAL_PORT = 8081
separator_token = "<SEP>" # Separator token for messages

# Initialize TCP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vocalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Set audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Open microphone stream
input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

new_user = False

# Connect to the server
try:
    clientSocket.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")
except Exception as e:
    print(f"Error connecting to the server: {e}")
    exit()

# GUI initialization
app = Login()
app.windows.mainloop()
user_info = app.userInfo
if user_info == []:
    app = Register()
    app.windows.mainloop()
    user_info = app.userInfo
    client = User(user_info[0], user_info[1], user_info[2], user_info[3])
    new_user = True
    app = Graphic(client)
    
else:
    client = User(user_info[2], user_info[1], user_info[3], user_info[4])
    new_user = False
    app = Graphic(client)

# Set client socket for user
client.clientSocket = clientSocket

# Function to handle incoming messages
def listen_for_messages():
    try:
        while True:
            message = clientSocket.recv(1024).decode()
            if not message:
                break
            if "<COMMAND>notification" in message:
                message_parts = message.split('|')
                notification.notify(
                    title=message_parts[1],
                    message="Nouveau message dans le salon " + message_parts[1],
                    timeout=10
                )
            elif "<COMMAND>refresh" in message:
                app.update_option_menu()
                app.text_rooms_menu.configure(command=handle_switch_channel)  # Update command
            
            else:
                app.receive_message(message)
    except Exception as e:
        print(f"Error occurred while listening for messages: {e}")

# Function to send messages
def send_message(message):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"{client.channel}{separator_token}{date_now}{separator_token}{client.firstname}{separator_token}{client.lastname}{separator_token}{message}"
    clientSocket.send(to_send.encode())

# Function to handle "Send" button click event
def handle_send_button():
    message = app.send_message()
    send_message(message)

# Function to handle "Switch Channel" event
def handle_switch_channel(channel_name):
    channel_name = app.select_channel(channel_name)
    if channel_name is not None:
        client.joinChannel(channel_name)
        send_message("<COMMAND>switch")

# Function to handle "Create Channel" event
def handle_create_channel():
    new_channel_name = app.create_channel()
    if new_channel_name:
        send_message(f"<COMMAND>create_channel|{new_channel_name}")
        handle_switch_channel(new_channel_name)
        app.text_rooms_menu.configure(command=handle_switch_channel)  # Update command
        app.text_rooms_menu.set(new_channel_name)

# Function to send audio data
def send_audio():
    while True:
        try:
            data = input_stream.read(CHUNK)
            vocalSocket.sendall(data)
        except Exception as e:
            print(f"Error occurred while sending audio: {e}")
            break

# Function to play received audio data
def play_audio():
    while True:
        try:
            data = vocalSocket.recv(CHUNK)
            if not data:
                break
            output_stream.write(data)
        except Exception as e:
            print(f"Error occurred while playing audio: {e}")
            break

# Function to join the voice chat
def join_voice_chat():
    try:
        vocalSocket.connect((SERVER_HOST, VOCAL_PORT))
        send_audio_thread = Thread(target=send_audio)
        send_audio_thread.start()
        play_audio_thread = Thread(target=play_audio)
        play_audio_thread.start()
    except Exception as e:
        print(f"Error occurred while joining voice chat: {e}")

# Function to quit the voice chat and cleanup resources
def quit_voice_chat():
    try:
        vocalSocket.close()
        input_stream.stop_stream()
        input_stream.close()
        output_stream.stop_stream()
        output_stream.close()
        audio.terminate()
    except Exception as e:
        print(f"Error occurred while quitting voice chat: {e}")


# Start listening for messages in a separate thread
t1 = Thread(target=listen_for_messages)
t1.start()

# Set GUI button commands
app.send_button.config(command=handle_send_button)
app.text_rooms_menu.configure(command=handle_switch_channel)
app.create_channel_button.config(command=handle_create_channel)
app.join_voice_button.config(command=join_voice_chat)
app.quit_voice_button.config(command=quit_voice_chat)

if new_user == True:
    send_message("<COMMAND>refresh")

# Display GUI
app.show()



# Close the sockets
clientSocket.close()
vocalSocket.close()