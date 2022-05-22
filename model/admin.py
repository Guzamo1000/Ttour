
from database.db import mysql
from flask import Flask, render_template, url_for, redirect, request, Blueprint, flash, session
from datetime import timedelta
admin = Blueprint('admin', __name__)
admin.permanent_session_lifetime = timedelta(minutes=1)
@admin.route("/admin")
@admin.route("/login",methods=['GET','POST'])
def adminlogin():
    """ 
    Login account admin
    input: 
        Admin_Login
        Password_Admin
    output:
        return to function adminuser adn session = Admin_Login
    """
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        user_name=request.form['username']
        password=request.form['password']
        cur=mysql.get_db().cursor()
        cur.execute(f"select * from admin_1 where Admin_Login='{user_name}' and Password_Admin='{password}'")
        admin=cur.fetchall()
        if admin is not None:
            session['admin']=user_name
            session['id']=admin[0]
            return redirect(url_for('admin.adminuser'))




@admin.route("/logout")
def adminlogout():
    """ 
    logout account admin
    Remove admin account from session and return function adminlogin
    """
    session.pop('admin',None)
    return redirect(url_for("admin.adminlogin"))




@admin.route("/adminuser", methods=['GET', 'POST'])
def adminuser():
    """
    Display customer information and tour booking history
    input: 
        Data in table
        - user_1
        - order_tour
        - order_detail
        - tour
    output: 
        information customer and booking history
    """
    cur = mysql.get_db().cursor()
    cur.execute(
        "select U_id,Name_user,Address_User,Number_Phone_User from user_1")
    user = cur.fetchall()
    # history=None
    nameadmin=None
    if "admin" in session:
        nameadmin=session['admin']
    else: 
        return redirect(url_for('admin.adminlogin'))
    if request.method == "POST":
        user_id = request.form["U_id"]
        if user_id is not None:
            cur.execute(
                f'select U_id,Name_Tour, Order_Date,Amount_of_people, order_tour.Price from order_tour inner join ttour.orderdetail on order_tour.O_id=orderdetail.OD_id inner join ttour.tour on orderdetail.OD_id=order_tour.O_id where order_tour.U_id={user_id}')
            history = cur.fetchall()
            return render_template("adminUser.html",nameadmin=nameadmin,user=user, history=history)

        print(user_id)
    cur.close()
    return render_template("adminUser.html", user=user)


@admin.route("/admintour", methods=['GET', 'POST'])
def tour():
    cur = mysql.get_db().cursor()
    if request.method == 'GET':
        cur.execute(
            "SELECT T_id,Name_hotel,Describe_Tour,Vehicle,Price FROM ttour.tour")
        tour = cur.fetchall()
        infor_tour = [[]]
        if tour is not None:

            return render_template("adminTour.html", tour=tour, infor_tour=infor_tour)
    cur.close()
    return render_template("adminTour.html")


@admin.route("/edittour/<T_id>", methods=['GET', 'POST'])
def getedit(T_id):
    T_id = T_id
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT T_id,Name_hotel,Describe_Tour,Vehicle,Price FROM ttour.tour")
    tour = cur.fetchall()
    cur.execute(
        f"SELECT T_id,Name_Tour,Name_Hotel,Vehicle,Time_tour,tour.Price, Schedule_Tour,Describe_Tour,Image_1,Image_2,Image_3,Image_4,Image_5 FROM ttour.tour where T_id={T_id}")
    infor_tour = cur.fetchall()
    # infor_tour=list(infor)
    print(infor_tour)
    if infor_tour is not None:
        if request.method == 'GET':
            # flash("Thông tin chi tiết của tour",'')
            return render_template("adminTour.html", tour=tour, T_id=T_id, infor_tour=infor_tour)
        if request.method == 'POST':
            nametour = request.form['nametour']
            namehotel = request.form['namehotel']
            vehicle = request.form['vehicle']
            time_tour = request.form['time_tour']
            price = request.form['price']
            schedule = request.form['schedule']
            describe = request.form['describe']
            cur.execute(f"Update tour SET Name_Tour= '{str(nametour)}', Name_Hotel='{str(namehotel)}', Vehicle='{str(vehicle)}',Time_tour='{str(time_tour)}'  tour.Price={price},  Schedule_Tour='{str(schedule)}',  Describe_Tour='{str(describe)}',  Image_1=null, Image_2=null, Image_3=null, Image_4=null, Image_5=null  where T_id={T_id} ")
            mysql.get_db().commit()
            flash("Dữ liệu tour đã được cập nhật", "info")
            # return render_template("adminTour.html",tour=tour,infor_tour=infor_tour)
            return redirect(url_for("admin.tour"))


@admin.route("/addtour", methods=['GET', 'POST'])
def addtour():
    cur=mysql.get_db().cursor()
    if request.method == 'GET':
        return redirect(url_for("admin.tour"))
    if request.method == 'POST':
        nametour = request.form['nametour']
        namehotel = request.form['namehotel']
        vehicle = request.form['vehicle']
        time_tour = request.form['time_tour']
        price = request.form['price']
        schedule = request.form['schedule']
        describe = request.form['describe']
        cur.execute("")

# @admin.route("/edittour/<T_id>", methods=['POST'])
# def postedit(T_id):
#     T_id=T_id
#     cur=mysql.get_db().cursor()
#     nametour = request.form['nametour']
#     namehotel = request.form['namehotel']
#     vehicle = request.form['vehicle']
#     price = request.form['price']
#     schedule = request.form['schedule']
#     describe = request.form['describe']
#     cur.execute(f"Update tour SET Name_Tour= '{str(nametour)}', Name_Hotel='{str(namehotel)}', Vehicle='{str(vehicle)}',  tour.Price={price},  Schedule_Tour='{str(schedule)}',  Describe_Tour='{str(describe)}',  Image_1=null, Image_2=null, Image_3=null, Image_4=null, Image_5=null  where T_id={T_id} ")
#     mysql.get_db().commit()
#     flash("Dữ liệu tour đã được cập nhật", "info")
#     # return render_template("adminTour.html",tour=tour,infor_tour=infor_tour)
#     return redirect(url_for("admin.getedit"))


@admin.route("/statistical", methods=['GET', 'POST'])
def statistical():
    pass
# @admin.route("/booktour", mthods=['GET','POST'])
# def booktour():
#     pass
