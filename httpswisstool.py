#!/usr/bin/env python3

import socket
import sys

class HTTPBody(object):
   def __init__(self):
      self.clear()

   def clear(self):
      self.textUsed = False
      self.__plaintext = ""
      self.parameters = {}
      
   def addParameter(self, name, value):
      self.textUsed = False
      self.parameters[name] = value

   def plaintext(self, text=None):
      if text is None:
         return str(self)
      else:
         self.textUsed = True
         self.__plaintext = text

   def parametersToStr(self):
      ret = []
      for i, j in self.parameters.items():
         ret.append("{}={}".format(i, j))
      return "&".join(ret)

   def __str__(self):
      if self.textUsed:
         return self.__plaintext
      else:
         return self.parametersToStr()

   def __len__(self):
      return len(str(self))

class HTTPHeader(dict):
   def __init__(self, body = None):
      dict.__init__(self)
      if body is None:
         self.body = HTTPBody()
      else:
         self.body = body

   def getBody(self):
      return self.body

   def plaintext(self, text):
      for i in text.split('\n'):
         self.clear()
         name, value = tuple(i.split(": "))
         if name != "Content-Length": self[name] = value

   def __str__(self):
      ret = []
      for p, v in self.items():
         ret.append("{}: {}".format(p, v))
      ret.append("Content-Length: {}".format(len(self.body)))
      return "\n".join(ret)

class HTTPRequest(object):
   def __init__(self):
      self.__method = "GET"
      self.url = "/"
      self.protocol = "HTTP/1.1"
      self.body = HTTPBody()
      self.header = HTTPHeader(self.body)

   def method(self, method=None):
      if method is None:
         return self.__method
      else:
         self.__method = method
   
   def __str__(self):
      return "{} {} {}\n{}\n\n{}\n\n".format(self.__method, self.url, self.protocol, str(self.header), str(self.body))

httpRequest = HTTPRequest()


def cmdSetHeader(plaintext):
   httpRequest.header.plaintext(plaintext)

def cmdSetHeaderparameter(name, value):
   httpRequest.header[name] = value

def cmdSetMethod(method):
   httpRequest.method(method)

def cmdSetBody(plaintext):
   httpRequest.body.plaintext(plaintext)

def cmdSet(params):
   subCommand, params = tuple(params.split(" ", 1))
   if subCommand == "body": cmdSetBody(params)
   if subCommand == "method": cmdSetMethod(params)
   if subCommand == "headerparameter": 
      name, value = tuple(params.split(" ", 1))
      cmdSetHeaderparameter(name, value)
   if subCommand == "header": cmdSetHeader(params)

def cmdHeader():
   print(httpRequest.header)

def cmdPrint():
   print(str(httpRequest))

def parseCommand(command):
   try:
      command, params = tuple(command.split(" ", 1))
   except ValueError:
      params = ""

   if command == "help":
      cmdHelp()
   if command == "set":
      cmdSet(params)
   if command == "header":
      cmdHeader()
   if command == "print":
      cmdPrint()

def cmdHelp():
   print("""
   Building HTTP request:
      * help : print this message
      * print : print the whole 
      * header : print current header
      * set header <new header> : repleace header with <new header>.
      * set headerparameter <element> <new value> : replace or add the content of <element> in header with <new value>
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
      * set bodyparameter <param_name> <param_value>
      * set urlparameter <param_name> <param_value>
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

if len(sys.argv)<2:
   print("Usage: httpswisstool.py <HOST> <PORT>")
   sys.exit(1)
   
host = sys.argv[1]
port = sys.argv[2]

print("Waiting for commands...")
quit = False

while not quit:
   command = input("{}:{}?> ".format(host, port))
   parseCommand(command)
