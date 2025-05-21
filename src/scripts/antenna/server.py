# script that accepts motor commands and forwards them to the motors via UART

from serial import Serial
import socket

UART_PATH = "/dev/serial0"

HOST = "0.0.0.0"
PORT = 2000  # we are using port 2000 to communicate
MAX_MSG_SIZE = 1024  # max 1024 bytes

"""
@brief sends a message over UART
@param message the message to send
"""
def send_to_uart(msg: bytes, ser: Serial) -> None:
    print(f"Sending {msg} over UART")
    ser.write(msg)

"""
@brief processes a message received
@param message the message we received
@return what we should send back in response to this message
"""
def process_message(msg: bytes, ser: Serial) -> bytes:
    if msg == b'OFF':
        send_to_uart((0).to_bytes(1, signed=False), ser)
    elif msg == b'LEFT':
        send_to_uart((1).to_bytes(1, signed=False), ser)
    elif msg == b'RIGHT':
        send_to_uart((2).to_bytes(1, signed=False), ser)
    elif msg == b'UP':
        send_to_uart((3).to_bytes(1, signed=False), ser)
    elif msg == b'DOWN':
        send_to_uart((4).to_bytes(1, signed=False), ser)
    else:
        print(f"Unrecognized message: {msg}")
    return None

ser = Serial(UART_PATH)

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
                            response = process_message(data, ser)
                            if data:
                                conn.sendall(data)
        except KeyboardInterrupt as e:
            print("Shutting down server")
            sock.close()
            ser.close()
except Exception as e:
    print(e)

# turn off motors
ser.write(b'\00')
