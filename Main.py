debug = False

if debug: print("program started")
#import dependencies
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import numpy as np

if debug: print("libraries loaded")

#load variables
reader = SimpleMFRC522()

cache = np.array()

if debug: print("variables loaded")

#open log file
with open('log.csv', 'a') as log:
    pass

if debug: print("loaded log file")

#----------------------------------------------------------------------------------------#

#connect to spreadsheet
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('./roboticsrfidsignin.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open('Test')

# get the third sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(2)

if debug: print("connected to sheet")

#----------------------------------------------------------------------------------------#

#reader function
def readCard():
    try:
        _, id = reader.read()
        print(id)
        return id
    except Exception as e:
        if debug:print(e)
        return None
    # finally:
    #         GPIO.cleanup()

#send data to spreadsheet
def sendData(id, time):
    sheet_instance.update('A2:B2', [[int(id), int(time)*1000]])
    # print(id)

#log id to csv file
def logID(id):
    with open ('log.csv', 'a') as log:
        log.write(str(id).strip() + ',' + str(time.time()).strip() + "\n")

#check if the id is in the sheet
def isUpdated(id):
    lastID = sheet_instance.cell(4,2)
    if id == lastID:
        return True
    return False
    
if debug: print("functions loaded")

#----------------------------------------------------------------------------------------#

#main function
def main():
    cache = None
    while True:
        id = readCard()
        if id != cache:
            sendData(id, time.time())
            print("Sent data to spreadsheet")
            if not isUpdated(id):
                logID(id)
        time.sleep(1)
        cache = id
            
if debug: print("reading")

if __name__ == "__main__":
    main()