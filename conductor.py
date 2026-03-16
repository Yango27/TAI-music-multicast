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

    #what would happen if the execution of the code stops before closing the sockets?
    #in this case, we are on UDP, so, if the sockets are not close there's not a big problem,
    #it would almos inmediately liberate the ports so it would be reusable
    #but we are in multicast, its possible that the kernel would still register our socket as active even if its not

    #if it was TCP we would encounter that the port is ocuppied for a few minutes, 
    #thats because TCP has a handshake, which ensures that the connection is fully closed from both sides
    #if the execution stops before closing tcp would mantain the port used for a few minutes, which
    #would avoid other programs to use these ports.

if __name__ == "__main__":

    startMusic(*sys.argv[1:])

