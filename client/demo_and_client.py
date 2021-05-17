import curses
from random import random, choice
import time

### stolen from github code haha

import os
import socket
import json


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
        data = {"direction": direction}
        send_data = json.dumps(data)
        self.send_udp(send_data)

###

# please forgive my sphaget code, it was born of various tests into curses.
# still need to try out text entry though

# TODO
# bars w/ values for relevant
# get multiple keys
# put Y/N on the main groups

AVAILABLE_DIAGNOSTICS = {"Displayed Values:": False,
                         "GPS":True,
                         "Acceleration":True,
                         "Battery":True,
                         "Speed":True,
                         "Temperature":True,
                         "Motor":True}



def demo_screen(stdscr):
    
##    curses.curs_set(0)
    
    k = 0
    y_pos = 1
    
##    curses.halfdelay(1)
    stdscr.nodelay(True)
    host_name = ''
    server_name = ''
    c = None

    pseudo_timer = 50
    pseudo_timer_length = pseudo_timer
    
    quit_attempt = False
    
    enter_hit = False

    opening_screen = True

    test_set = set()
    
    current_curse = ''
    
    random_curses = ["Vetus quomodo sanies signeficatur Tacita deficta.",
                     
                     "Docimedis perdidit manicilia dua qui illas involavit\
ut mentes suas perdat et oculos suos in fano ubi destinat.",
                     
                     "Humanum quis sustulit Verionis palliolum sive res\
illius, qui illius minus fecit, ut illius mentes, memoriasdeiectas sive\
mulierem sive eas, cuius Verionis res minus fecit, ut illius manus,\
caput, pedes vermes, cancer, vermitudo interet, membra medullas illius interet.",
                     
                     "Qui mihi Vilbiam involavit sic liquat comodo aqua.\
Ell[…] muta qui eam involavit.",

                     "Inplicate lacinia Vincentzo Tzaritzoni, ut urssos\
ligare non possit, omni urssum perdat, non occidere possit in die\
Merccuri in omni ora iam iam, cito cito, facite!",

                     "Adiuro te demon, quicunque es, et demando tibi ex\
hanc hora, ex hanc die, ex hoc momento, ut equos prasini et albi crucies,\
occidas et agitatores Clarum et Felicem et Primulum et Romanum occidas.",

                     "Sosio de Eumolpo mimo ne enituisse poteat. Ebria vi\
monam agere nequeati in eqoleo."]
    
    necessary_lines = 0
    
    text_dict = dict()
    text_dict[0] = f'Options:'
    
    for i in range(1, 10):
        text_dict[i] = f'Option {i}'
    
    
    while (k != ord('q')):
        curses.curs_set(0)
        stdscr.clear()

        height, width = stdscr.getmaxyx()   # expects a certain size on startup,
                                            # so doesn't check the first render
                                            # changing the window size will
                                            # update it properly
                                            
                                            # currently has issues with tiny
                                            # window sizes, but supposedly
                                            # curses doesn't manage the window,
                                            # only paints over it


            # sort of a fake "timer" in that it only updates in intervals of half
            # of a second without interfering with constant input checks
            # updates the bar and reading values with random ones
        if pseudo_timer == pseudo_timer_length:
            bar_0 = random()
            bar_1 = random()
            bar_2 = random()
            
            reading_0 = random()
            reading_2 = random()
            pseudo_timer = 0

            readings = dict(AVAILABLE_DIAGNOSTICS)
            for category in readings:
                readings[category] = random()
        else:
            pseudo_timer += 1
                
        
        if opening_screen:
            if k == curses.KEY_DOWN and y_pos < len(AVAILABLE_DIAGNOSTICS) + 2:
                y_pos = y_pos + 1
            elif k == curses.KEY_UP and y_pos > 1:
                y_pos = y_pos - 1

            if k == 10 and y_pos == (len(AVAILABLE_DIAGNOSTICS) + 2):
                y_pos = 1
                opening_screen = False
                if (host_name != '') and (server_name != ''):
                    c = ClientNetwork(host_name, server_name)
                    c.initialize_header(None)
                else:
                    #c = None
                    c = ClientNetwork("10.0.1.15", "10.0.1.24")
            
            for line, text in enumerate(AVAILABLE_DIAGNOSTICS):
                if line == 0:
                    stdscr.addstr(line, 0, text)
                    
                elif line == y_pos and y_pos < len(AVAILABLE_DIAGNOSTICS):
                    stdscr.addstr(line, 0, text, curses.A_REVERSE)
                    stdscr.addnstr(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)), ": Y/N", 5)
                    if AVAILABLE_DIAGNOSTICS[text]:
                        if k == curses.KEY_RIGHT:
                            AVAILABLE_DIAGNOSTICS[text] = not AVAILABLE_DIAGNOSTICS[text]
                            stdscr.chgat(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)) + 4, 1, curses.A_STANDOUT)
                        else:
                            stdscr.chgat(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)) + 2, 1, curses.A_STANDOUT)
                    else:
                        if k == curses.KEY_LEFT:
                            AVAILABLE_DIAGNOSTICS[text] = not AVAILABLE_DIAGNOSTICS[text]
                            stdscr.chgat(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)) + 2, 1, curses.A_STANDOUT)
                        else:
                            stdscr.chgat(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)) + 4, 1, curses.A_STANDOUT)
                            
                else:
                    stdscr.addstr(line, 0, text)
                    stdscr.addnstr(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)), ": Y/N", 5)
                    if AVAILABLE_DIAGNOSTICS[text]:
                        stdscr.chgat(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)) + 2, 1, curses.A_STANDOUT)
                    else:
                        stdscr.chgat(line, len(max(AVAILABLE_DIAGNOSTICS.keys(), key = len)) + 4, 1, curses.A_STANDOUT)

            if y_pos == len(AVAILABLE_DIAGNOSTICS):
                if k == 46 or (k <= 57 and k >= 48):
                    host_name += chr(k)
                elif len(host_name) != 0:
                    if k == 8:
                        host_name = host_name[:-1]
                stdscr.addstr(y_pos, 0, "Host name", curses.A_REVERSE)
            else:
                stdscr.addstr(len(AVAILABLE_DIAGNOSTICS), 0, "Host name: " + host_name)

            stdscr.addnstr(len(AVAILABLE_DIAGNOSTICS), len("Host name"), ": " + host_name, 2 + len(host_name))
            stdscr.chgat(len(AVAILABLE_DIAGNOSTICS), len("Host name: " + host_name), 1, curses.A_BLINK)

            if y_pos == (len(AVAILABLE_DIAGNOSTICS) + 1):
                if k == 46 or (k <= 57 and k >= 48):
                    server_name += chr(k)
                elif len(server_name) != 0:
                    if k == 8:
                        server_name = server_name[:-1:]
                stdscr.addstr(y_pos, 0, "Server name", curses.A_REVERSE)
            else:
                stdscr.addstr(len(AVAILABLE_DIAGNOSTICS) + 1, 0, "Server name: " + server_name)

            stdscr.addnstr(len(AVAILABLE_DIAGNOSTICS)+ 1, len("Server name"), ": " + server_name, 2 + len(server_name))
            stdscr.chgat(len(AVAILABLE_DIAGNOSTICS) + 1, len("Server name: " + server_name), 1, curses.A_BLINK)

            if y_pos == (len(AVAILABLE_DIAGNOSTICS) + 2):
                stdscr.addstr(len(AVAILABLE_DIAGNOSTICS) + 2, 0, "Done", curses.A_REVERSE)
            else:
                stdscr.addstr(len(AVAILABLE_DIAGNOSTICS) + 2, 0, "Done")
    
        else:
