import pygame
import pygame.freetype
#import pygameGui

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
cursor_lock = 0
enter_hit = False

running = True

## Main loop; Uses a keydown check to manage a cursor lock to avoid unintentionally
## skipping past when navigating. The lock is not release until the keyup is detected
## for the key that initiated the lock
while running:
    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and cursor_lock == 0:
                if (cursor_vertical_pos + 1) < len(AVAILABLE_DIAGNOSTICS):
                    cursor_vertical_pos += 1
                    cursor_lock = 1

            elif event.key == pygame.K_UP and cursor_lock == 0:
                if (cursor_vertical_pos - 1) >= 1:

                    cursor_vertical_pos -= 1
                    cursor_lock = 2

            elif event.key == pygame.K_RETURN and cursor_lock == 0:
                enter_hit = True
                cursor_lock = 3

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and cursor_lock == 1:
                cursor_lock = 0
            elif event.key == pygame.K_UP and cursor_lock == 2:
                cursor_lock = 0
            elif event.key == pygame.K_RETURN and cursor_lock == 3:
                cursor_lock = 0


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




    screen.fill((0, 0, 0))
    text = ''
    if x1 != 0 and y1 != 0:
        text += direction_dict[y1] + " and " + direction_dict[x1]
    elif x1 == 0 and y1 == 0:
        text = "No movement being sent"
    else:
        text += direction_dict[y1] + direction_dict[x1]

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
    #clock.tick(120)

    #window_surface.blit(background, (0, 0))