import hashlib
from flask_ngrok import run_with_ngrok
from flask import Flask
from flask import request, render_template as rt
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

u = Register('obj')
u.signup('just','halo')



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


