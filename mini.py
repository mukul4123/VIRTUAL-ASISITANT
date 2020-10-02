import hashlib
from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import request, render_template as rt
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia



warnings.filterwarnings('ignore')
#voice to text and return as string
def voicetotext():
  # Recording voice
  s=sr.Recognizer()
  # getting microphone access and start voice capture
  with sr.Microphone() as source:
    print('hello :-)')
    voice= s.listen(source)
  # using speech recognition
  data=''
  try:

    data=s.recognize_google(audio) 
    print('voice captured'+data) 
  except sr.UnknownValueError:
    print('sorry could not get what you said,please try again') 
  except sr.RequestError as e:
    print('request error'+e)
  
  return data

#response from va
def virtualresponse(text):
  print(text)
  #convert text to speech
  myobj=gTTS( text= text,lang='en', slow=False)
  #save the aodio to file
  myobj.save('virtual_response.mp3')
  #play the file
  os.system('start virtual_response.mp3')

text='hi how are you'
virtualresponse(text)
#function to open the va
def activate(text):
  activate_commands = ['hey buudy','khul ja sim sim'] #list of activate commands
  text=text.lower()
  for phrase in activate_commands:
    if phrase in text:
      return True
  return False 
#FUNCTION to display date 
def getDate():
  now =datetime.datetime.now()
  today_date=datetime.datetime.today()
  weekday=calendar.day_name[today_date.weekday()]
  monthnumber=now.month
  daynumber=now.day
  month_names=[ 'January', 'February', 'March', 'Aprril', 'May', 'June', 'July', 'August', 'September', 'October', 'November','december']
  ordinalnumbers=['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22th','23th','24th','25th','26th','27th','28th','29th','30th','30st']
  return 'today is '+weekday+' '+month_names[monthnumber-1]+' the ' +ordinalnumbers[daynumber-1]+'.'
# A function to return a random greeting response
def greeting(text):
  GREETING_INPUTS=['hi','hello','hey']
  GREETING_output=['hii','hello','hey']
  for word in text.split():
    if word.lower() in GREETING_INPUTS:
      return random.choice(GREETING_output) +'.'
    else:
      return random.choice( GREETING_output)+'.'
def wiki_search(text):

  searchlist=text.split()
  for i in range(0,len(searchlist)):
    if i+3 <= len(searchlist) -1 and searchlist[i].lower()=='who' and searchlist[i+1].lower()== 'is':
      return searchlist[i+2] +' '+ searchlist[i+3]



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
    return 'login successful for {}'.format(username)
    while True:
        text= voicetotext()
        response=' ' 
        #checking for wake command
        if(activate(text)== True):
            
            #checking for greetings by the user
            response=response + greeting(text)
            if('date' in text):
                get_date=getDate()
                response = response + ' '+ get_date
            if('time' in text):
                now =datetime.datetime.now()
                midday=' '
                if now.hour>12:
                    midday='p.m'
                    hour=now.hour -12
                else:
                    midday='a.m'
                    hour=now.hour
                if now.minute<10:
                    minute='0'+str(now.minute)
                else:
                    minute=str(now.minute)
                    response = response +' '+'IT is '+str(hour)+ ':'+minute+ ' '+midday+ '. '  
            if('who is' in text):
                domain = wiki_search(text)
                wiki = wikipedia.summary(domain,sentenses=2)
                response =response + ' ' +wiki_search
                virtualresponse(response)  





              
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


