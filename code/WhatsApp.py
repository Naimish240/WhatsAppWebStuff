# -----------------------------------------------------
# Created : 29th Aug 2020
# Author  : @Naimish240
# -----------------------------------------------------
# This program handles the sending of messages to each
# user from the csv file
# -----------------------------------------------------
import time, random, csv, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# -----------------------------------------------------
'''
    DISCLAIMER :
    I AM NOT RESPONSIBLE IF YOUR ACCOUNT GETS BANNED. CONSULT THE
    TERMS AND CONDITIONS OF WHATSAPP AND PROCEED WITH CAUTION.
    https://www.whatsapp.com/legal/

    Functions found here:
        checkFolder()                : Checks if the folder 'LOGs' exists, to save logs 
        randDist(mu, sig, low, high) : Generates random time from a gaussian distribuiton for sleep function
        openWebsite(url)             : Opens the WhatsApp Web website
        openContact(driver, number)  : Opens the URL for the person to send the message to
        sendMessages(driver, text)   : Sends the text message to the person
        saveLOG(success, failed)     : Saves the LOGs
        main(numbers, text, save)    : Controls the flow loop
'''
# -----------------------------------------------------
# Function to check if CSV/ exists. Else, creates it
def checkFolder():
    '''
        INPUTS : None
        OUTPUT : None
    '''
    if os.path.exists('LOGs'):
        pass
    else:
        os.mkdir('LOGs')
# -----------------------------------------------------
# Function to identify time from gaussian
def randDist(mu, sig, low, high):
    '''
        INPUTS : mu (mean), sig (standard deviation), low (lower limit), high (upper limit)
        OUTPUT : x (time to sleep for in seconds)
    '''
    x = random.gauss(mu, sig)
    if x < low:
        return low
    if x > high:
        return high
    return x
# -----------------------------------------------------
# This function opens up the whatsapp web website
def openWebsite(url, browser):
    '''
        INPUTS : url (url of website, string)
        OUTPUT : driver (selenium object)
    '''
    # Tries to load drivers from PATH, if configured properly
    try:
        # Loads the browser
        if browser.lower() == 'chrome':
            # Creates a chromedriver object
            driver = webdriver.Chrome()
        elif browser.lower() == 'firefox':
            # Creates a geckodriver object
            driver = webdriver.Firefox()
    # Unable to load driver. Prompts user to download and save in this folder
    except:
        print("Error! Unable to locate the webdriver")
        print("Download the driver and save the executable in the 'code/' folder!")
        return None

    # Opens the URL
    driver.get(url)
    print("Scan QR Code")
    # Waits for 20 seconds for user to authenticate session from their phone
    time.sleep(20)
    # Returns the driver object to main
    return driver
# -----------------------------------------------------
# Function to open the contact of that user
def openContact(driver, number):
    '''
        INPUTS : driver (selenium object), number (phone number of person to send message to; int)
        OUTPUT : driver (selenium object)
    '''
    # Contact URL of person
    driver = driver.get("https://web.whatsapp.com/send?phone={}".format(number))
    # Waits for a random amount of time after opening the user's contact, to avoid detection
    t = randDist(7, 3, 2, 13)
    time.sleep(t)
    # Returns driver object to main
    return driver
# -----------------------------------------------------
# Function to send the message to the user
def sendMessages(driver, text):
    '''
        INPUTS : driver (selenium object), text (message to send, string)
        OUTPUT : None
    '''
    # Finds element to shove text into
    usrMSG = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    # Loops through each character
    for char in text:
        t = randDist(0.015, 0.01, 0.002, 0.03)
        time.sleep(t)
        usrMSG.send_keys(char)
    # Waits another 0.25 seconds before pressing send
    time.sleep(0.25)
    usrMSG.send_keys(Keys.ENTER)
# -----------------------------------------------------
# Function to save logs.csv
def saveLOG(success, failed):
    '''
        INPUTS : data (log data)
        OUTPUT : None (saves data)
    '''
    # filepath and name declaration
    filename = "LOGs/{}_log.csv".format(time.time())
    fields = ["Phone_Number", "Message", "Status"]
    # Generates data for saving into csv
    data = []
    for i in success:
        data.append(i + ['success'])
    for i in failed:
        data.append(i + ['failed'])
    # Opens file
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)
# -----------------------------------------------------
# Main function, called externally
def main(numbers, text, save=True, browser='Chrome'):
    '''
        INPUTS : data (list of numbers and the corresponding messages to be sent)
        OUTPUT : res (list, count of [successful, failed])

        NOTE : SENDS SAME MESSAGE TO ALL USERS
    '''
    # Stores log
    success = []
    failed = []
    # Handles signin
    try:
        # Opens website
        print("Opening website")
        driver = openWebsite("https://web.whatsapp.com", browser)
        # QR code scanned successfully
        print("Session Authenticated!")
    except:
        # Unsuccessful attempt
        print("Unable to connect to website! Check your connection!")
        return None

    # Drivers haven't been configured properly
    if not driver:
        print("Driver not configured properly!")
        return None

    # If successfully signed in
    for number in numbers:
        try:
            print("Finding Contact {}".format(text))
            driver = openContact(driver, number)
            print("Contact Found!")
            print("Sending Message {}".format(text))
            sendMessages(driver, text)
            print("\033[32mSent Message to {} successfully!\033[00m".format(number))
            success.append([number, text])
        except:
            print("\033[91mUnable to send message to {}!\033[00m".format(number))
            failed.append([number, text])
   
    # Saves log data
    if save:
        # Checks if log folder exists
        checkFolder()
        # Dumps log
        saveLOG(success, failed)
    
    # Returns success/failed matrix
    return([len(success), len(failed)])
# -----------------------------------------------------