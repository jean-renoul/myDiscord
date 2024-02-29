import socket
from datetime import datetime
from threading import Thread
from User import User
from Login import Login
from Register import Register
from Graphic import Graphic
from Db import Db
import pyaudio

class Client:
    def __init__(self):
        # Server's IP address and port
        self.SERVER_HOST = "127.0.0.1"
        self.SERVER_PORT = 8080
        self.separator_token = "<SEP>" # Separator token for messages
        # Audio parameters
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        # Initialize TCP socket
        self.clientSocket = socket.socket()

        try:
            # Connect to the server
            self.clientSocket.connect((self.SERVER_HOST, self.SERVER_PORT))
            print("[+] Connected.")
        except Exception as e:
            print(f"Error connecting to the server: {e}")
            exit()

        # Get user information
        self.app = Login()
        self.app.windows.mainloop()
        user_info = self.app.userInfo
        if user_info == []:
            self.app = Register()
            self.app.windows.mainloop()
            user_info = self.app.userInfo
            self.client = User(user_info[0], user_info[1], user_info[2], user_info[3])
            self.app = Graphic(user_info[2])
        else:
            self.client = User(user_info[2], user_info[1], user_info[3], user_info[4])
            self.app = Graphic(user_info[3])

        self.client.clientSocket = self.clientSocket

        # Start listening for messages in a separate thread
        t1 = Thread(target=self.listen_for_messages)
        t1.daemon = True
        t1.start()

        # Set the "Send" button command to the handle_send_button function
        self.app.send_button.config(command=self.handle_send_button)
        self.app.text_rooms_menu.configure(command=self.handle_switch_channel)
        self.app.create_channel_button.config(command=self.handle_create_channel)

        self.app.show()
        

    def listen_for_messages(self):
        try:
            while True:
                message = self.clientSocket.recv(1024).decode()
                self.app.receive_message(message)
        except Exception as e:
            print(f"Error occurred while listening for messages: {e}")

    def send_message(self, message):
        # Add timestamp, name, and color to the message
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{self.client.channel}{self.separator_token}{date_now}{self.separator_token}{self.client.firstname}{self.separator_token}{self.client.lastname}{self.separator_token}{message}"
        print(to_send)

        # Send the message to the server
        self.clientSocket.send(to_send.encode())

    def handle_send_button(self):
        message = self.app.send_message()
        self.send_message(message)

    def handle_switch_channel(self, channel_name):
        channel_name = self.app.select_channel(channel_name)
        self.client.joinChannel(channel_name)
        self.send_message("<COMMAND>switch")

    def handle_create_channel(self):
        new_channel_name = self.app.create_channel()
        if new_channel_name:
            self.send_message(f"<COMMAND>create_channel | {new_channel_name}")
            self.handle_switch_channel(new_channel_name)
            self.app.text_rooms_menu.configure(command=self.handle_switch_channel)  # Update command
            self.app.text_rooms_menu.set(new_channel_name)

    # Function to send audio to the server
    def send_audio(self):
        print("Recording and sending audio...")
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        try:
            while self.is_recording:
                data = stream.read(self.CHUNK)
                self.clientSocket.sendall(data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            print("Audio stream stopped and closed.")

    def start_audio(self):
        self.is_recording = True
        self.send_audio()

    def stop(self):
        print("Stopping audio recording on vocal...")
        self.is_recording = False

        # Close the socket
        self.clientSocket.close()

if __name__ == "__main__":
    client = Client()
    client.start_audio()
