""" --------------------------------------------

VALEO Engineer Remote Assistant

BEng (Hon) in Mechatronic Engineering FYP
Dublin City University
Daire Curran | 18108831 | ME4

------------------------------------------------"""

#!/usr/bin/env python
# Calls python interpretor to execute code

# import Python Libraries
import pyaudio
import sys
import json
import datetime
import socket
from gpiozero import LED, Buzzer
from time import sleep
from os import environ, path
from sphinxbase import *
from pocketsphinx import *

green_led = LED(22) # controls LED connected to GPIO20
red_led = LED(24) # controls LED connected to GPIO21
buzzer = Buzzer(23) # controls Buzzer connected to GPIO16

# speech recognition function
def Get_speech():
    global speech # global variable which holds mic data
    global mic_input # global variable contains recognised words as string
    speech = LiveSpeech(#logfn = '/dev/null', # disables logs
                        buffer_size=1048,
                        sampling_rate=16000,
                        hmm='/home/pi/Desktop/Acoustic_model_adaption2/en-us-adapt', # set path to acoustic model
                        lm='/home/pi/Desktop/Acoustic_Model_Adaption/7945.lm', # set path to language model
                        dic='/home/pi/Desktop/Acoustic_Model_Adaption/7945.dic' # set path to phonetic dictionary
                        )
    for phrase in speech:
        print(phrase) # prints detected word in speech data
        mic_input = str(phrase) # converts to string
        return 1 # exit function

# function creates JSON file according to mic input
def Pre_annotation():
    print('Running Pre-annotation function')
    global rec_time # global variable contains timestamp information
    rec_time = ('Timestamp_{:%d-%m-%Y_%H_%M}'.format(datetime.datetime.now())) # uses datetime library to create timestamp of current date and time
    for phrase in speech:
        print(phrase)
        mic_input = str(phrase)
        f = open(rec_time,'a')
        if 'QUIT' in mic_input: # finish pre-annotation
            f.close # closes JSON file
            print('[+] JSON file created')
            Client()
            return 1
        with open(rec_time, 'a') as f: # Open text file in append mode, with file name set to the variable rec_time
            json.dump(mic_input, f) # appends mic_input to JSON
            f.write('\n') # new line after each entry to JSON

# function pushed JSON file to server
def Client():
    server_address = "169.254.237.170"
    server_port = 12345 # port number must be the same on client and server
    s = socket.socket() # creates a socket for transferring of data
    print(f"[*] Connecting to {server_address}")
    s.connect((server_address, server_port))
    print("[+] Connected")
    filename = bytes(rec_time, 'utf-8') # convert filename to 8-bit unicode transformation format
    s.send(filename)
    f = open(rec_time, "rb") # open JSON file in read-binary format
    l = f.read(1024) # read 1kb of data from binary text file
    while (l): # continue to run loop as long as the file is being read
        s.send(l) # send 1kb of data accross connection to server
        l = f.read(1024)
    s.close() # close socket connnection
    print("[>] File sent")

# function demonstrates I/O control
def MT_control():
    print('Running MT control function')
    buzzer.on() #
    sleep(0.01)
    buzzer.off()
    sleep(1)
    for i in range(0,15): # Flicker LEDs
        red_led.on(), sleep(0.05)
        green_led.on(), sleep(0.05)
        red_led.off(), sleep(0.05)
        green_led.off(), sleep(0.05)

def Canbus_control():
    print('Running CANbus control function')

def Log_test_results():
    print('Running test results function')

def Shutdown_sys():
    print('Shutting system down')
    buzzer.on()
    sleep(0.01)
    buzzer.off() # switches off all ouputs
    red_led.off()
    green_led.off()
    sys.exit() # closes program
#    os.system("sudo shutdown -h now") # shutsdown raspberrypi

while True:
    print('Listening for keyword : ')
    red_led.on() # red light on to represent system is not fully active
    green_led.off()
    Get_speech()

    if  'VERA' in mic_input: # Listen for keyword 'VERA' to activate main body of code
        print('VERA activated')

        while True:
            print('Choose mode : ')
            red_led.off()
            green_led.on() # green light respresetns active system
            buzzer.on() # beep to signal system is active
            sleep(0.01)
            buzzer.off()
            Get_speech()

            if 'PREANNOTATE' in mic_input: # Listen for keyword 'Preannotate' to activate pre-annotation
                buzzer.on() # beep to signal start of preannotation function
                sleep(0.01)
                buzzer.off()
                Pre_annotation()
            
            elif 'MT CONTROL' in mic_input: # Listen for keyword 'MT Control' to activate mt control
                MT_control()

            elif 'CANBUS CONTROL' in mic_input: # Listen for keyword 'CANbus control' to activate CANbus control
                Canbus_control()

            elif 'LOG TEST RESULTS' in mic_input: # Listen for keyword 'Log Test Results' to activate test results
                Log_test_results()

            elif 'SHUTDOWN' in mic_input: # Listen for keyword 'Shutdown' to shut raspberry-pi down
                Shutdown_sys()

            else: # Error Handling
                print('Error undefined input')
                for i in range(0,15):
                    red_led.on() # red LED blinks to signal error
                    sleep(0.05)
                    red_led.off()
                    sleep(0.05)

    else:
        print('Error undefined input')
        # red LED does not blink because program is not in active state
