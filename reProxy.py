import os, sys, socket,time
import _thread as thread
import tkinter as tk
from tkinter import *

BACKLOG = 200
# Max number of bytes to receive at once?
MAX_DATA_RECV = 4096
# Set true if you want to see debug messages.
DEBUG = True
# Dict to store the blocked URLs
blocked = {}
# Dict to act as a cache, stores responses.
cache = {}
# Dict to store time of response before caching.
timings = {}

def main():
    listeningPort = 8000

    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('',listeningPort))
        s.listen((BACKLOG))
        print("[*] Initializing sockets... done")
        print("[*] Sockets binded successfully...")
        print("[*] Server started successfully [ %d ]\n" % (listeningPort))
    except Exception:
        print("[*] Unable to initalize socket...")
        sys.exit(2)

    while True:
        try:
            conn, client_addr = s.accept()
            data = conn.recv(MAX_DATA_RECV)
            conn_string(conn,data,client_addr)
        except KeyboardInterrupt:
            s.close()
            print("Shutting Down...")
            sys.exit(1)
    s.close()

def conn_string(conn,data,client_addr):
    print('Here3')
    first_line = str(data).split('\n')[0]
    print(first_line)
    url = first_line.split(' ')[1]
    print(url)
    method = first_line.split(' ')[0]
    print(method)
    try:
        print('Here3')
        first_line = data.split('\n')[0]
        print(first_line)
        url = first_line.split(' ')[1]
        print(url)
        method = first_line.split(' ')[0]
        print(method)

        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos+3):]
        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver =""
        port = -1
        if (port_pos ==-1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        print(port)
        print(webserver)
        proxy_server(webserver,port,conn,client_addr,data)
    except Exception:
        pass
def proxy_server(webserver, port,conn,client_addr,data):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((webserver,port))
        s.send(data)

        while 1:
            reply = s.recv(8192)
            if (len(reply) > 0):
                conn.send(reply)
                rep = float(len(reply))
                rep = float(rep/1024)
                rep = "%.3s" % (str(rep))
                print("[*] request done: ")
            else:
                break
        s.close()
        conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit(1)

if __name__ == '__main__':
    main()