#Add ability to communicate with laptop via udp and tcp
#Needs to establish udp and tcp
#Needs class to send and recieve data that main loop can use
import sys
import socket
from threading import Thread
from vprint import vprint
import traceback
import asyncio
import json


udp_buff = 1024   #size of buffer/chunk of data that udp recieves. Needs to be
tcp_buff = 1024   #size of buffer/chunk of data that tcp recieves
                #larger than incoming data packet

header = [      #list of possible items to send back
    "time",
    "accelerometer",
    "locator",
    "velocity",
    "gyro",
    "battery"
]

class NetworkServer():
    def __init__(self, myRVR):
        self.myRVR = myRVR
        self.host = "10.0.1.24"
        self.tcp_status = [0,1,2] #0 = no data 1= currently adding data 2=data ready
        self.udp_port = 13081
        self.tcp_port = 13082
        self.udp_rcv_data = None
        self.tcp_rcv_data = None
        self.udp_read = False
        self.tcp_read = False   #if udp data has been read make true, once updated make false

        self.udp_timeout = 1
        self.tcp_timeout = 1

        self.udp_send_data = None
        self.tcp_send_data = None
        self.udp_close = False
        self.tcp_close = False

        self.client = None


    def start_servers(self):
        vprint("Starting Servers")
        try:
            self.udp_thread = Thread(target=self.start_server_udp)
            self.udp_thread.start()
            self.tcp_thread = Thread(target=self.start_server_tcp)
            self.tcp_thread.start()
        except Exception as e:
            vprint("Failed to create threads: ")
            vprint(e)

    def start_server_udp(self):
        global udp_buff
        """Attempt to create a udp socket and bind to port"""
        try:
            self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.udp_socket.bind((self.host,self.udp_port))
            self.udp_socket.settimeout(self.udp_timeout)
        except Exception as e:
            vprint("Error creating udp server")
            vprint(e)
            self.myRVR.set_color("NETERR")

        while not self.udp_close:
            """get recieved message from udp"""
            try:
                message, address = self.udp_socket.recvfrom(udp_buff)
            except socket.timeout:
                vprint("UDP timeout")
                continue

            self.udp_rcv_data = message.decode()
            self.udp_read = False
            #vprint(message.decode())

            """test if client is from previous client"""
            if str(address) is not str(self.client):
                self.client = address

            """If there is data to be sent over udp, send it"""
            if self.udp_send_data is not None:
                self.udp_socket.sendto(self.udp_send_data.encode(),address)
        vprint("udp socket closed")

    def stop_server_udp(self):
        try:
            self.udp_close = True
            self.udp_socket.close()
        except NameError:
            vprint("udp socket not created")
        except Exception as e:
            vprint("Error in activation. Exception: ",e)


    def start_server_tcp(self):
        """Attempt to create a udp socket and bind to port"""
        try:
            self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.tcp_socket.bind((self.host,self.tcp_port))
            self.tcp_soclet.settimeout(self.tcp_timeout)
        except Exception as e:
            vprint("Error creating tcp server")
            vprint(e)
            self.myRVR.set_color("NETERR")

        while not self.tcp_close:
            self.connect_tcp()

    def connect_tcp(self):
        global tcp_buff
        self.tcp_socket.listen()
        connection, address = self.tcp_socket.accept()
        if address is not self.client:
            self.client = address
            vprint("updating client address")

        while not self.tcp_close:
            vprint("listening")
            try:
                data = connection.recv(tcp_buff).decode()
            except socket.timeout:
                vprint("TCP timeout")
            if data:
                self.tcp_rcv_data = data
            else:
                 vprint("conection closed by client. Attempting to reestablish connection")
                 break

            self.tcp_send_data = "howdy partner"
            if self.tcp_send_data:
                connection.sendall(self.tcp_send_data.encode())
                self.tcp_send_data = None

    def stop_server_tcp(self):
        try:
            self.tcp_close = True
            self.tcp_socket.close()
        except NameError:
            vprint("udp socket not created")
        except Exception as e:
            vprint("Error in activation. Exception: ",e)


    async def get_init_tcp(self):
        loop = True
        send_list = []
        while loop:
            if not self.tcp_rcv_data:
                await asyncio.sleep(0.25)
                continue
            vprint("recieved data")
            data = json.loads(self.tcp_rcv_data)

            try:
                 id = data["init"]
            except KeyError:
                vprint("no id found in json object")
                await asyncio.sleep(0.25)
                continue
            except Exception as e:
                vprint("Error in activation. Exception: ",e)

            for x in id:
                if x in header:
                    send_list.append(x)

            vprint(send_list)

            self.tcp_read = True
            return send_list

    def stop_networks(self):
        self.stop_server_tcp()
        self.stop_server_udp()


    def get_direction(self):
        if self.udp_rcv_data:
            self.udp_read = True
            message = json.loads(self.udp_rcv_data)
            if "direction" in list(message.keys()):
                direction = message["direction"]
                if direction >= 0 and direction <= 8:
                    return direction
            else:
                vprint("Direction command not found")
                return 0
