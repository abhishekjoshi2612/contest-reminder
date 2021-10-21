import os
import json
import urllib3
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail
from flask import Flask, render_template, url_for, redirect,request,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table
from flask_migrate import Migrate
import jinja2
import pickle

app = Flask(__name__)
app.config.update(
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT = '465',
MAIL_USE_SSL = True,
MAIL_USERNAME = 'username@gmail.com',
MAIL_PASSWORD = 'pasword'
)
mail = Mail(app)
app.config['SECRET_KEY'] = 'mysecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
#creating database

def se():
    with app.app_context():
        https = urllib3.PoolManager()
        r = https.request('GET','https://www.kontests.net/api/v1/all')
        sitedata = json.loads(r.data.decode('utf-8'))
        hg = Userdb.query.all()
        for i in sitedata:
         for users in hg:
             name = i["site"]
             if name == "CodeForces":
                 if users.codeforces == 1 and i["in_24_hours"] == "Yes":
                     mail.send_message(users.username + 'your  ' + i["site"] + 'contest is in 24 hours',sender = 'abhishekjoshi26121999@gmail.com',recipients = [users.email],body = i["site"] + ' contest in 24 hours')
             if name == "CodeChef":
                 if users.codechef == 1 and i["in_24_hours"] == "Yes":
                     mail.send_message(users.username  + 'your  ' + i["site"] + 'contest is in 24 hours',sender = 'abhishekjoshi26121999@gmail.com' ,recipients = [users.email],body = i["site"] + ' contest in 24 hours')
             if name == "HackerRank":
                 if users.hackerank == 1 and i["in_24_hours"] == "Yes":
                     mail.send_message(users.username  + 'your  ' + i["site"] + 'contest is in 24 hours',sender = 'abhishekjoshi26121999@gmail.com' ,recipients = [users.email],body = i["site"] + ' contest in 24 hours')



#local_server = True





class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __init__(self,username,email):
        self.username = username
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username



class Userdb(db.Model):
    __tablename__ = "Userdb"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    codeforces = db.Column(db.Integer,nullable=False)
    codechef = db.Column(db.Integer,nullable=False)
    hackerank = db.Column(db.Integer,nullable=False)
    def __init__(self,username,email,codeforces,codechef,hackerank):
        self.username = username
        self.email = email
        self.codeforces = codeforces
        self.codechef = codechef
        self.hackerank = hackerank
    def __repr__(self):
        return '<User %r>' % self.username





#no need to create form bcz forms we are using are html
#ju = 'adkdj@gmail.com'
#mr = User.query.filter_by(email=ju).first()
#if mr is None:

@app.route('/')
def hi():
    return render_template('index.html')

@app.route('/basefile')
def basefile():
    return render_template('index.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        me = User(username = username,email=email)
        mo = Userdb(username = username,email=email,codeforces=1,codechef=1,hackerank=1)
        gh = User.query.filter_by(email=request.form["email"]).first()
        if gh is None:
            db.session.add(me)
            db.session.commit()
            db.session.add(mo)
            db.session.commit()
            flash('You are Succesfully Registered in the database')
            session['user'] = email
            return render_template('index.html')

        else:
            flash('Your email is not unique')
            return render_template('index.html')



@app.route('/login',methods = ['GET','POST'])
def login():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        username = request.form["username"]
        email = request.form["emails"]
        bd = User.query.filter_by(email = request.form["emails"]).first()
        if bd is None or bd.email != email or bd.username != username :
            return render_template('index.html')
        else:
            session['user'] = email
            return render_template('dashboard.html')


@app.route('/logout',methods=['GET','POST'])
def logout():
    if 'user' in session:
        session.pop('user',None)
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/submitcontest',methods = ['GET','POST'])
def submitcontest():
    if 'user' in session:
        cf = request.form.get('codeforces')
        cc = request.form.get('codechef')
        hk = request.form.get('hackerank')
        cfs = 1
        ccs = 1
        hks = 1
        if cf is None:
            cfs = 0
        if cc is None:
            ccs = 0
        if hk is None:
            hks = 0
        cbt = session['user']
        Userd = Userdb.query.filter_by(email = cbt).first()
        Userd.codeforces = cfs
        Userd.codechef = ccs
        Userd.hackerank = hks
        db.session.commit()
        return render_template('index.html')


@app.route("/removeaccount",methods = ['GET','POST'])
def removeaccount():
    if request.method == "POST":
        username = request.form["namer"]
        email = request.form["emailer"]
        bd = User.query.filter_by(email = request.form["emailer"]).first()
        bds =  Userdb.query.filter_by(email = request.form["emailer"]).first()
        db.session.delete(bd)
        db.session.delete(bds)
        db.session.commit()
    return render_template('index.html')


@app.route("/codechef",methods = ['GET','POST'])
def codechef():
    return render_template('codechef.html')

@app.route("/codeforces",methods = ['GET','POST'])

def codeforces():
    return render_template('codeforces.html')

@app.route("/predict",methods = ['GET','POST'])
def predict():
    return render_template('predict.html')

sched = BackgroundScheduler(daemon=True)
sched.add_job(se,'interval',minutes= 720)
sched.start()

if __name__ == "__main__":
    app.run(debug=True)
