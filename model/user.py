
from urllib import response
from database.db import mysql
from flask import Flask, render_template, redirect,url_for,request,Blueprint, session, flash
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import bcrypt

user=Blueprint("user",__name__)

user.permanent_session_lifetime = timedelta(minutes=1)
@user.route("/user")
@user.route("/userhome", methods=['GET', 'POST'])
def userhome():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM tour limit 3")
    attract_tours = cur.fetchall()
    cur.execute("SELECT * FROM tour limit 3")
    tours = cur.fetchall()
    cur.execute("select image_1, place.name_place from tour inner join place on tour.p_id = place.p_id group by place.p_id order by count(place.p_id) DESC limit 5")
    places = cur.fetchall()
    return render_template("home.html", attract_tours = attract_tours, tours = tours, places = places)


@user.route("/userlogin",methods=['GET','POST'])
def userlogin():
    if request.method=='GET':
        return render_template("userlogin.html")
    if request.method=='POST':
        user_name=request.form['user_name']
        password=request.form['user_password']
        cur=mysql.get_db().cursor()
        cur.execute(f"select * from user_1 where username ='{user_name}' and Password_user='{password}'")
        user = cur.fetchall()
        if user is not None:
            session['name_user']=user_name
            session['id']= user[0][0]
            
            return redirect(url_for('user.userhome'))
        return redirect(url_for('user.userhome'))

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
        has_password = bcrypt.hashpw(password_user, bcrypt.gensalt())
        
        cur=mysql.get_db().cursor()
        
        cur.execute("insert into user_1 (username, has_password, name_user, address_user, Number_Phone_User) values (%s, %s,%s,%s, %s)",(username,password_user,nameuser,address_user,phone_number_user))
        mysql.get_db().commit()
        session['name_user'] = nameuser
        session['user_name'] = username
        return redirect(url_for("user.userhome"))
        

@user.route("/userlogout")
def userlogout():
    """ 
    logout account user
    Remove user account from session and return function userlogin
    """
    session.pop('user',None)
    return redirect(url_for("user.userlogin"))

@user.route("/readattracttour")
def readattract():
    cursor = mysql.get_db().cursor()
    response = cursor.execute("SELECT * FROM tour limit 3")
    if response > 0:
        attract_tours = cursor.fetchall()
        return redirect(url_for("user.userhome", attract_tours = attract_tours))


@user.route("/userinfo",methods=['GET','POST'])
def userinfo():
    cur = mysql.get_db().cursor()
    u_id = session["id"]

    cur.execute(f"SELECT * FROM user_1 where u_id = {u_id}")
    user = cur.fetchall()
    cur.execute(f"select user_1.U_id,tour.T_id,O_id,Name_user,Name_Tour,order_tour.Price,Order_Date, order_tour.Amount_of_people, tour.Vehicle, tour.Name_Hotel, status_Order from order_tour inner join tour on tour.T_id=order_tour.T_id inner join user_1 on user_1.U_id=order_tour.U_id where user_1.u_id = {u_id}")
    booking = cur.fetchall()
    return render_template("userManageTour.html", user = user, booking = booking)


@user.route("/tour",methods=['GET','POST'])
def usertour():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM tour")
    tour = cur.fetchall()
    return render_template("userTour.html", tour = tour)

@user.route("/attracttour",methods=['GET','POST'])
def userattracttour():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM tour limit 9")
    tour = cur.fetchall()
    return render_template("userTour.html", tour = tour)

@user.route("/usertourdetail/<T_id>",methods=['GET','POST'])
def usertourdetail(T_id):
    T_id = T_id
    cur = mysql.get_db().cursor()
    cur.execute(f"SELECT * FROM tour where t_id={T_id}")
    tour = cur.fetchall()
    print(tour)
    if request.method == "GET":
        return render_template("userTourDetail.html", tour = tour)
    
@user.route("/userchangeinfo",methods=['GET','POST'])
def userchangeinfo():
    if request.method=='POST':
        cur = mysql.get_db().cursor()
        u_id = session["id"]
        name_user=request.form['name_user']
        user_name=request.form['user_name']
        phone_number = request.form['phone_number']
        user_address = request.form['user_address']
        cur.execute(f"update user_1 set username = '{user_name}', name_user = '{name_user}', address_user = '{user_address}', number_phone_user = '{phone_number}' where u_id = {u_id}")
        user = cur.fetchall()
        mysql.get_db().commit()
        # if user is not None:
        #     session['name_user']=user_name
        #     session['id']= user[0][0]
            
        #     return redirect(url_for('user.userhome'))
        return redirect(url_for('user.userhome'))

@user.route("/usercanceltour/<O_id>",methods=['GET','POST'])
def usercanceltour(O_id):
    O_id = O_id
    cur = mysql.get_db().cursor()
    cur.execute(f"update order_tour set status_Order = 2 where o_id={O_id}")
    mysql.get_db().commit()
    if request.method == "GET":
        return redirect(url_for('user.userinfo'))
    
@user.route("/usersearch", methods = ['GET','POST'])
def usersearch():
    keysearch = request.form['key_search']
    cur=mysql.get_db().cursor()
    cur.execute(f"SELECT t_id, place.p_id, a_id, name_tour, name_hotel, vehicle, price, Describe_Tour, Schedule_Tour, Time_tour, Image_1, Image_2,Image_3, Image_4, Image_5 FROM ttour.tour inner join place where name_tour like '%{keysearch}%' or place.name_place like '%{keysearch}%'")
    tour = cur.fetchall()
    return render_template("userSearch.html", tours = tour, keysearch = keysearch)

