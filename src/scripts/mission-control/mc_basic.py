import tkinter as tk
import socket
from threading import Lock

def send_message(conn: socket.socket, msg: bytes, mut: Lock) -> None:
    try:
        with mut:
            conn.sendall(msg)
    except BrokenPipeError as e:
        print("Unexpectedly disconnected from server.")
        conn.close()
        raise e

HOST = "raspberrypi.local"  # connect to raspberry pi
# HOST = "localhost"  # uncomment to connect to local server
PORT = 2000

sock_mutex = Lock()
# start connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def on_button_release(event):
    global sock_mutex
    global sock
    print("Turning off motors")
    send_message(sock, b'OFF', sock_mutex)

def on_left_press(event):
    global sock_mutex
    global sock
    print("Sending left turn")
    send_message(sock, b'LEFT', sock_mutex)

def on_right_press(event):
    global sock_mutex
    global sock
    print("Sending right turn")
    send_message(sock, b'RIGHT', sock_mutex)

def on_up_press(event):
    global sock_mutex
    global sock
    print("Sending up turn")
    send_message(sock, b'UP', sock_mutex)

def on_down_press(event):
    global sock_mutex
    global sock
    print("Sending down turn")
    send_message(sock, b'DOWN', sock_mutex)


root = tk.Tk()
root.geometry("450x500")
left_button = tk.Button(root, text="Left", width=10, height=5)
left_button.bind("<Button-1>", on_left_press)
left_button.bind("<ButtonRelease-1>", on_button_release)
left_button.place(x=50, y=200)

right_button = tk.Button(root, text="Right", width=10, height=5)
right_button.bind("<Button-1>", on_right_press)
right_button.bind("<ButtonRelease-1>", on_button_release)
right_button.place(x=285, y=200)

up_button = tk.Button(root, text="Up", width=10, height=5)
up_button.bind("<Button-1>", on_up_press)
up_button.bind("<ButtonRelease-1>", on_button_release)
up_button.place(x=170, y=100)

down_button = tk.Button(root, text="Down", width=10, height=5)
down_button.bind("<Button-1>", on_down_press)
down_button.bind("<ButtonRelease-1>", on_button_release)
down_button.place(x=170, y=300)

try:
    root.mainloop()
except KeyboardInterrupt as e:
    print("Disconnecting from Antenna server")
    sock.close()
