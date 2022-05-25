from fileinput import filename
from flask import Flask, redirect,url_for, render_template, Blueprint
from sqlalchemy import true
from database.db import mysql
from model.admin import admin
from model.user import user
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL


app=Flask(__name__)
app.config["SECRET_KEY"] = "ttour"
app.config["MYSQL_DATABASE_HOST"]='localhost'
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]="250201"
app.config["MYSQL_DATABASE_DB"]='ttour'

mysql.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(user)

if __name__ == "__main__":
    app.run(debug=true)