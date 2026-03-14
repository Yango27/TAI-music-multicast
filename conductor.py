import socket
import time
import struct
import sys
import json
import subprocess
import pygame

def send_message(sock, ip, port, note):
    #we create a dict with a pair key called note with value note to play
    message = {"note": note}
    data = json.dumps(message).encode("utf-8") #serialize message into json
    sock.sendto(data, (ip, port)) #send the json data to a specific ip and port through a socket

def startMusic(*args):
    if len(args) != 4:
        return "In order to start music you need 4 args: 1-> ip_multicastA, 2-> ip_multicastB, " \
        "3->ip_multicastC, 4-> port_multicast"
    
    mcIPA = args[0]
    mcIPB = args[1]
    mcIPC = args[2]
    mcPort = int(args[3])

    #creates sockets, every socket representing a multicast group
    udpSocketA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocketB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocketC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #define sequence to play
    sequences = [
        ("c", "e", "g"),
        ("c", "e", "a"),
        ("d", "f", "a"),
        ("g", "b", "d"),
    ]

    for notes in sequences:
        #sends note to every socket
        send_message(udpSocketA, mcIPA, mcPort, notes[0])
        send_message(udpSocketB, mcIPB, mcPort, notes[1])
        send_message(udpSocketC, mcIPC, mcPort, notes[2])

        print("Notes enviades.")
        time.sleep(1)
    
    #closing sockets
    udpSocketA.close()
    udpSocketB.close()
    udpSocketC.close()

if __name__ == "__main__":

    mcIPA = input("Multicast IPA: ")
    mcIPB = input("Multicast IPB: ")
    mcIPC = input("Multicast IPC: ")
    mcPort = input("Multicast Port: ")

    startMusic(mcIPA, mcIPB, mcIPC, mcPort)

