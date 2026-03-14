import socket
import time
import struct
import sys
import json
import subprocess
import pygame

def send_message(sock, ip, port, note):
    message = {"note": note}
    data = json.dumps(message).encode("utf-8")
    sock.sendto(data, (ip, port))

def startMusic(*args):
    if len(args) != 4:
        return "In order to start music you need 4 args: 1-> ip_multicastA, 2-> ip_multicastB, " \
        "3->ip_multicastC, 4-> port_multicast"
    mcIPA = args[0]
    mcIPB = args[1]
    mcIPC = args[2]
    mcPort = int(args[3])

    udpSocketA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocketB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocketC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sequences = [
        ("c", "e", "g"),
        ("c", "e", "a"),
        ("d", "f", "a"),
        ("d", "b", "g"),
    ]

    for notes in sequences:
        send_message(udpSocketA, mcIPA, mcPort, notes[0])
        send_message(udpSocketB, mcIPB, mcPort, notes[1])
        send_message(udpSocketC, mcIPC, mcPort, notes[2])

        print("Notes enviades.")
        time.sleep(1)

    udpSocketA.close()
    udpSocketB.close()
    udpSocketC.close()

if __name__ == "__main__":

    mcIPA = input("Multicast IPA: ")
    mcIPB = input("Multicast IPB: ")
    mcIPC = input("Multicast IPC: ")
    mcPort = input("Multicast Port: ")

    startMusic(mcIPA, mcIPB, mcIPC, mcPort)

