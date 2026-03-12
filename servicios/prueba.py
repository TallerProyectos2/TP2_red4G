import os
import socket
import struct
import pickle
import cv2
import time
from pynput import keyboard
import numpy as np
import cmath
import math

BIND_IP = os.getenv("TP2_BIND_IP", "172.16.0.1")
BIND_PORT = int(os.getenv("TP2_BIND_PORT", "20001"))
server_address = (BIND_IP, BIND_PORT)

control_acelerador = 0
control_giro = 0


def on_press(key):
    global control_acelerador
    global control_giro
    if key == keyboard.KeyCode.from_char("2"):
        control_acelerador = 1
    if key == keyboard.KeyCode.from_char("w"):
        control_acelerador = 0.6
    if key == keyboard.KeyCode.from_char("s"):
        control_acelerador = -0.5
    if key == keyboard.KeyCode.from_char("x"):
        control_acelerador = -0.9
    if key == keyboard.KeyCode.from_char("a"):
        control_giro = 1
    if key == keyboard.KeyCode.from_char("d"):
        control_giro = -1


def on_release(key):
    global control_acelerador
    global control_giro
    if key == keyboard.KeyCode.from_char("2"):
        control_acelerador = 0
    if key == keyboard.KeyCode.from_char("w"):
        control_acelerador = 0
    if key == keyboard.KeyCode.from_char("s"):
        control_acelerador = 0
    if key == keyboard.KeyCode.from_char("x"):
        control_acelerador = 0
    if key == keyboard.KeyCode.from_char("a"):
        control_giro = 0.25
    if key == keyboard.KeyCode.from_char("d"):
        control_giro = 0.25


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


def send_control(control_giro, control_acelerador, address):
    sock.sendto(
        struct.pack("c", bytes("C", "ascii"))
        + struct.pack("d", round(control_giro, 3))
        + struct.pack("d", round(control_acelerador, 3)),
        address,
    )


if __name__ == "__main__":
    received_payload = b""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    print(f"Manual control server listening on {server_address[0]}:{server_address[1]}")

    while True:
        data, address = sock.recvfrom(99999)
        data_type = struct.unpack("c", bytes([data[0]]))[0]
        received_payload = bytes(data[1:])
        data = pickle.loads(received_payload, encoding="latin1")

        if data_type == b"I":
            img = cv2.imdecode(data, 1)
            cv2.imshow("Coche ARTEMIS", img)
            cv2.waitKey(1)
            send_control(control_giro, control_acelerador, address)
        if data_type == b"D":
            pass
        if data_type == b"L":
            img_lidar = np.zeros((480, 640, 3), np.uint8)
            i = 0
            ranges = data
            for range_value in ranges:
                z_value = cmath.rect(range_value, math.radians(-i - 90))
                i = i + 1
                if z_value.real != float("inf") and z_value.real != float("-inf"):
                    x = int(z_value.real * 70) + 320
                else:
                    x = 0
                if z_value.imag != float("inf") and z_value.imag != float("-inf"):
                    y = int(z_value.imag * 70) + 240
                else:
                    y = 0
                cv2.circle(img_lidar, (x, y), radius=2, color=(0, 0, 255), thickness=2)

            cv2.imshow("Mapa LIDAR", img_lidar)
            cv2.waitKey(1)
