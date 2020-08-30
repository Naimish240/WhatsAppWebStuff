# -----------------------------------------------------
# Created : 29th Aug 2020
# Author  : @Naimish240
# -----------------------------------------------------
# This program gets a csv file from the user and the 
# message template from the user and sends the messages
# using WhatsApp Web
# -----------------------------------------------------
import csv, WhatsApp, argparse, time, twilioAPI
# -----------------------------------------------------
'''
    CSV File Structure Supported in the funciton readCSV():

    a. Default : Can either specify country code in function call or default to IND
        1. Name, Number
        2. Asdf, XXXXXXXXXX
        3. Qwer, XXXXXXXXXX

    b. Country in Number; use '-' or ' ' to seperate country code from number. If not found, pass default value in function call
        1. Name, Number, Email
        2. Asdf, +YYY-XXXXXXXXXX
        3. Qwer, +YYY XXXXXXXXXX

    secrets.json structure:
    
        {
            'account' : "Your Account Key Here"
            'token'   : "Your Access Token Here"
            'fr'      : "Your Twilio Number Here"
        }

    Functions found here:
        readCSV(fileName)       : Opens a CSV file to get the phone numbers
        process(rawCSV, isd)    : Does basic processing on phone numbers to convert it into the input type expected by WhatsApp
        readTXT(filename)       : Opens the text file which stores the message to be sent
        sendMsgs(numbers, text) : Sends the message to all the numbers
'''
# -----------------------------------------------------
# This funciton opens the CSV file to get the name and numbers
def readCSV(fileName):
    '''
        INPUTS : fileName (Path to CSV file; string), countryCode (Code for the country; string), message (if speficied by user)
        OUTPUT : rawCSV (CSV data; list)

        IMPORTANT : CSV file should be of structure specified aboce
    '''
    with open('{}.csv'.format(fileName), 'r') as fh:
        reader = csv.reader(fh)
        rawCSV = [i for i in reader]
        return rawCSV
# -----------------------------------------------------
# Function to format rawCSV into something sendable
def process(rawCSV, isd):
    '''
        INPUTS : rawCSV (csv data; list), isd (isd code, string)
        OUTPUT : numbers (list)
    '''
    # Pre-Processing ISD to be on the safe side
    isd = isd.replace('+', '')
    isd = isd.replace('-', '')
    isd = isd.replace(' ', '')
    # List to store numbers
    numbers = []
    for row in rawCSV:
        xx = row[1]
        # if number is 10 digits long, it means the country code is missing
        if len(xx) == 10:
            numbers.append(isd + str(xx))
            continue
        # Length of number is greater than 10
        elif len(xx) > 10:
            # Removes the characters '+', '-' and ' ' from number
            xx = xx.replace('+', '')
            xx = xx.replace('-', '')
            xx = xx.replace(' ', '')
            # Number without fancy characters is 10 digits long, so adds isd
            if len(xx) == 10:
                numbers.append(isd + str(xx))
                continue
            # Assumes number has isd
            else:
                numbers.append(str(xx))
                continue
        # Length of number is less than 10
        else:
            print("\033[91m{} is an invalid number!\033[00m")
            continue
    # Returns the set of valid numbers from list
    return numbers
# -----------------------------------------------------
# Function to read text file for message
def readTXT(filename):
    '''
        INPUTS : filename (Name of text file for message body; string)
        OUTPUT : text (Message in file; string)
    '''
    text = ''
    # Opens the file in read mode
    with open(filename, 'r') as fh:
        # Reads the text file for message
        text = fh.read()
    # Returns body of the message to user
    return text
# -----------------------------------------------------
# Function to send messages
def sendMsgs(numbers, text, save, browser):
    '''
        INPUTS : numbers (list of phone numbers), text (message body; string)
        OUTPUT : None
    '''
    stats = WhatsApp.main(numbers, text, save, browser)

    # If sign in successful
    if stats:
        print("Messages Sent")
        print("\033[32mSuccessful {}\033[00m, \033[91mFailed\033[00m {}".format(stats[0], stats[1]))
        print("Fraction of messages successfully sent : {}".format(stats[0]/(stats[0]+stats[1])))
        print("Open the folder 'LOGs' for further details")
    # Failed to run successfully
    else:
        print("\033[91mError! Authentication Failed! Try again later\033[00m")
# -----------------------------------------------------
# Main function
def main(csvFile, textFile, ISD, save, browser, twilio):
    '''
        INPUTS : csvFile (path to csv file; string), textFile(path to message body; string), ISD (country code; string), browser (Chrome/Firefox; string), twilio (Path to secrets.json; string)
        OUTPUT : None
    '''
    # Function Calls
    raw = readCSV(csvFile)
    data = process(raw, ISD)
    msg = readTXT(textFile)
    # Checks if using twilio or selenium
    if browser:
        sendMsgs(data, msg, save, browser)
    elif twilio:
        twilioAPI.main(data, msg, save, twilio)
# -----------------------------------------------------
if __name__ == "__main__":
    # Sets start time to find how long it took to execute
    t1 = time.time()

    # Sets up argument parser
    parser = argparse.ArgumentParser(description="Handles sending of messages through WhatsApp Web")
    parser.add_argument('-f', '--csvFile', help="Use this flag to specify the path to the csv file to load the data from")
    parser.add_argument('-t', '--textFile', help="Use this flag to specify the path to the text file to load message body from")
    parser.add_argument('-i', '--ISD', default='91', help="Use this flag to specify the ISD code to assume when it isn't specified in the CSV")
    parser.add_argument('-s', '--save', default=True, help="Use this flag to specify whether the logs should be saved or not")
    parser.add_argument('-b', '--browser', default='Chrome', help="Use this flag to specify which browser to use")
    parser.add_argument('-s', '--twilio', default=None, help="Use this flag to pass the path to the 'secrets.json' file to access Twilio API")
    args = parser.parse_args()

    print("State at Initialization")

    if args.twilio:
        print("Reading API Keys from {}".format(args.twilio))
    else:
        print("Browser used             : {}".format(args.browser))

    print("CSV file to read from    : {}".format(args.csvFile))
    print("Text file to read from   : {}".format(args.textFile))
    print("Country code from ISD    : {}".format(args.ISD))
    print("Saving Log?              : {}".format(args.save))

    # Calls main function
    main(args.csvFile, args.textFile, args.ISD, args.save, args.browser, args.twilio)

    # Prints the time it took to run the script
    print("Executed in {}s".format(time.time()-t1))
# -----------------------------------------------------