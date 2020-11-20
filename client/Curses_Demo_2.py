import curses
from random import random, choice
import time


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
    
    pseudo_timer = 50
    pseudo_timer_length = pseudo_timer
    
    quit_attempt = False
    
    enter_hit = False

    opening_screen = True
    
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
        
        if opening_screen:
            if k == curses.KEY_DOWN and y_pos < len(AVAILABLE_DIAGNOSTICS):
                y_pos = y_pos + 1
            elif k == curses.KEY_UP and y_pos > 1:
                y_pos = y_pos - 1

            if k == 10 and y_pos == len(AVAILABLE_DIAGNOSTICS):
                y_pos = 1
                opening_screen = False
            
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
                stdscr.addstr(len(AVAILABLE_DIAGNOSTICS), 0, "Done", curses.A_REVERSE)
            else:
                stdscr.addstr(len(AVAILABLE_DIAGNOSTICS), 0, "Done")
    
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

        # refreshes screen and checks if there's a queued input
        stdscr.refresh()
        k = stdscr.getch()
        time.sleep(.01)

        
        if k == ord('q') and quit_attempt == False:
            quit_attempt = True
            k = 0
            
        elif k != ord('q') and k != curses.ERR and quit_attempt == True:
            quit_attempt = False

        elif k == ord('c'):
            opening_screen = True

        elif k == ord("w"):
            pass
        elif k == ord("a"):
            pass
        elif k == ord("
            
        enter_hit = False
##            

def main():
    curses.wrapper(demo_screen)
    
if __name__ == "__main__":
    main()
