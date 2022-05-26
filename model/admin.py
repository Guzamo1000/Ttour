
import os

from database.db import mysql
from flask import Flask, render_template, url_for, redirect, request, Blueprint, flash, session
from datetime import timedelta
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

admin = Blueprint('admin', __name__)
admin.permanent_session_lifetime = timedelta(minutes=1)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@admin.route("/admin")
@admin.route("/adminbooking", methods=['GET', 'POST'])
def booktour():
    if "id" in session:
        cur = mysql.get_db().cursor()
        cur.execute("select user_1.U_id,tour.T_id,O_id,Name_user,Name_Tour,order_tour.Price,Order_Date,status_Order from order_tour inner join tour on tour.T_id=order_tour.T_id inner join user_1 on user_1.U_id=order_tour.U_id")
        booking = cur.fetchall()
        print(booking)
        if request.method == 'GET':
            infor_order = [[]]
            cur.close()
            return render_template("adminbookTour.html", booking=booking, infor_order=infor_order)
    else:
        return redirect(url_for("admin.adminlogin"))


@admin.route("/<U_id>/<T_id>", methods=['GET', 'POST'])
def checktour(U_id, T_id):
    U_id = U_id
    T_id = T_id
    print(U_id+" "+T_id)
    cur = mysql.get_db().cursor()
    cur.execute("select user_1.U_id,tour.T_id,O_id,Name_user,Name_Tour,order_tour.Price,Order_Date,status_Order from order_tour inner join tour on tour.T_id=order_tour.T_id inner join user_1 on user_1.U_id=order_tour.U_id")
    booking = cur.fetchall()
    cur.execute(
        f"select Name_user,tour.Name_Tour,tour.Vehicle,Order_Date,order_tour.Price,Amount_of_people,user_1.Number_Phone_User,status_Order from order_tour inner join tour on tour.T_id=order_tour.T_id inner join user_1 on user_1.U_id=order_tour.U_id where user_1.U_id='{U_id}' and tour.T_id='{T_id}'")
    infor_order = cur.fetchall()
    if request.method == 'GET':
        print(infor_order)
        print(U_id+" "+T_id)
        return render_template("adminbookTour.html", booking=booking, infor_order=infor_order)
    if request.method == 'POST':
        status = request.form['status']
        print(status)
        cur.execute(
            f"update order_tour set status_Order='{status}' where U_id={U_id} and T_id={T_id}")
        mysql.get_db().commit()
        return redirect((url_for("admin.booktour")))


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
    print(session["id"])
    nameadmin = None
    if "admin" in session:
        nameadmin = session['admin']
    else:
        return redirect(url_for('admin.adminlogin'))
    cur = mysql.get_db().cursor()
    cur.execute(
        "select U_id,Name_user,Address_User,Number_Phone_User from user_1")
    user = cur.fetchall()
    # history=None

    if request.method == "POST":
        user_id = request.form["U_id"]
        if user_id is not None:
            cur.execute(f'select U_id,O_id,tour.Name_Tour,time_start,Amount_of_people, order_tour.Price,status_Order from order_tour inner join tour on tour.T_id=order_tour.T_id where U_id={user_id}')
            history = cur.fetchall()
            return render_template("adminUser.html", nameadmin=nameadmin, user=user, history=history)

        print(user_id)
    cur.close()
    return render_template("adminUser.html", user=user)


@admin.route("/admintour", methods=['GET', 'POST'])
def tour():
    """
        Display the interface to view information of the tour already in the database
        input:

    """
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT T_id,Name_hotel,Describe_Tour,Vehicle,Price FROM ttour.tour")
    tour = cur.fetchall()
    infor_tour = [[]]
    cur.execute(f"Select * from place")
    place = cur.fetchall()
    if request.method == 'GET':

        if tour is not None:

            return render_template("adminTour.html",place=place,tour=tour, infor_tour=infor_tour)
        cur.close()
    if request.method == 'POST':
        place = request.form['place']
        nametour = request.form['nametour']
        namehotel = request.form['namehotel']
        vehicle = request.form['vehicle']
        time_tour = request.form['time_tour']
        price = request.form['price']
        schedule = request.form['schedule']
        describe = request.form['describe']
        image = request.form['image']
        print(image)
        A_id = session['id']
        print(A_id)
        cur.execute(
            f"insert into tour(P_id,A_id,Name_Tour,Name_Hotel, Vehicle, Price, Describe_Tour, Schedule_Tour, Time_tour, Image_1,Image_2,Image_3,Image_4,Image_5) values ('{place}','{A_id}','{nametour}','{namehotel}','{vehicle}','{price}','{describe}','{schedule}','{time_tour}',null,null,null,null,null)")
        mysql.get_db().commit()
        flash("Đã thêm tour mới", 'info')
        cur.execute(
            "SELECT T_id,Name_hotel,Describe_Tour,Vehicle,Price FROM ttour.tour")
        tour = cur.fetchall()
        return render_template("adminTour.html", tour=tour, infor_tour=infor_tour)
    # return render_template("adminTour.html")


