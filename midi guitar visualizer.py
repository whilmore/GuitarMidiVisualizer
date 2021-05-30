import mido as m
import pygame.midi
import pygame
import time
import re
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from easygui import *
import pygame.freetype
import pygame.time
from threading import Event

def showKey(keyNum):
    if keyNum in keyLocation:
        for location in keyLocation[keyNum]:
            screen.blit(circle,[location[0] - 27,location[1] - 26])

def loadify(img):
    return pygame.image.load(img).convert_alpha()

def mute():
    global currentlyPlaying
    for i in currentlyPlaying:
        player.note_off(i, 127)
    currentlyPlaying[:] = []

def messageList(messages, mid, tempo, trackNumber):
    for msg in mid.tracks[trackNumber]:
        message = str(msg)
        noteFind = re.search(r'(?:[, ])note=(\d+)', message)
        velocityFind = re.search(r'(?:[, ])velocity=(\d+)', message)
        timeFind = re.search(r'(?:[, ])time=(\d+)', message)
        if noteFind and velocityFind and timeFind and ('note_on' in message):
            messages.append([int(noteFind.group(1)), int(velocityFind.group(1)),
                             float(m.tick2second(float(timeFind.group(1)), mid.ticks_per_beat, float(tempo))), 1])
        elif noteFind and velocityFind and timeFind and ('note_off' in message):
            messages.append([int(noteFind.group(1)), int(velocityFind.group(1)),
                             float(m.tick2second(float(timeFind.group(1)), mid.ticks_per_beat, float(tempo))), 0])
    return messages

def tempoFind(mid):
    for msg in mid.tracks[0]:
        message = str(msg)
        pace = re.search(r'(?:[, ])tempo=(\d+)', message)
        if pace:
            return pace.group(1)
        else:
            for msg in mid.tracks[1]:
                message = str(msg)
                pace = re.search(r'(?:[, ])tempo=(\d+)', message)
                if pace:
                    return pace.group(1)

def midiPlayer(message, player):
    global currentlyPlaying
    if message[3] == 1:
        player.note_on(message[0], 127)
        currentlyPlaying.append(message[0])
    elif message[3] == 0:
        player.note_off(message[0], 127)
        if message[0] in currentlyPlaying:
            currentlyPlaying.remove(message[0])


# all keys DONT TOUCH
keyLocation = {
    #e
    40: [(40, 290)],
    #f
    41: [(111,300)],
    #f#
    42: [(175, 299)],
    #g
    43: [(225, 301)],
    #g#
    44: [(287, 299)],
    #a
    45: [(342, 299), (39, 247)],
    #a#
    46: [(404, 299), (107, 247)],
    #b
    47: [(461, 301), (172, 250)],
    #c
    48: [(514, 301), (228, 252)],
    #c#
    49: [(567, 298), (287, 250)],
    #d
    50: [(632, 300), (344, 247), (41, 197)],
    #d#
    51: [(688, 301), (400, 248), (108, 201)],
    #e2
    52: [(742, 299), (456, 249), (169, 201)],
    #f2
    53: [(798, 300), (511, 250), (226, 198)],
    #f#2
    54: [(860, 297), (570, 248), (284, 199)],
    #g2
    55: [(920, 300), (629, 249), (344, 201), (39, 151), ],
    #g#2
    56: [(973, 300), (687, 251), (396, 201), (110, 147), ],
    #a2
    57: [(1035, 300), (744, 249), (455, 198), (172, 151),],
    #a#2
    58: [(1090, 299), (801, 249), (516, 199), (230, 147), ],
    #b2
    59: [(1150, 302), (861, 245), (571, 198),(287, 146),(37, 101)],
    #c2
    60: [(1203, 302),(914, 249),(627, 200),(345, 149),(109, 99)],
    #c#2
    61: [(1263, 298),(973, 249),(684, 198),(400, 148),(172, 103)],
    #d2
    62: [(1319, 300), (1032, 247), (745, 198), (457, 147), (228, 97)],
    #d#2
    63: [(1377, 299),(1088, 248),(802, 199),(517, 150),(282, 96)],
    #e3
    64: [(1437, 300),(1149, 251),(860, 197),(574, 147),(341, 96),(40, 56)],
    #f3
    65: [(1204, 250),(913, 197),(627, 147),(396, 99),(109, 48)],
    #f#3
    66: [(1262, 248),(975, 200),(685, 151),(455, 98),(164, 49)],
    #g3
    67: [(1319, 252),(1031, 197),(741, 145),(512, 99),(224, 51)],
    #g#3
    68: [(1377, 250),(1093, 199),(802, 148),(569, 99),(284, 51)],
    #a3
    69: [(1435, 249),(1149, 200),(861, 148),(628, 98),(342, 47)],
    #a#3
    70: [(1206, 199),(917, 147),(688, 100),(399, 48)],
    #b3
    71: [(1263, 200),(974, 146),(747, 97),(458, 50)],
    #c3
    72: [(1320, 197),(1033, 149),(803, 100),(515, 46)],
    #c#3
    73: [(1377, 202),(1084, 153),(859, 98),(575, 50)],
    #d3
    74: [(1435, 198),(1149, 148),(916, 97),(630, 45)],
    #d#3
    75: [(1204, 150),(977, 100),(684, 51)],
    #e4
    76: [(1263, 149),(1032, 97),(742, 48)],
    #f4
    77: [(1321, 148),(1088, 99),(800, 48)],
    #f#4
    78: [(1377, 151),(1147, 99),(860, 49)],
    #g4
    79: [(1437, 151),(1205, 99),(921, 49)],
    #g#4
    80: [(1262, 99),(973, 50)],
    #a4
    81: [(1322, 103),(1028, 48)],
    #a#4
    82: [(1378, 101),(1094, 48)],
    #b4
    83: [(1436, 99),(1149, 48)],
    #c4
    84: [(1208, 51)],
    #c#4
    85: [(1265, 49)],
    #d4
    86: [(1320, 47)],
    #d#4
    87: [(1380, 52)],
    #e5
    88: [(1434, 53)],
}
exit = Event()

