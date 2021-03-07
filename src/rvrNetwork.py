# Add ability to communicate with laptop via udp and tcp
# Needs to establish udp and tcp
# Needs class to send and recieve data that main loop can use

import sys
import socket
from threading import Thread
from vprint import vprint
import traceback
import asyncio
import json


header = [
    # list of possible items to send back
    "time",
    "accelerometer",
    "locator",
    "velocity",
    "gyro",
    "battery"
]


class NetworkServer():
    def __init__(self, myRVR, hostMAC, control_port, data_port):
        self.myRVR = myRVR
        self.host = "10.0.1.24"
        self.tcp_status = [0, 1, 2]
        # 0 = no data 1= currently adding data 2=data ready
        self.udp_port = 13081
        self.tcp_port = 13082
        self.udp_rcv_data = None
        self.tcp_rcv_data = None

        self.data_read = False
        self.control_read = False
        # if udp data has been read make true, once updated make false

        self.data_timeout = 1
        self.control_timeout = 3

        self.udp_send_data = None
        self.tcp_send_data = None

        self.control_buff = 1024
        self.data_buff = 1024

        self.data_close = False
        self.control_close = False

        self.client = None

        self.hostMAC = hostMAC
        self.control_port = control_port
        self.data_port = data_port

    def start_control_bluetooth(self):
        self.bt_control_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.bt_control_socket.bind((self.hostMAC, self.control_port))
        self.bt_control_socket.settimout(self.control_timeout)

        while not self.control_close:
            try:
                self.connect_control()
            except socket.timeout:
                vprint("control bluetooth timeout")

    def connect_control(self):
        self.bt_control_socket.listen()
        try:
            client, address = self.bt_control_socket.accept()
            while not self.control_close:
                data = client.recv(self.control_buff).decode()
                if data:
                    self.control_rcv_data = data
                    self.control_read = False
                else:
                    vprint("Bad control data, reconnecting")
                    break
        except socket.timeout as e:
            raise e

    def stop_server_control(self):
        try:
            self.control_close = True
            time.sleep(self.control_timeout)
            self.bt_control_socket.close()
        except NameError:
            vprint("control socket not created")
        except Exception as e:
            vprint("Error in activation. Exception: ", e)

    def start_data_bluetooth(self):
        self.bt_data_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.bt_data_socket.bind((self.MAC, self.data_port))
        self.bt_data_socket.settimout(self.data_timeout)

        while not self.data_close:
            try:
                client, address = self.init_data()
                if not client:
                    continue
                self.connect_data(client, address)
            except socket.timeout:
                vprint("data bluetooth timeout")

    def connect_data(self, client, address):
        try:
            while not self.data_close:
                if self.data_send_data:
                    client.sendall(self.data_send_data)
        except socket.timeout as e:
            raise e

    def init_data(self):
        self.bt_data_socket.listen()
        client, address = self.bt_data_socket.accept()
        data = client.recv(self.data_buff).decode()
        if data:
            self.data_rcv_data = data
            self.data_read = False
            init_msg = "initialized"
            client.sendall(init_msg.encode())
            break
        else:
            vprint("Bad data data, reconnecting")
            return None, None
        return client, address

    def stop_server_data(self):
        try:
            self.data_close = True
            time.sleep(self.data_timeout)
            self.bt_data_socket.close()
        except NameError:
            vprint("data socket not created")
        except Exception as e:
            vprint("Error in activation. Exception: ", e)

    def start_servers(self):
        vprint("Starting Servers")
        try:
            self.control_thread = Thread(target=self.start_control_bluetooth)
            self.control_thread.start()
            self.data_thread = Thread(target=self.start_data_bluetooth)
            self.data_thread.start()
        except Exception as e:
            vprint("Failed to create threads: ")
            vprint(e)
            self.myRVR.set_color("NETERR")
            raise e

    async def get_init_data(self):
        loop = True
        send_list = []
        while loop:
            if not self.data_rcv_data:
                await asyncio.sleep(0.05)
                continue
            vprint("recieved data")
            data = json.loads(self.data_rcv_data)

            try:
                id = data["init"]
            except KeyError:
                vprint("no id found in json object")
                await asyncio.sleep(0.25)
                continue
            except Exception as e:
                vprint("Error in activation. Exception: ", e)

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
        if self.control_rcv_data:
            self.control_read = True
            message = json.loads(self.control_rcv_data)
            if "direction" in list(message.keys()):
                direction = message["direction"]
                if direction >= 0 and direction <= 8:
                    return direction
            else:
                vprint("Direction command not found")
                return 0
