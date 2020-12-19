import os
import socket
import json
import time

class ClientNetwork():
    def __init__(self, hostname, servername):
        self.buf = 1024
        self.hostname = hostname

        self.server_ip = servername

        self.udp_port = 13081
        self.udp_addr = (self.hostname,self.udp_port)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(self.udp_addr)
        self.udp_server = (self.server_ip,self.udp_port)

        self.tcp_port = 13082
        self.tcp_addr = (self.hostname,self.tcp_port)

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server = (self.server_ip,self.tcp_port)
        self.tcp_socket.connect(self.tcp_server)

    def send_udp(self,data):
        self.udp_socket.sendto(data.encode(),self.udp_server)

    def send_tcp(self,data):
        print(data.encode())
        self.tcp_socket.sendall(data.encode())

    def rcv_udp(self):
        data, addr = self.udp_socket.recvfrom(self.buf)
        data = data.decode()
        return data

    def rcv_tcp(self):
        data = self.tcp_socket.recv(self.buf)
        data = data.decode()
        return data

    def change_udp_server_addr(self,address):
        self.udp_server = (address,server[1])

    def change_tcp_server_addr(self,address):
        self.tcp_server = (address,server[1])

    def close_udp(self):
        self.udp_socket.close()

    def close_tcp(self):
        self.tcp_socket.close()

    def initialize_header(self, init_data):
        if not init_data:
            init_data = {
                "init": ["accelerometer", "velocity", "battery"]
            }
        data = json.dumps(init_data)
        self.send_tcp(data)
        print("recieved response", self.rcv_tcp())

    def set_direction(self, direction):
        print(f"setting direction to {direction}")
        data = {"direction": direction}
        send_data = json.dumps(data)
        self.send_udp(send_data)

if __name__ == "__main__":
    c = ClientNetwork("10.0.1.15", "10.0.1.24")
    c.initialize_header(None)
    time.sleep(2)
    c.set_direction(1)
    time.sleep(1)
    c.set_direction(0)
    time.sleep(1)
    c.set_direction(3)
    time.sleep(1)
    c.set_direction(7)
    time.sleep(1)
    c.set_direction(0)
