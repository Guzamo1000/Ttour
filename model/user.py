
from database.db import mysql
from flask import Flask, render_template, redirect,url_for,request,Blueprint, session, flash
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash


user=Blueprint("user",__name__)

user.permanent_session_lifetime = timedelta(minutes=1)
@user.route("/user")

@user.route("/userhome", methods=['GET', 'POST'])
def userhome():
    return render_template("home.html")

@user.route("/userlogin",methods=['GET','POST'])
def userlogin():
    """ 
    Login account user
    input: 
        user_Login
        Password_user
    output:
        return to function useruser adn session = user_Login
    """
    if request.method=='GET':
        print("get ma")
        return render_template("login.html")
    if request.method=='POST':
        print("post ma")
        user_name=request.form['username']
        password=request.form['password']
        cur=mysql.get_db().cursor()
        cur.execute(f"select top(1) * from user_1 where username ='{user_name}' and Password_user='{password}'")
        user=cur.fetchall()
        if user is not None:
            session['user']=user_name
            # session['id']=user[0]
            return redirect(url_for('user.userhome'))
    return render_template("login.html")


@user.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method=='GET':
        print("get ma")
        return render_template("register.html")
    else:
        username = request.form["username"]
        password_user = request.form["password_user"].encode('utf-8')
        nameuser = request.form["nameuser"]
        address_user = request.form["address_user"]
        phone_number_user = request.form["phone_number_user"]
        # has_password = bcrypt.hashpw(password_user, bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        cur.execute("insert into user_1 (username, password_user, name_user, address_user, Number_Phone_User) values (%s, %s,%s,%s, %s)",(username,has_password,nameuser,address_user,phone_number_user))
        mysql.connection.commit()
        session['nameuser'] = nameuser
        session['username'] = username
        return redirect(url_for(user.userhome))
        

@user.route("/logout")
def userlogout():
    """ 
    logout account user
    Remove user account from session and return function userlogin
    """
    session.pop('user',None)
    return redirect(url_for("user.userlogin"))