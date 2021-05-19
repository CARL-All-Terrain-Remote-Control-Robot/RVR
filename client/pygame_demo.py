import pygame
import pygame.freetype
#import pygameGui
import os
import socket
import json

###

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
        ##I don't see a server variable anywhere, but it may also be in separate code
        ##altenratively, any chance it should be "self.udp_port"?
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
        data = {"direction": direction}
        send_data = json.dumps(data)
        self.send_udp(send_data)

###

AVAILABLE_DIAGNOSTICS = {"Displayed Values:": False,
                         "GPS":True,
                         "Acceleration":True,
                         "Battery":True,
                         "Speed":True,
                         "Temperature":True,
                         "Motor":True}

direction_dict = {10: "Back",
                  0: '',
                  -10: "Forward",
                  -1: "Left",
                  1: "Right"}

pygame.init()

pygame.display.set_caption('pygame_demo')

screen = pygame.display.set_mode([1000, 500])

## Base font
myfont = pygame.font.SysFont('Helvetica', 20)

## Altered font effect to provide a cue for which line the user is on
alteredfont = pygame.font.SysFont('Helvetica', 20)
alteredfont.set_underline(True)

space = myfont.get_linesize()

cursor_vertical_pos = 1
cursor_horizontal_pos = 1
enter_hit = False

running = True

startup = True
host_name = ''
server_name = ''
default_host = ''
default_server = ''

c = None

