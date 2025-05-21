# script that accepts motor commands and forwards them to the motors via UART

import serial
import socket

HOST = "0.0.0.0"
PORT = 2000  # we are using port 2000 to communicate
MAX_MSG_SIZE = 1024  # max 1024 bytes

"""
@brief sends a message over UART
@param message the message to send
"""
def send_to_uart(msg: bytes) -> None:
    print(f"Sending {msg} over UART")

"""
@brief processes a message received
@param message the message we received
@return what we should send back in response to this message
"""
def process_message(msg: bytes) -> bytes:
    if msg == b'OFF':
        send_to_uart((0).to_bytes(1, signed=False))
    elif msg == b'LEFT':
        send_to_uart((1).to_bytes(1, signed=False))
    elif msg == b'RIGHT':
        send_to_uart((2).to_bytes(1, signed=False))
    elif msg == b'UP':
        send_to_uart((3).to_bytes(1, signed=False))
    elif msg == b'DOWN':
        send_to_uart((4).to_bytes(1, signed=False))
    else:
        print(f"Unrecognized message: {msg}")
    return None


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        try:
            while True:
                    conn, addr = sock.accept()
                    with conn:  # connection created
                        while True:
                            data = None
                            try:
                                data = conn.recv(MAX_MSG_SIZE)
                            except ConnectionResetError as e:
                                data = None
                            if not data:
                                print("Client disconnected")
                                break
                            response = process_message(data)
                            if data:
                                conn.sendall(data)
        except KeyboardInterrupt as e:
            sock.close()
            print("Shutting down server")
except Exception as e:
    pass

# make sure to turn off the motors here
