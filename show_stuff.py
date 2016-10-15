

#!/usr/bin/env python
#
### Libraries, will need to update a dependency install thing #############

from __future__ import print_function
import httplib2
#import requests 
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
from oauth2client.client import AccessTokenCredentials
from oauth2client import client
from oauth2client import tools
from datetime import datetime, timedelta
import parsedatetime as pdt


try:
    import argparse
    #flags = argparse.Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=True)
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
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly' + ' https://mail.google.com' + ' https://www.googleapis.com/auth/plus.me' 
CLIENT_SECRET_FILE = 'client.json'
APPLICATION_NAME = 'Office Manager'

########### Enables the use of google API's as Spencer for questions #############



def start_up(): 
    if  os.path.exists(".office_profile.json"):
        with open(".office_profile.json", "r") as file:
            data = json.load(file)
            calendar_name = "Official" #data["calendar_name"]
            subject_key = "Note" #data["subject_key"]
            
    else:
        with open(".office_profile.json", "w+") as file:
            calendar_name = "Official"
            subject_key = "Note"
            data = {"calendar_name": calendar_name, "subject_key": subject_key}
            json.dump(data, file)
    if os.path.exists("message_log.txt"):
        pass
    else:
        with open("message_log.txt", 'w+'):
            os.utime("message_log.txt", None)

    return (calendar_name, subject_key)
            
    

def check_past_message(message):
    print("Message " + message)
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
    print("Output" + user_message) 
    return user_message
                
