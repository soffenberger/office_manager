

#!/usr/bin/env python
#
### Libraries, will need to update a dependency install thing #############

from __future__ import print_function
import httplib2
import qrcode
import os
import json
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from apiclient import errors
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from datetime import datetime, timedelta
import parsedatetime as pdt


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

####### Things that should be configured by the users ########################

#calendar_name = "Official"
#subject_key = "Note"



    


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
# Can add more API's in the future when it gets there
#'https://mail.google.com/' + 
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly' + ' https://mail.google.com/' + ' https://www.googleapis.com/auth/hangouts.readonly'
CLIENT_SECRET_FILE = 'client.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

########### Enables the use of google API's as Spencer for questions #############



def start_up():
    if  os.path.exists(".office_profile.json"):
        with open(".office_profile.json", "r") as file:
            data = json.load(file)
            calendar_name = data["calendar_name"]
            subject_key = data["subject_key"]
            user_name = data["user_name"]
            
    else:
        with open(".office_profile.json", "w+") as file:
            calendar_name = raw_input("What is the name of the calendar? ")
            subject_key = raw_input("What subject will the messages have? ")
            user_name = raw_input("What name should I call you? ")
            data = {"calendar_name": calendar_name, "subject_key": subject_key, "user_name": user_name}
            json.dump(data, file)
    if os.path.exists("message_log.txt"):
        pass
    else:
        with open("message_log.txt", 'w+'):
            os.utime("message_log.txt", None)

    return (calendar_name, subject_key, user_name)
            
    

def check_past_message(message):
    time = message.split(" ^% ")[1].replace("\n","")
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    mss = message.split(" ^% ")[0]
    if mss.lower() == "reset":
        user_message = ""
    else:
        cal = pdt.Calendar()
        parse_time = cal.parseDT(mss, time)
        if (parse_time[1] == 0 or datetime.now() < parse_time[0]):
            user_message = mss
        else:
            user_message = ""
            
        
    return user_message
                

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

###### Google hangouts information ####################
def get_google_hangouts():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service3 = discovery.build('plusDomains', 'v1', http=http)
    print(dir(service3))



###### Switching the calendar info to its own function ######

def get_google_calendar():
    (calendar_name, subject_key, user_name) = start_up()
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service2 = discovery.build('calendar', 'v3', http=http)
    calendars = service2.calendarList().list().execute()
    with open(".gmail.txt", 'r') as file:
        google_email = file.read()
        name = google_email.split("<")[0] 
    for g in calendars['items']:
        if g['summary'] == calendar_name:
            calendar_id = g['id']

    now = datetime.now()
    dates = [now + timedelta(days=i) for i in range(0 - now.weekday(), 5 - now.weekday())]
    dict_dates = []
    for i in dates:
        start_time = i.strftime("%Y-%m-%dT0:0:0") + "Z"
        end_time = i.strftime("%Y-%m-%dT23:59:59") + "Z"
        events = service2.events().list(calendarId = calendar_id, singleEvents = 1, maxResults = 1, timeMin=start_time, timeMax=end_time).execute()
    #print(events)
        try:
            dict_dates.append(
            { 
            "event_summary": events['items'][0]['summary'],
            "event_timezone": events['timeZone'],
            "event_end": (events['items'][0]['end']['dateTime'].split("T")[0],events['items'][0]['end']['dateTime'].split("T")[1].split("-")[0][0:5]),
        "event_start": (events['items'][0]['start']['dateTime'].split("T")[0],events['items'][0]['start']['dateTime'].split("T")[1].split("-")[0][0:5]) }
            )
        except IndexError:
            dict_dates.append("")
            text_to_print = []
    for i in range(5):
        if len(dict_dates[i]) > 0:
            text_to_print.append(dict_dates[i]["event_summary"]  + "\n" + dict_dates[i]["event_start"][1]  + "-" + dict_dates[i]["event_end"][1])
        else:
            text_to_print.append("No Events")
    return (text_to_print , name)

   
####### Function that connects gmail and looks for messages #######3
####### Also this function looks at calendar and gets the ##########
###### Most recent calendar event ##################################


def get_google_information():
    (calendar_name, subject_key, user_name) = start_up()
    #global service
    global google_email
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    
    user_message = ""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    messages = service.users().messages().list(userId= 'me', maxResults = 5).execute()
    
    for i in messages['messages']:
        for g in service.users().messages().get(userId = 'me', id = i['id']).execute()['payload']['headers']:
        #print(g['name'])
            if g['name'] == "to" or g['name'] == "Delivered-To" or g['name'] == "To" :
                    google_email = g["value"]
            elif g["name"] == "from" or g["name"] == "From" :   
                    senders_email = g["value"]
            elif g["name"] == "Subject":
                    subject = g["value"]
        try:
            if senders_email.split("<")[1].split(">")[0]:
                    if (str(subject_key) in str(subject) or "reset" in subject.lower()): 
                        if (str(subject).lower() != "reset"):
                                user_message = service.users().messages().get(userId = 'me', id = i['id']).execute()['snippet']
                                service.users().messages().delete(userId = 'me', id = i['id']).execute()
                                now = datetime.now()
                
                                with open("message_log.txt" , "a") as file:
                                    file.write(user_message + " ^% " + str(now) + "\n")

                        else:
                                service.users().messages().delete(userId = 'me', id = i['id']).execute()
                                now = datetime.now()
                    
                                with open("message_log.txt" , "a") as file:
                                    file.write("reset" + " ^% " + str(now) + "\n")
                                    user_message = ""
                    else:
                        with open("message_log.txt" , "r") as file:
                                prev_mess = file.readlines()[-1].decode()
                                user_message= check_past_message(prev_mess)
                    
    
        except IndexError as e:
            pass
    
        if os.path.exists(".gmail.txt"):
            pass
        else:
            with open(".gmail.txt", 'w+') as file:
                file.write(google_email) 
        with open(".gmail.txt", 'r') as file:
            google_email = file.read()
        name = google_email.split("<")[0] 
        if user_message:
            return(True, user_message, name)
        else:
            return(False, "", name)
            

def qr_code():
    with open(".gmail.txt", 'r') as file:
        email = file.readline() 
        qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        )
    qr.add_data("mailto:{0}".format(email))
    qr.make(fit=True)
    img = qr.make_image()
    img.save("qr_code.png")
    return img

"""
def create_message(msg, name, email, waiting):
    global service, google_email
    message = MIMEText(msg)
    message['to'] = google_email
    message['from'] = google_email
    if waiting:
        message['subject'] = "Just wanted to let you know {0}({1}) is waiting".format(name, email)
    else:
        message['subject'] = "Just wanted to let you know {0}({1}) dropped by".format(name, email)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}
"""

def send_message():#msg, name, email, waiting):
    qr_code()
    """
    message = create_message(msg, name, email, waiting)
    message = service.users().messages().send(userId = 'me', body=message).execute()
    return message
    """


         

def main():
    hj = get_google_information()



if __name__ == '__main__':
    main()