##        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
##        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        
        # curses has built-in key values that can be checked against inputs
##        if k == curses.KEY_DOWN and y_pos < len(text_dict) - 1:
##            y_pos = y_pos + 1
##        elif k == curses.KEY_DOWN and y_pos == len(text_dict) - 1:
##            y_pos = (height - 1)//2
##        elif k == curses.KEY_UP and y_pos == (height - 1)//2:
##            y_pos = len(text_dict) - 1
##        elif k == curses.KEY_UP and y_pos > 1:
##            y_pos = y_pos - 1

            if k == curses.KEY_DOWN and y_pos < len(AVAILABLE_DIAGNOSTICS) - 1:
                y_pos = y_pos + 1
            elif k == curses.KEY_DOWN and y_pos == len(AVAILABLE_DIAGNOSTICS) - 1:
                y_pos = (height - 1)//2
            elif k == curses.KEY_UP and y_pos == (height - 1)//2:
                y_pos = len(AVAILABLE_DIAGNOSTICS) - 1
            elif k == curses.KEY_UP and y_pos > 1:
                y_pos = y_pos - 1

            
            # There're issues with enter/return being interpretted as newlines
            # versus the built-in curses KEY, so the ascii code is used instead
            elif k == 10:
                enter_hit = True
            
            # renders the "options" in the top left
            # renders with a highlight if the cursor is there
    ##        for line in text_dict:
    ##            if line == y_pos and line != 0:
    ##                stdscr.addstr(line, 0, text_dict[line], curses.A_STANDOUT)
    ##            else:
    ##                stdscr.addstr(line, 0, text_dict[line])
            for line, text in enumerate(AVAILABLE_DIAGNOSTICS):
                if line == y_pos and line != 0:
                    if AVAILABLE_DIAGNOSTICS[text]:
                        stdscr.addstr(line, 0, text, curses.A_REVERSE)
                    else:
                        stdscr.addstr(line, 0, text, curses.A_BLINK)
                    if enter_hit == True:
                        AVAILABLE_DIAGNOSTICS[text] = not AVAILABLE_DIAGNOSTICS[text]
                elif AVAILABLE_DIAGNOSTICS[text]:
                    stdscr.addstr(line, 0, text, curses.A_STANDOUT)
                else:
                    stdscr.addstr(line, 0, text)
    ##


            # some bar displays using highlights of spaces as the "filled" bar
            stdscr.addstr(0, ((width - 1)//2), "Bar 0:")
            stdscr.addstr(1, ((width - 1)//2), (width - 1 - (width - 1)//2)* ' ')
            stdscr.addstr(2, (((width - 1)//2) - 1), "0")
            stdscr.addstr(2, width - 1 -(((width - 1)%2) + 3), "100")
            stdscr.chgat(1, ((width - 1)//2),
                         int(bar_0* (width - 1 - ((width - 1)//2))),
                         curses.A_STANDOUT)

            stdscr.addstr(4, ((width - 1)//2), "Bar 1:")
            stdscr.addstr(5, ((width - 1)//2), (width - 1 - (width - 1)//2)* ' ')
            stdscr.addstr(6, (((width - 1)//2) - 1), "0")
            stdscr.addstr(6, width - 1 -(((width - 1)%2) + 3), "100")
            stdscr.chgat(5, ((width - 1)//2),
                         int(bar_1* (width - 1 - ((width - 1)//2))),
                         curses.A_STANDOUT)

            stdscr.addstr(8, ((width - 1)//2), "Bar 2:")
            stdscr.addstr(9, ((width - 1)//2), (width - 1 - (width - 1)//2)* ' ')
            stdscr.addstr(10, (((width - 1)//2) - 1), "0")
            stdscr.addstr(10, width - 1 -(((width - 1)%2) + 3), "100")
            stdscr.chgat(9, ((width - 1)//2),
                         int(bar_2* (width - 1 - ((width - 1)//2))),
                         curses.A_STANDOUT)

    ##
            # renders with a highlight is a cursor is present here
            # if the cursor was present with enter/return being the most recent key,
            # chooses a random curse from the list at the top and figures out how
            # many lines are needed to display it with a margin of five spaces
            # otherwise displays the normal text and the most recent curse
            if y_pos == (height - 1)//2:
                stdscr.addstr((height - 1)//2, 0,
                              "Select a random curse (enter/return)",
                              curses.A_REVERSE)
                
                if enter_hit:
                    current_curse = choice(random_curses)
                    necessary_lines = -((-len(current_curse))//((width - 1)//2 - 5))
                    
            else:
                stdscr.addstr((height - 1)//2, 0,
                              "Select a random curse (enter/return)")
                
            # renders the portions of the curses to fit in the current sizing
            for i in range(1, necessary_lines + 1):
                stdscr.addstr(((height - 1)//2 + 1 + i), 0,
                              current_curse[i*((width-1)//2-5)-((width-1)//2-5):\
                              i*((width-1)//2-5)])

    ##
            # rendering the bottom right values
            current_add = 0
            for line, text in enumerate(AVAILABLE_DIAGNOSTICS):
                if AVAILABLE_DIAGNOSTICS[text]:
                    current_add += 1
                    stdscr.addstr((height - 1)//2 + current_add, (width - 1)//2, text + f': {readings[text]:0.3f}')

    ##        stdscr.addstr((height - 1)//2, (width - 1)//2, f'Reading 0: {reading_0:0.3f}')
    ##        stdscr.addstr((height - 1)//2 + 1, (width - 1)//2, f'Reading 1: {(180 - 360*reading_0):0.5f}, {(180 - 360*reading_2):0.5f}')
    ##        stdscr.addstr((height - 1)//2 + 2, (width - 1)//2, f'Reading 2: {(100* reading_2):0.2f}%')

    ##
        # the far bottom right text
        stdscr.addstr(height - 1, width - 1 - (len("timer: ") + len(str(pseudo_timer_length))), "timer: " + str(pseudo_timer))

        # keeps track of the quit status from the previous cycle
        if quit_attempt:
            stdscr.addstr(height - 1 , 0, "press q again to quit")
        else:
            stdscr.addstr(height - 1, 0, "press q twice to quit")

        stdscr.addstr(height - 1, len("press q twice to quit")+ 5, "Set contents: " + str(test_set))
        # refreshes screen and checks if there's a queued input
        stdscr.refresh()
        j = stdscr.getch()
        k = j
        if j == ord(' '):
            test_set = set()
        elif j != curses.ERR:
            if j == ord('a'):
                test_set.discard('d')
            elif j == ord('d'):
                test_set.discard('a')
            elif j == ord('w'):
                test_set.discard('s')
            elif j == ord('s'):
                test_set.discard('w')
            elif j == ord('e'):
                test_set.discard('a')
                test_set.discard('d')
            elif j == ord('f'):
                test_set.discard('w')
                test_set.discard('s')
            if j in {ord('w'), ord('a'), ord('s'), ord('d')}:
                test_set.add(chr(j))
            
            while(True):
                j = stdscr.getch()
                if j == ord(' '):
                    test_set = set()
                elif j != curses.ERR:
                    if j == ord('a'):
                        test_set.discard('d')
                    elif j == ord('d'):
                        test_set.discard('a')
                    elif j == ord('w'):
                        test_set.discard('s')
                    elif j == ord('s'):
                        test_set.discard('w')
                    elif j == ord('e'):
                        test_set.discard('a')
                        test_set.discard('d')
                    elif j == ord('f'):
                        test_set.discard('w')
                        test_set.discard('s')
                    if j in {ord('w'), ord('a'), ord('s'), ord('d')}:
                        test_set.add(chr(j))
                else:
                    break
        time.sleep(.01)

        if c != None:
            if len(test_set) != 0:
                if 'w' in test_set:
                    if 'd' in test_set:
                        c.set_direction(2)
                    elif 'a' in test_set:
                        c.set_direction(8)
                    else:
                        c.set_direction(1)
                elif 's' in test_set:
                    if 'd' in test_set:
                        c.set_direction(4)
                    elif 'a' in test_set:
                        c.set_direction(6)
                    else:
                        c.set_direction(5)
                elif 'd' in test_set:
                    c.set_direction(3)
                elif 'a' in test_set:
                    c.set_direction(7)
            else:
                c.set_direction(0)
        
        if k == ord('q') and quit_attempt == False:
            quit_attempt = True
            k = 0
            
        elif k != ord('q') and k != curses.ERR and quit_attempt == True:
            quit_attempt = False

        elif k == ord('c'):
            opening_screen = True
            
        enter_hit = False
##            

def main():
    curses.wrapper(demo_screen)
    
if __name__ == "__main__":
    main()
