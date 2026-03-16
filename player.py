import socket
import struct
import sys
import json
import subprocess
import pygame
import os

def play(*args):
    if (len(args) != 3):
        return "In order to play you need 3 args: 1-> ip_multicast, 2-> udp_port, 3->instrument"
    
    mcIP = args[0]
    mcPort = int(args[1])
    instrument = args[2]

    pygame.mixer.init()

    #creates socket
    mcSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creates an UDP socket (by DGRAM) using IPv4 (by af_inet)
    mcSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #modifies sockets config, in this cases, allows to reuse same port
    mcSocket.bind(('', mcPort)) # listen on all interfaces

    # Join multicast group
    mreq = struct.pack("4sl", socket.inet_aton(mcIP), socket.INADDR_ANY) #create binary structure needed for ip_add_membership, converts 
    #our mc ip and any interface addr on the expected format for kernel
    mcSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) #joins the socket to the mc group, with our
    #mreq and the command IP_ADD_MEMBERSHIP

    #would it be desirable to have a high-level abstraction of multicast join for Python?
    #no, because python's sockets tries to be as close as possible to the actual sockets
    #OS API, in order to have a full compatibility between different systems and ensure full control of the sockets

    while True:
        dataRaw, addr = mcSocket.recvfrom(1024) #receive data from socket
        if not dataRaw:
            break
        data_str = dataRaw.decode('utf-8') #converts it to string so we can parse it
        try:
            data = json.loads(data_str) #parse JSON into dict
        except json.JSONDecodeError as e:
            print(f"There was an error: {e}") #if there's an error, prints it

        #gets note and file
        note = data["note"]
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        mp3_file = os.path.join(BASE_DIR, "notes", instrument, f"{note}.mp3")

        print(f"[Multicast Receiver] Received: {note}")
        print(f"Playing: {mp3_file}")

        #plays music
        try:
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing {mp3_file}: {e}")


if __name__ == "__main__":


    print(play(*sys.argv[1:]))