# note/velocity/time/OnOff
messages = []
coordinates = []

# for muting
currentlyPlaying = []

# placeholders
tempo = 500000
speed = 1.0
skipAmount = 40
speedAmount = 0.1

# file select
Tk().withdraw()
filename = tkFileDialog.askopenfilename()
mid = m.MidiFile(filename)
mid.print_tracks(0)
# midi track
trackList = []

for i in mid.tracks:
    trackList.append(str(i))

trackNumber = indexbox(msg='What Midi track to play', title="Track Select", choices=trackList)

# tempo find
tempo = tempoFind(mid)

# get all the messages
messages = messageList(messages, mid, tempo, trackNumber)

# init
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)
pygame.midi.init()
font = pygame.freetype.SysFont("arial", 24)

# clock
clock = pygame.time.Clock()

# ports
port = pygame.midi.get_default_output_id()
player = pygame.midi.Output(port, 0)

# instrument
player.set_instrument(1)

# screen
screen = pygame.display.set_mode((1529, 500))

# timing
newTime = 0
lostTime = 0

# assets load

scale = loadify('newscale.png')
circle = loadify('circle.png')

# gameLoop
counter = 0
moveCounter = 0
setCounter = 0
play = True
running = True
loop = False
#tuple = (0,0)

while running:
    oldTime = pygame.time.get_ticks()
    if oldTime != 0:
        lostTime = (oldTime - newTime) + 2.7

    # white screen
    screen.fill((244, 240, 219))

    # player
    if counter < len(messages) and play:
        if (messages[counter][2] - (lostTime / 1000) > 0):
            time.sleep((messages[counter][2] - (lostTime / 1000)) / speed)
        midiPlayer(messages[counter], player)
        counter = counter + 1

    if len(currentlyPlaying) != 0:
        for i in range(len(currentlyPlaying)):
            showKey(currentlyPlaying[i])

    if loop and counter == len(messages):
        counter = 0

    # background
    screen.blit(scale, (0, 0))
    # event
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False
        # keyboard input
        if event.type == pygame.KEYDOWN:
            exit.set()
            # restart song
            if event.key == pygame.K_r:
                exit.set()
                mute()
                counter = 0
            # pause game
            if event.key == pygame.K_SPACE:
                exit.set()
                mute()
                play = not play
            # skip back
            if event.key == pygame.K_LEFT:
                if counter - skipAmount < 0:
                    exit.set()
                    mute()
                    counter = 0
                else:
                    mute()
                    exit.set()
                    counter = counter - skipAmount
            # skip ahead
            if event.key == pygame.K_RIGHT:
                if counter + skipAmount > len(messages):
                    exit.set()
                    mute()
                    counter = len(messages)
                else:
                    exit.set()
                    mute()
                    counter = counter + skipAmount
            # speed up
            if event.key == pygame.K_UP:
                exit.set()
                speed = round((speed + speedAmount), 1)
            # speed down
            if event.key == pygame.K_DOWN:
                exit.set()
                if speed - speedAmount > 0:
                    speed = round((speed - speedAmount), 1)
            if event.key == pygame.K_l:
                    loop = not loop
            #get coordinate on screen (testing purposes)
            #if event.key == pygame.K_p:
            #    tuple = pygame.mouse.get_pos()
            #   print tuple

    #if tuple != (0,0):
    #    screen.blit(circle, (tuple[0] - 27, tuple[1] - 26))
    #else:
    #   screen.blit(circle,tuple)

    text_surface, rect = font.render('Speed: ' + str(speed) + " Current: " +  str(counter) + "/" + str(len(messages)), (0, 0, 0))
    screen.blit(text_surface, (30, 450))

    # update screen
    pygame.display.update()
    newTime = pygame.time.get_ticks()
    clock.tick(60)

# player quit
del player
pygame.midi.quit()
pygame.quit()