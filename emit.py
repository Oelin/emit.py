#!/usr/bin/env python3

'''emit(1), interact with a process over TCP.

emit [port] [command]'''



from socket import socket
from sys import argv
from subprocess import Popen


# Open a process with a specific file descriptor for I/O.

def popen(command, fd):
    # Both stdin, stdout and stderr are set to the same
    # descriptor. 

    flags = (command, 0, None, fd, fd, fd)

    # Actually open the process with a system call.

    proc = Popen(*flags)

    return proc


# Attach a process to a socket by equating respective I/O
# file descriptors. This creates a weird pipe-ish thing.

def link(command, socket):
    fd = socket.fileno()

    proc = popen(command, fd)

    return proc



# Create a new socket and listen on a given port. When a 
# peer connects, attach their socket to a certain process.

def listen(port, command):
    server = socket()

    server.bind(('', port))
    server.listen(5)

    while True:
        # Accept a peer connection also as socket object.
        # Then attempt to attach it to the target process.

        client, info = server.accept()
        link(command, client)

        # Their socket should fall back on the process' I/O
        # streams.

        client.close()
       
    server.close()



def main():
    if len(argv) == 3:
        # Extract command line arguments if enough given.

        port = int(argv[1])
        command = argv[2]

        # Listen for peer connections to attach to.

        listen(port, command)

    # If an incorrect number of arguments are given, output
    # the docstring for help.

    else:
        print(__doc__)



main()
