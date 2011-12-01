#!/usr/bin/python

'''
Copyright (c) 2011, Peter Hajas
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Peter Hajas nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL PETER HAJAS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import requests
import json
import sys,os,random

def register_account(number, password):
    dataDict = {"password":password}
    response = requests.put("http://api.fakecall.net/v1/account/{0}".format(number),data=dataDict)
    
    if response.status_code >= 400:
        print "There was a problem registering your account"
        return None
    else:
        result = json.loads(response.content)
        return result["code"]


def call_number(number, password):
    response = requests.post('http://api.fakecall.net/v1/account/{0}/call'.format(number),auth=(number,password))
    
    if response.status_code >= 400:
        print "There was a problem calling your number"
    else:
        print "Calling your number..."


def delete_account(number, password):
    response = requests.delete('http://api.fakecall.net/v1/account/{0}'.format(number),auth=(number,password))
    if response.status_code >= 400:
        print "There was a problem deleting your account"
    else:
        print "Account deleted"

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print "Please run Elliot with a command."
        print "Elliot will create a password for you and save it in ~/elliot"
        print "Commands are:"
        print "    - call"
        print "    - delete"
        print "For example:"
        print "    ./Elliot.py call"
        quit()
    
    command = sys.argv[1]
    
    number = None
    password = None
    
    # If the elliot config file does not exist, create it and register an account
    if not os.path.isfile(os.path.expanduser("~/.elliot")):
        print "No config file found, creating one..."
        # Create the file
        configFile = open(os.path.expanduser("~/.elliot"), 'w')
        number = raw_input("What number would you like Elliot to reach you at?: ")
        # Write the user's number to the file
        configFile.write(number+" ")
        password = str(random.randint(0,sys.maxint))
        # Write the password to the file
        configFile.write(password+" ")
        print "Registering an acocunt with password {0}".format(password)
        code = register_account(number, password)
        if not code:
            print "Couldn't register, sorry"
            quit()
        print "fakecall.net will now call you to confirm."
        print "Please enter the code {0}\n".format(code)
        configFile.close()
        wait = raw_input("Press enter after confirming your code with fakecall...")
    
    # If we don't have a password or phone number, load it from their file
    if not number or not password:
        configFile = open(os.path.expanduser("~/.elliot"), 'r')
        authentication = configFile.readline().split()
        number = authentication[0]
        password = authentication[1]
        configFile.close()
    
    if command == "call":
        call_number(number,password)
    elif command == "delete":
        delete_account(number, password)
        # Delete their config file
        os.remove(os.path.expanduser("~/.elliot"))
    else:
        print "Elliot doesn't know that command, sorry."

if __name__ == "__main__":
    main()