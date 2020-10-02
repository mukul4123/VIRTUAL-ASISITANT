import speech_recognition as sr
from gtts import gTTS
import playsound
import time
import os
from time import ctime
import re
import webbrowser
import bs4
import requests
import smtplib
import hashlib
from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import request, render_template as rt
import warnings
import calendar
import random
import wikipedia



def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening..")
        audio = r.listen(source,phrase_time_limit = 10)
    data = ""
    try:
        data = r.recognize_google(audio,language='en-US')
        print("You said:"+data)
    except sr.UnknownValueError:
        print("I cannot hear you")
    except sr.RequestError as e:
        print("Request Failed")
    return data
def respond(String):
    print(String)
    tts = gTTS(text=String,lang="en")
    tts.save("speech.mp3")
    playsound.playsound("speech.mp3")
    os.remove("speech.mp3")





users={}
class Register(object):
  def __init__(self,app):
    self.app =app
  def signup(self,username,password):
    hash=hashlib.md5(password.encode())
    users.update({username:hash.hexdigest()})
  def login(self,username,password):
    hash=hashlib.md5(password.encode())
    if users[username]==hash.hexdigest():
      return True
    else:
      return False
u1=Register('obj')
u1.signup('just','halo')



app = Flask(__name__)
userobj = Register(app) #start app instance
run_with_ngrok(app) #starts ngrok when app is run



@app.route("/")
def index():
  return rt('index.html')



@app.route("/signup",methods=["POST"])
def reg():
  username = request.form.get("username")
  password = request.form.get("password")
  userobj.signup(username,password)
  return "{} successfully Registered".format(username)



@app.route("/login",methods=["POST"])
def login():
  username = request.form.get("username")
  password = request.form.get("password")
  auth=userobj.login(username,password)
  if auth:
    print('login successful for {}'.format(username))
    while True:
        def voice_assistant(data):
            if "how are you" in data:
                listening =True
                respond("I am doing good")
            if "time" in data:
                listening = True
                respond(ctime())
            if "open google" in data.casefold():
                listening = True
                reg_ex = re.search('open google(.*)',data)
                url = 'https://www.google.com/'
                if reg_ex:
                    sub = reg_ex.group(1)
                    url = url + 'r/'
                webbrowser.open(url)
                print('Done')
                respond('Done')
            if "email" in data:
                listening = True
                respond("Whom should i send email to?")
                to = listen()
                edict = {'hello':'sakethreddy.kallepu@gmail.com','just':'codegnan@gmail.com'}
                toaddr = edict[to]
                respond('What is the subject')
                subject = listen()
                respond("What should i tell the person")
                message=listen()
                content = 'Subject:{}\n\n{}'.format(subject,message)
                #init gmail smtp
                mail = smtplib.SMTP('smtp.gmail.com',587)
                #identify the server
                mail.ehlo()
                mail.starttls()
                #login
                mail.login('qwertyforwork@gmail.com','jyppeoscgghmqlbf')
                mail.sendmail('qwertyforwork@gmail.com',toaddr,content)
                mail.close()
                respond('Email sent')
            if "search" in data.casefold():
                listening = True
                respond("What should i search")
                query = listen()
                response = requests.get("https://en.wikipedia.org/wiki/"+query)
                if response is not None:
                    html = bs4.BeautifulSoup(response.text,'html.parser')
                    paragraphs=html.select("p")
                    intro = [i.text for i in paragraphs]
                    halo =' '.join(intro)
                respond(halo[:200])

            if "stop" in data:
                listening = False
                print("Listening Stopped")
                respond("See you Saketh")

            try:
                return listening
            except UnboundLocalError:
                print("timedout")
    
        respond("Hello user,what can i do for you?")
        listening = True
        while listening == True:
            data = listen()
            listening = voice_assistant(data)




  else:
      return 'Wrong password'


@app.route("/users")
def data():
  return users

@app.route("/toregister")
def toregister():
  return rt("register.html")

@app.route("/tologin")
def tologin():
  return rt("login.html")

app.run()      


