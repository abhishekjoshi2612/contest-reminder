import os
from flask import Flask, render_template, url_for, redirect,request,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)

#creating database

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

#no need to create form bcz forms we are using are html
#ju = 'adkdj@gmail.com'
#mr = User.query.filter_by(email=ju).first()
#if mr is None:
    ms = User(username = "dsjfdsj",email="adkdj@gmail.com")
    db.session.add(ms)
    db.session.commit()

@app.route('/')
def hi():
    return render_template('base_file.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        me = User(username = username,email=email)
        gh = User.query.filter_by(email=request.form["email"]).first()
        if gh is None:
            db.session.add(me)
            db.session.commit()
            flash('You are Succesfully Registered in the database')
            return render_template('registerpage.html')

        else:
            flash('Your email is not unique')
            return render_template('base_file.html')



@app.route('/login',methods = ['GET','POST'])
def login():
    if session['logged_in'] == True:
        return render_template('dashboard.html')
    else:
        username = request.form["username"]
        email = request.form["emails"]
        bd = User.query.filter_by(email = request.form["emails"]).first()
        if bd is None or bd.email != email or bd.username != username :
            return render_template('/')
        else:
            session['user'] = email
            session['logged_in'] = True
            return render_template('dashboard.html')


@app.route('/logout',methods=['GET','POST'])
def logout():
    if session['logged_in'] == True:
        session.clear()
        return render_template('/')
    else:
        return render_template('/')










if __name__ == "__main__":
    app.run(debug=True)