pygame.key.set_repeat(500, 50)
## Main loop; Uses a keydown check to manage a cursor lock to avoid unintentionally
## skipping past when navigating. The lock is not release until the keyup is detected
## for the key that initiated the lock
while running:
    if startup:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                if c != None:
                    c.close_udp()
                    c.close_tcp()
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if (cursor_vertical_pos + 1) < 4:
                        cursor_vertical_pos += 1

                elif event.key == pygame.K_UP:
                    if (cursor_vertical_pos - 1) >= 1:
                        cursor_vertical_pos -= 1

                elif event.key == pygame.K_RETURN:
                    if cursor_vertical_pos < 3:
                        cursor_vertical_pos += 1
                    elif cursor_vertical_pos == 3:
                        startup = False
                        cursor_vertical_pos = 1
                        ##if no connection exists, create it (or default)
                        if c == None:
                            if (host_name != '') and (server_name != ''):
                                c = ClientNetwork(host_name, server_name)
                            else:
                                #c = ClientNetwork("10.0.1.15", "10.0.1.14")
                                c = None
                        else:
                            pass
                            #c.change_tcp_server_addr()
                            #c.change_udp_server_addr()
                        ##if one already exists, close it, then create the new one with the specified addresses

                elif event.key == pygame.K_BACKSPACE:
                    if cursor_vertical_pos == 1:
                        if (len(host_name) > 0):
                            host_name = host_name[:-1:]
                    elif cursor_vertical_pos == 2:
                        if (len(server_name) > 0):
                            server_name = server_name[:-1:]

                elif event.key in {pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_PERIOD}:
                    if cursor_vertical_pos == 1:
                        host_name += event.unicode
                    elif cursor_vertical_pos == 2:
                        server_name += event.unicode


        keys = pygame.key.get_pressed()
        #print(keys)
        #if highlighted, use the gray background
        if cursor_vertical_pos == 1:
            host_text = myfont.render("Host name", True, (255, 255, 255), (128, 128, 128))
        else:
            host_text = myfont.render("Host name", True, (255, 255, 255))

        host_width, host_height = myfont.size("Host_name")

        if cursor_vertical_pos == 2:
            server_text = myfont.render("Server name", True, (255, 255, 255), (128, 128, 128))
        else:
            server_text = myfont.render("Server name", True, (255, 255, 255))

        if cursor_vertical_pos == 3:
            done_text = myfont.render("Done", True, (255, 255, 255), (128, 128, 128))
        else:
            done_text = myfont.render("Done", True, (255, 255, 255))

        server_width, server_height = myfont.size("Server name")


        colon_text = myfont.render(": ", True, (255, 255, 255))
        colon_width, colon_height = myfont.size(": ")


        host_text_2 = myfont.render(host_name, True, (255, 255, 255))
        host_width_2, host_height_2 = myfont.size(host_name)


        server_text_2 = myfont.render(server_name, True, (255, 255, 255))
        server_width_2, server_height_2 = myfont.size(server_name)


        screen.blit(host_text, (0, 0))
        screen.blit(colon_text, (host_width, 0))
        screen.blit(host_text_2, ((host_width+colon_width), 0))


        screen.blit(server_text, (0, max(host_height, colon_height, host_height_2)))
        screen.blit(colon_text, (server_width, max(host_height, colon_height, host_height_2)))
        screen.blit(server_text_2, ((server_width + colon_width), max(host_height, colon_height, host_height_2)))

        screen.blit(done_text, (0, max(host_height, colon_height, host_height_2) + max(server_height, colon_height, server_height_2)))
    else:

        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                if c != None:
                    c.close_udp()
                    c.close_tcp()

                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if (cursor_vertical_pos + 1) < len(AVAILABLE_DIAGNOSTICS):
                        cursor_vertical_pos += 1

                elif event.key == pygame.K_UP:
                    if (cursor_vertical_pos - 1) >= 1:
                        cursor_vertical_pos -= 1

                elif event.key == pygame.K_RETURN:
                    enter_hit = True
                elif event.key == pygame.K_ESCAPE:
                    startup = True
                    cursor_vertical_pos = 1



        keys = pygame.key.get_pressed()

        ## Direction controls; keys[(key name)] returns a boolean if the key is pressed
        ## results will be -1, 0, 1 for x1 and -10, 0, 10 for y1, used with the
        ## "direction_dict" at the top of the file
        x1 = keys[pygame.K_d] - keys[pygame.K_a]
        y1 = 10*(keys[pygame.K_s] - keys[pygame.K_w])

        ## Arrow key controls; same format as the wasd controls. Used in navigating the cursor
        ## on the text
        x2 = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        y2 = keys[pygame.K_DOWN] - keys[pygame.K_UP]


        text = ''
        if x1 != 0 and y1 != 0:
            text += direction_dict[y1] + " and " + direction_dict[x1]
        elif x1 == 0 and y1 == 0:
            text = "No movement being sent"
        else:
            text += direction_dict[y1] + direction_dict[x1]

        if c != None:
            if (x1 == 0) and (y1 == 0):
                c.set_direction(0)
            else:
                if y1 == -10:
                    if x1 == 0:
                        c.set_direction(1)
                    elif x1 == 1:
                        c.set_direction(2)
                    elif x1 == -1:
                        c.set_direction(8)
                elif y1 == 10:
                    if x1 == 0:
                        c.set_direction(5)
                    elif x1 == 1:
                        c.set_direction(4)
                    elif x1 == -1:
                        c.set_direction(6)
                elif y1 == 0:
                    if x1 == 1:
                        c.set_direction(3)
                    elif x1 == -1:
                        c.set_direction(7)



        text_surface = myfont.render(text, True, (255, 255, 255))


        offset = 0
        for index, diagnostic in enumerate(AVAILABLE_DIAGNOSTICS):

            if index == cursor_vertical_pos:
                if enter_hit:
                    AVAILABLE_DIAGNOSTICS[diagnostic] ^= True
                    enter_hit = False

            if offset == 0:
                temp_header = myfont.render(diagnostic, True, (255, 255, 255))
            elif AVAILABLE_DIAGNOSTICS[diagnostic] == True:
                if index == cursor_vertical_pos:
                    temp_header = alteredfont.render(diagnostic, True, (0, 255, 0))
                else:
                    temp_header = myfont.render(diagnostic, True, (0, 255, 0))
            else:
                if index == cursor_vertical_pos:
                    temp_header = alteredfont.render(diagnostic, True, (255, 0, 0))
                else:
                    temp_header = myfont.render(diagnostic, True, (255, 0, 0))
            screen.blit(temp_header, (0, offset))
            offset += space

        direction_header = myfont.render("Direction:", True, (255, 255, 255))
        screen.blit(direction_header, (0, 250))
        screen.blit(text_surface, (0, 250+space))



    pygame.display.flip()
    pygame.time.wait(10)
    screen.fill((0, 0, 0))
    #clock.tick(120)

    #window_surface.blit(background, (0, 0))