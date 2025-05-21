# script that accepts motor commands and forwards them to the motors via UART

import serial
import socket

HOST = "127.0.0.1"
PORT = 2000  # we are using port 2000 to communicate
MAX_MSG_SIZE = 1024  # max 1024 bytes

"""
@brief processes a message received
@param message the message we received
@return what we should send back in response to this message
"""
def process_message(message: bytes) -> bytes:
    print(message)
    # replace with actual processing
    return message

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    try:
        while True:
            conn, addr = sock.accept()
            with conn:  # connection created
                while True:
                    data = conn.recv(MAX_MSG_SIZE)
                    if not data:
                        print("Client disconnected")
                        break
                    response = process_message(data)
                    if data:
                        conn.sendall(data)
    except KeyboardInterrupt as e:
        print("Shutting down server...")