"""
def get_credentials():
    if  os.path.exists("refresh.json"):
        with open("refresh.json") as file:
            refresh = json.load(file)
    else:
        ss.refresh()
    credentials = AccessTokenCredentials(refresh['access_token'],'my-user-agent/1.0')
    return credentials


def refresh(device_code):
    with open("client.json") as file:
        data = json.load(file)
    if  os.path.exists("refresh.json"):
        with open("refresh.json") as file:
            refresh = json.load(file)
            payload = {
            'client_id' : data['installed']['client_id'],
            'client_scret': data['installed']['client_secret'] + "&",
            'refresh_token': refresh['refresh_token'],
            'grant_type': 'http://oauth.net/grant_type/device/1.0' 
            }
            headers = {"Content-type": "application/x-www-form-urlencoded",
            "Host": "www.googleapis.com"
            }
            conn = requests.post("https://www.googleapis.com/oauth2/v4/token", data=payload, headers=headers)

        with open("refresh.json", "w+") as file:
            json.dump(conn.json(), file)
        refresh = conn.json()
    else:
        payload = {
        'client_id' : data['installed']['client_id'],
        'client_scret': data['installed']['client_secret'] + "&",
        'code': device_code,
        'grant_type': refresh_token 
        }
        headers = {"Content-type": "application/x-www-form-urlencoded",
           "Host": "www.googleapis.com"
        }
        conn = requests.post("https://accounts.google.com/o/oauth2/device/code", data=payload, headers=headers)
"""    


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
            #print(credentials)        
    
        #else: # Needed only for compatibility with Python 2.6
        #    credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    """
    with open("client.json") as file:
        data = json.load(file)
    payload = {
    'client_id' : data['installed']['client_id'],
    'scope' : SCOPES,
    }
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Host": "accounts.google.com"
    }
    conn = requests.post("https://accounts.google.com/o/oauth2/device/code", data=payload, headers=headers)
    """
    qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=5,
    )
    qr.add_data("{0}".format(conn.json()['verification_url']))
    qr.make(fit=True)
    img = qr.make_image()
    img.save("verification_page.png")
    """
    print(conn.json()['user_code']) 
    return (conn.json()['user_code'], conn.json()['device_code'])
    """

###### Get google email ###############

def get_name():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service2 = discovery.build('plus', 'v1', http=http)
    user = service2.people().get(userId = 'me').execute()
    return str(user["displayName"])



###### Google hangouts information ####################

def need_to_set_calendar():
    pass



###### Switching the calendar info to its own function ######

def get_google_calendar():
    (calendar_name, subject_key) = start_up()
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service2 = discovery.build('calendar', 'v3', http=http)
    calendars = service2.calendarList().list().execute()
    #with open(".gmail.txt", 'r') as file:
    #    google_email = file.read()
    name = get_name()
    for g in calendars['items']:
        if g['summary'] == calendar_name:
            calendar_id = g['id']
            calendar_exists = True
            break
        else:
            need_to_set_calendar()
            calendar_exists = False
    if calendar_exists:
        now = datetime.now()
        dates = [now + timedelta(days=i) for i in range(0 - now.weekday(), 5 - now.weekday())]
        dict_dates = []
        for i in dates:
            start_time = i.strftime("%Y-%m-%dT0:0:0") + "Z"
            end_time = i.strftime("%Y-%m-%dT23:59:59") + "Z"
            #print(events, start_time) 
            events = service2.events().list(calendarId = calendar_id, singleEvents = 1, maxResults = 3, timeMin=start_time, timeMax=end_time).execute()
            if len(events["items"]) > 0:
                events_day = []
                for a in range(len(events["items"])):
                    events_day.append(
                    { 
                    "event_summary": events['items'][a]['summary'],
                    "event_timezone": events['timeZone'],
                    "event_end": (events['items'][a]['end']['dateTime'].split("T")[0],events['items'][a]['end']['dateTime'].split("T")[1].split("-")[0][0:5]),
                    "event_start": (events['items'][a]['start']['dateTime'].split("T")[0],events['items'][a]['start']['dateTime'].split("T")[1].split("-")[0][0:5])}
                            )
                    #print(events_day)
                    dict_dates.append(events_day)
            else:
                dict_dates.append("")
                text_to_print = [] 
        for i in range(5):
            if len(dict_dates[i]) > 0:
                day_events = []
                for h in range(len(dict_dates[i])):
                    day_events.append(dict_dates[i][h]["event_summary"]  + "\n" + dict_dates[i][h]["event_start"][1]  + "-" + dict_dates[i][h]["event_end"][1])
                    text_to_print.append(day_events)
            else:
                text_to_print.append(["No Events"])
    else:
        text_to_print = ""
        name = ""       
    return (text_to_print , name, calendar_exists)

   
####### Function that connects gmail and looks for messages #######3
####### Also this function looks at calendar and gets the ##########
###### Most recent calendar event ##################################


def get_google_information():
    (calendar_name, subject_key) = start_up()
    phone_number = get_num()
    #print(phone_number)
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
            #print(g['name'], g["value"])
            if g['name'] == "to" or g['name'] == "Delivered-To" or g['name'] == "To" :
                    google_email = g["value"]
            elif g["name"] == "from" or g["name"] == "From" :   
                    senders_email = g["value"]
            elif g["name"] == "Subject":
                    subject = g["value"]
        try:
            #print(google_email.split("<")[1].split(">")[0].lower(), senders_email.split("<")[1].split(">")[0].lower())
            if google_email.lower() in senders_email.lower() and (str(subject_key).lower() in str(subject).lower() or "reset" in subject.lower()):
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
            elif phone_number and phone_number in senders_email:
                 if (service.users().messages().get(userId = 'me', id = i['id']).execute()['snippet'].lower() != "reset"):
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
                    prev_mess = file.readlines()[-1]#.decode()
                    user_message= check_past_message(prev_mess)
                 
    
        except IndexError as e:
            pass
    
        #if os.path.exists(".gmail.txt"):
        #    pass
        #else:
        #    with open(".gmail.txt", 'w+') as file:
        #        file.write(google_email) 
        #with open(".gmail.txt", 'r') as file:
        #    google_email = file.read()
        name = get_name()#google_email.split("<")[0] 
        if user_message:
            #print(user_message)
            return(True, user_message, name)
        else:
            return(False, "", name)
            

def get_phone_number():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    messages = service.users().messages().list(userId= 'me', maxResults = 5).execute()
    
    for i in messages['messages']:
        for g in service.users().messages().get(userId = 'me', id = i['id']).execute()['payload']['headers']: 
            if g["name"] == "from" or g["name"] == "From" :   
                if g["value"][0].isdigit():
                    service.users().messages().delete(userId = 'me', id = i['id']).execute()
                    return g["value"]
                else:
                    return "Nothing yet"

def get_num():
   if os.path.exists(".phone_number.txt"):
        with open(".phone_number.txt", "r") as file:
            num_sig = file.readline()
        return num_sig
 
def store_phone_number(signature):
    with open(".phone_number.txt", "w+") as file:
        file.write(signature)

    
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



def send_message():
    qr_code() 


         

def main():
    hj = get_google_information()



if __name__ == '__main__':
    main()
