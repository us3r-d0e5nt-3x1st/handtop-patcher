#!/usr/bin/env python3

import configparser
import os
import sys
import termios
import time

CONFIG = "/home/rg/.config/joystick-leds/settings.conf"
LED_BRIGHTNESS = "/sys/class/leds/rgb:kbd_backlight/brightness"


def load_config():
    cfg = configparser.ConfigParser()

    if not cfg.read(CONFIG):
        raise RuntimeError(f"Cannot read configuration: {CONFIG}")

    section = cfg["leds"]

    brightness = section.getint("brightness", 255)
    right = section.get("right", "#8000FF")
    left = section.get("left", "#8000FF")
    device = section.get("device", "/dev/ttyS2")
    baudrate = section.getint("baudrate", 115200)

    if not 0 <= brightness <= 255:
        raise ValueError("Brightness must be 0-255")

    if baudrate != 115200:
        raise ValueError("Only 115200 baud is supported")

    def parse_rgb(value):
        value = value.strip().removeprefix("#")

        if len(value) != 6:
            raise ValueError(f"Invalid RGB color: {value}")

        try:
            rgb = tuple(bytes.fromhex(value))
        except ValueError:
            raise ValueError(f"Invalid RGB color: {value}")

        return rgb

    return brightness, parse_rgb(right), parse_rgb(left), device


def build_packet(brightness, right, left):
    # Mode + brightness
    packet = bytearray([1, brightness])

    # Right analog: 8 RGB repetitions
    for _ in range(8):
        packet.extend(right)

    # Left analog: 8 RGB repetitions
    for _ in range(8):
        packet.extend(left)

    # Checksum: sum of all preceding bytes modulo 256
    packet.append(sum(packet) & 0xFF)

    assert len(packet) == 51

    return bytes(packet)


def enable_leds():
    with open(LED_BRIGHTNESS, "w") as f:
        f.write("1")


def configure_uart(fd):
    attrs = termios.tcgetattr(fd)

    # Match the important settings used by ROCKNIX stty:
    # 115200 baud, no output processing, no signals,
    # no canonical mode and no echo.
    attrs[1] &= ~termios.OPOST
    attrs[2] = (attrs[2] & ~termios.CSIZE) | termios.CS8
    attrs[2] |= termios.CLOCAL | termios.CREAD
    attrs[3] &= ~(termios.ISIG | termios.ICANON | termios.ECHO)

    attrs[4] = termios.B115200
    attrs[5] = termios.B115200

    termios.tcsetattr(fd, termios.TCSANOW, attrs)


def send_packet(device, packet):
    fd = os.open(device, os.O_RDWR | os.O_NOCTTY)

    try:
        configure_uart(fd)

        time.sleep(0.05)

        # Enable the RGB controller through kernel LED interface.
        enable_leds()

        # Send the complete packet, handling partial writes.
        offset = 0

        while offset < len(packet):
            written = os.write(fd, packet[offset:])

            if written <= 0:
                raise RuntimeError("UART write failed")

            offset += written

        termios.tcdrain(fd)

    finally:
        os.close(fd)


def main():
    brightness, right, left, device = load_config()

    packet = build_packet(brightness, right, left)

    print("Joystick RGB controller")
    print(f"UART: {device}")
    print(f"Brightness: {brightness}")
    print(f"Right: {right}")
    print(f"Left: {left}")
    print(f"Packet: {len(packet)} bytes")
    print(f"Checksum: 0x{packet[-1]:02X}")

    send_packet(device, packet)

    print("RGB configuration sent successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
