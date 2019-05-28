#!/usr/bin/env python3

import socket
import sys

def cmdHelp():
   print("""
   Building HTTP request:
      * help : print this message
      * header : print current header
      * set header <new header> : repleace header with <new header>. You can use \\n as line breaks
      * set header <element> <new value> : replace or add the content of <element> in header with <new value>
        You don't have to maintain Content-Length.
      * set method <http type> : You can set the HTTP type 
      * set body 
      * save : saves the current session into the memory 
      * load : restores the session stored in memory
      * load body : restores only the body of the session stored in memory
      * load header
      * load cookies
      * save session <filename>
      * load session <filename>
      * load session header <filename>
      * load session body <filename>
      * load session cookies <filename>
      * list sessions
      * list parameters
      * set body parameter <param_name> <param_value>
      * set url parameter <param_name> <param_value>
      * list parameters
      * list body parameters
      * list url parameters
      * list cookies
      * delete url parameter <param_name>
      * delete body parameter <param_name>
      * set cookie <cookie_name> <cookie_value>
      * get cookie <cookie_name>
      * delete cookie <cookie_name>
      
   Controlling communication:
      * send : Sends the current session
      * send <filename> : Sends the stored session
      * accept answer cookies : Accepts the cookies from the last answer
      * get answer : Prints last answer
      * get answer header : Prints the header of last answer
      * get answer body : Prints the body of last answer
      * mute / unmute : disable/enable the automatic print of the answer
   
   Handling/parsing answers:
      * save answer <filename> : Saves last answer into file
      * load answer <filename> : Restores answer from file. (It will be set as last answer)
      * list answers : lists stored answers
   """)

commandHandlers = {
   "help":cmdHelp
}

if len(sys.argv)<2:
   print("Usage: httpswisstool.py <HOST> <PORT>")
   sys.exit(1)
   
host = sys.argv[1]
port = sys.argv[2]

print("Waiting for commands...")
quit = False

while not quit:
   command = input("{}:{}?> ".format(host, port))
   commandHandlers[command]()
