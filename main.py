
from flask import Flask, render_template, redirect, request, url_for, Blueprint
from sqlalchemy import true
from database.tourdb import mysql
from model.admin import admin

app=Flask(__name__)

#connect database
app.config["MYSQL_DATABASE_HOST"]='localhost'
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]="258000"
app.config["MYSQL_DATABASE_DB"]='mytour'

mysql.init_app(app)
app.register_blueprint(admin)


if __name__=="__main__":
    app.run(debug=True)