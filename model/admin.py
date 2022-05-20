from database.db import mysql
from flask import Flask, render_template, url_for, redirect, request, Blueprint
admin=Blueprint('admin',__name__)
@admin.route("/admin")
@admin.route("/",methods=['GET','POST'])
def adminuser():
    cur=mysql.get_db().cursor()
    cur.execute("select U_id,Name_user,Address_User,Number_Phone_User from user_1")
    user=cur.fetchall()
    # history=None
    if request.method=="POST":
        user_id=request.form["U_id"]
        if user_id is not None:
            cur.execute(f'select U_id,Name_Tour, Order_Date,Amount_of_people, order_tour.Price from order_tour inner join ttour.orderdetail on order_tour.O_id=orderdetail.OD_id inner join ttour.tour on orderdetail.OD_id=order_tour.O_id where order_tour.U_id={user_id}')
            history=cur.fetchall()
            return render_template("adminUser.html",user=user,history=history)
        print(user_id)
    cur.close()
    return render_template("adminUser.html", user=user)
@admin.route("/<id>")
def history_tour_user(id):
    user_id=id
    cur=mysql.get_db().cursor()
    cur.execute(f'select U_id,Name_Tour, Order_Date,Amount_of_people, order_tour.Price from order_tour inner join ttour.orderdetail on order_tour.O_id=orderdetail.OD_id inner join ttour.tour on orderdetail.OD_id=order_tour.O_id where order_tour.U_id={user_id}')
    history=cur.fetchall()
    cur.close()
    return render_template("adminUser.html",history=history)
