# from crypt import methods
from flask import Flask, request, render_template, url_for, redirect,Blueprint
import pandas as pd
from database.db import mysql
vis=Blueprint("vis",__name__)

@vis.route("/vis")
def line_chart():
    if request.method=='GET':
        cur = mysql.get_db().cursor()
        cur.execute("select Order_Date, Price from order_tour")
        data_order=cur.fetchall()
        # print(data_order)
        # # date=data_order[:][0].split()
        # date={}
        # for i in data_order:
        #     d=(i[0])
        #     d=(d.strftime("%Y/%d/%m"))
        #     if d in date:
        #         date[d]+=i[1]
        #     else: date[d]=i[1]
        # end=sorted(date.items())
        # print(end)
        # print(type(date))
        return render_template("statistical.html",data_order)
    # for i in range(len(data_order)):
