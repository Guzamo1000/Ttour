from flask import Flask, redirect
from sqlalchemy import true
from database.db import mysql
from model.admin import admin
from model.user import user
app=Flask(__name__)
app.config["SECRET_KEY"] = "ttour"
app.config["MYSQL_DATABASE_HOST"]='localhost'
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]="258000"
app.config["MYSQL_DATABASE_DB"]='ttour'

mysql.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(user)



# @app.route('/')
# def default():
#     return 'hello'

if __name__ == "__main__":
    app.run(debug=true)