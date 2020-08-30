# -----------------------------------------------------
# Created : 30th Aug 2020
# Author  : @Naimish240
# -----------------------------------------------------
# This program uses the twilio API to send messages 
# instead of using the browser
# Used for people who have a twilio account
# -----------------------------------------------------
import json, WhatsApp
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
# -----------------------------------------------------
'''
    DISCLAIMER :
    I AM NOT RESPONSIBLE IF YOUR ACCOUNT GETS BANNED OR API
    CALLS EXCEDE YOUR TIER LIMIT. CONSULT THE TWILIO DOCS
    AND PROCEED WITH CAUTION.

    Functions found here:
        readJSON(path)                  : Gets keys from json file
        sendMessage(number, text, cred) : Sends Message using API
        main(numbers, text, save, cred) : Main control loop

    NOTE : USES FUNCTIONS FROM 'WhatsApp.py'
'''
# -----------------------------------------------------
# Function to open JSON and get the required data from it
def readJSON(path):
    '''
        INPUTS : path (string)
        OUTPUT : data (dictionary)
    '''
    # Opens file and yoinks the keys from it
    with open(path) as f:
        data = json.load(f)
    # Returns the fun stuff to the bot
    return data
# -----------------------------------------------------
# Function to send message with the API
def sendMessage(number, text, cred):
    '''
        INPUTS : number (Number to send message to), text (Message to send), cred (Dictionary of credentials)
        OUTPUT : None

        NOTE : Yoinked from https://www.twilio.com/docs/libraries/reference/twilio-python/
    '''
    account = cred.account
    token = cred.token
    client = Client(account, token)
    fr = cred.fr
    # Adds '+' to number, if it isn't first character
    if fr[0] != '+':
        fr = '+' + fr
    # Sends message
    message = client.messages.create(to="+{}".format(number), 
                                    from_="{}".format(fr),
                                    body=text)
# -----------------------------------------------------
# Main function to control loop
def main(numbers, text, save, path):
    '''
        INPUTS : numbers (List of numbers to send the message to), text (Message to send), save (To save or to not save, that is the question), path (Path to JSON storing keys)
        OUTPUT : None

        NOTE : SENDS THE SAME MESSAGE TO ALL PEOPLE
    '''
    # Stores log
    success = []
    failed = []
    # Gets credentials from json
    cred = readJSON(path)
    # Loops through numbers to send message
    for number in numbers:
        # Tries to send message
        try:
            sendMessage(number, text, cred)
            print("\033[32mSent Message to {} successfully!\033[00m".format(number))
            success.append([number, text])
        # Message not sent
        except TwilioRestException:
            print("\033[91mUnable to send message to {}!\033[00m".format(number))
            failed.append([number, text])
    # Saves log data
    if save:
        # Checks if log folder exists
        WhatsApp.checkFolder()
        # Dumps log
        WhatsApp.saveLOG(success, failed)

    print("Stats:")
    print("\033[32mSuccessful {}\033[00m, \033[91mFailed\033[00m {}".format(len(success), len(failed)))
    print("Fraction of messages successfully sent : {}".format(len(success)/(len(success)+len(failed))))
    print("Open the folder 'LOGs' for further details")
# -----------------------------------------------------