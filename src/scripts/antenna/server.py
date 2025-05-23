# script that accepts motor commands and forwards them to the motors via UART

from serial import Serial
from threading import Thread, Lock
import time
import socket

serial_lock = Lock()
SERIAL_PATH = "/dev/serial0"
BAUD_RATE = 9600  # 115200

HOST = "0.0.0.0"
PORT = 2000  # we are using port 2000 to communicate
MAX_MSG_SIZE = 1024  # max 1024 bytes

status_lock = Lock()
motors_status = {
    'pitch': 0,
    'spin': 0,
}

"""
@brief updates the motor speeds via UART
@param ser the UART connection to send commands to
"""
def update_motors(ser: Serial) -> None:
    while enable_motor_thread:
        with status_lock:
            if motors_status['spin'] == 1:
                send_to_uart(b'a', ser)
            elif motors_status['spin'] == -1:
                send_to_uart(b'd', ser)

            if motors_status['pitch'] == 1:
                send_to_uart(b'w', ser)
            elif motors_status['pitch'] == -1:
                send_to_uart(b's', ser)

        time.sleep(.025)

"""
@brief sends a message over UART
@param message the message to send
"""
def send_to_uart(msg: bytes, ser: Serial) -> None:
    print(f"Sending {msg} over UART")
    with serial_lock:
        ser.write(msg)

"""
@brief processes a message received
@param message the message we received
@return what we should send back in response to this message
"""
def process_message(msg: bytes) -> bytes:
    with status_lock:
        if msg == b'OFF':
            motors_status['pitch'] = 0
            motors_status['spin'] = 0
        elif msg == b'LEFT':
            motors_status['spin'] = 1
        elif msg == b'RIGHT':
            motors_status['spin'] = -1
        elif msg == b'UP':
            motors_status['pitch'] = 1
        elif msg == b'DOWN':
            motors_status['pitch'] = -1
        else:
            print(f"Unrecognized message: {msg}")
    return None

ser = Serial(SERIAL_PATH, BAUD_RATE)

enable_motor_thread = True
motor_thread = Thread(target = update_motors, args=(ser, enable_motor_thread))
motor_thread.start()

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
            print("Shutting down server")
            sock.close()
            enable_motor_thread = False
            motor_thread.join()
except Exception as e:
    print(e)

if enable_motor_thread:
    enable_motor_thread = False
    motor_thread.join()

if ser.is_open:
    ser.close()
