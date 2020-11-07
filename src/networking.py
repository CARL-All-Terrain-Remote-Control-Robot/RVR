#Add ability to communicate with laptop via udp and tcp
#Needs to establish udp and tcp
#Needs class to send and recieve data that main loop can use
import sys
import socket
from threading import Thread
from carlraspirvr import vprint
import traceback

udp_buff = 1024   #size of buffer/chunk of data that udp recieves. Needs to be
tcp_buff = 1024   #size of buffer/chunk of data that tcp recieves
                #larger than incoming data packet
class NetworkServer():
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.self.tcp_status = [0,1,2] #0 = no data 1= currently adding data 2=data ready
        self.udp_rcv_data = self.tcp_rcv_data = None
        self.udp_read = False   #if udp data has been read make true, once updated make false
        self.udp_send_data = self.tcp_send_data = None
        self.udp_close = self.tcp_close = False

        self.client = None

        try:
            self.udp_thread = Thread(target=start_server_udp)
            self.udp_thread.start()
            #Thread(target=start_server_tcp).start()
        except:
            vprint("Failed to create threads")

    def start_server_udp(self):
        global udp_buff
        """Attempt to create a udp socket and bind to port"""
        try:
            self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.udp_socket.bind((self.host,0))
            self.udp_port = udp_socket.getsockname()[1]
        except:
            vprint("Error creating udp server")

        while not self.udp_close:
            """get recieved message from udp"""
            message, address = self.udp_socket.rcvfrom(udp_buff)
            self.udp_rcv_data = message.decode()
            self.udp_read = False

            """test if client is from previous client"""
            if address is not self.client:
                self.client = address
                vprint("updating client")

            """If there is data to be sent over udp, send it"""
            if self.udp_send_data is not None:
                self.udp_socket.sendto(self.udp_send_data.encode(),address)

    def stop_server_udp(self):
        try:
            self.udp_close = True
            self.udp_socket.close()
        except NameError:
            vprint("udp socket not created")
        vprint("udp socket closed")


    def recieve_input_udp(self):

    def start_server_tcp(self):
        """Attempt to create a udp socket and bind to port"""
        try:
            self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.tcp_socket.bind((self.host,0))
            self.tcp_port = udp_socket.getsockname()[1]
        except:
            vprint("Error creating udp server")

        while not self.tcp_close:
            self.connect_tcp()


    def connect_tcp(self):
        tcp_socket.listen()
        connection, address = self.tcp_socket.accept()
        if address is not self.client:
            self.client = address
            vprint("updating client address")

        while not self.tcp_close:
            self.tcp_rcv_data = connection.recv(tcp_buff).decode()

            if not self.tcp_rcv_data:
                 vprint("conection closed by client. Attempting to reestablish connection")
                 break






    def stop_server_tcp(self):

    def client_thread_tcp(self):
    def recieve_input_tcp(self):