@admin.route("/remove/<T_id>", methods=['GET'])
def deletetour(T_id):
    T_id = T_id
    cur = mysql.get_db().cursor()
    if request.method == 'GET':
        try:
            cur.execute(f"DELETE FROM tour WHERE T_id={T_id};")
            mysql.get_db().commit()
            return redirect(url_for("admin.tour"))
        except:
            flash("Tour đã được khách hàng đặt, vui lòng liên hệ hủy tour với khách hàng trước khi xóa tour", 'info')
            return redirect(url_for("admin.tour"))


@admin.route("/edittour/<T_id>", methods=['GET', 'POST'])
def touredit(T_id):
    """
    Edit tour information
    input:
        Edit data:
            nametour
            namehotel
            vehicle
            time_tour
            price
            schedule
            descipbe
    output:
        Update data on tour table
    """
    T_id = T_id
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT T_id,Name_hotel,Describe_Tour,Vehicle,Price FROM ttour.tour")
    tour = cur.fetchall()
    cur.execute(f"SELECT place.P_id,T_id,Name_Tour,Name_Hotel,Vehicle,Time_tour,tour.Price, Schedule_Tour,Describe_Tour,Image_1,Image_2,Image_3,Image_4,Image_5 FROM ttour.tour inner join place on place.P_id=tour.P_id where tour.T_id={T_id}")
    infor_tour = cur.fetchall()
    print(infor_tour[0][9])
    # cur.execute(f"Select Name_place from place where P_id={infor_tour[0][0]}")
    cur.execute(f"select * from place")
    place = cur.fetchall()
    print(place)
    # print(place[1][0])
    # print(place)
    if infor_tour is not None:
        if request.method == 'GET':
            # flash("Thông tin chi tiết của tour",'')
            return render_template("adminTour.html", place=place, tour=tour, T_id=T_id, infor_tour=infor_tour)
        if request.method == 'POST':
            place = request.form['place']
            A_id = session['id']
            nametour = request.form['nametour']
            namehotel = request.form['namehotel']
            vehicle = request.form['vehicle']
            time_tour = request.form['time_tour']
            price = request.form['price']
            schedule = request.form['schedule']
            describe = request.form['describe']

            image_1=request.files['image_1']
            image_1.save(secure_filename(image_1.filename))

            image_2=request.files['image_2']
            image_2.save(secure_filename(image_2.filename))
            image_3=request.files['image_3']
            image_3.save(secure_filename(image_3.filename))
            image_4=request.files['image_4']
            image_4.save(secure_filename(image_4.filename))
            image_5=request.files['image_5']
            image_5.save(secure_filename(image_5.filename))
            print(image_1.filename)
            cur.execute(f"Update tour SET P_id={place} ,A_id={str(A_id)}, Name_Tour= '{str(nametour)}', Name_Hotel='{str(namehotel)}', Vehicle='{str(vehicle)}', Time_tour='{str(time_tour)}' ,tour.Price={price},  Schedule_Tour='{str(schedule)}',  Describe_Tour='{str(describe)}',  Image_1='{image_1.filename}', Image_2='{image_2.filename}', Image_3='{image_3.filename}', Image_4='{image_4.filename}', Image_5='{image_5.filename}'  where T_id={T_id} ")
            mysql.get_db().commit()
            flash("Dữ liệu tour đã được cập nhật", "info")
            # return render_template("adminTour.html",tour=tour,infor_tour=infor_tour)
            return redirect(url_for("admin.tour"))


# @admin.route("/statistical", methods=['GET'])
# def statistical():
#     if request.method=='GET':

# @admin.route("/booktour", mthods=['GET','POST'])
# def booktour():
#     pass

@admin.route("/login", methods=['GET', 'POST'])
def adminlogin():
    """
    Login account admin
    input:
        Admin_Login
        Password_Admin
    output:
        return to function adminuser adn session = Admin_Login
    """
    if "admin" not in session:
        if request.method == 'GET':
            return render_template("login.html")
        if request.method == 'POST':
            user_name = request.form['username']
            password = request.form['password']
            cur = mysql.get_db().cursor()
            cur.execute(f"select * from admin_1 where Admin_Login='{user_name}' and Password_Admin='{password}'")
            admin = cur.fetchall()
            if 'admin' not in session:
                session['admin'] = user_name
                session['id'] = admin[0][0]
                return redirect(url_for('admin.booktour'))
            return redirect(url_for('admin.booktour'))


@admin.route("/logout")
def adminlogout():
    """ 
    logout account admin
    Remove admin account from session and return function adminlogin
    """
    session.pop('admin', None)
    return redirect(url_for("admin.adminlogin"))
