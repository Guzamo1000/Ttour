
from flask import Flask, redirect,url_for, render_template, Blueprint,request, session,flash
from sqlalchemy import true
from database.db import mysql
from model.admin import admin
from model.user import user
from model.data_visual import vis
from werkzeug.utils import secure_filename
import os
app=Flask(__name__)
app.config["SECRET_KEY"] = "ttour"
app.config["MYSQL_DATABASE_HOST"]='localhost'
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]="258000"
app.config["MYSQL_DATABASE_DB"]='ttour'

app.config['UPLOAD_FOLDER']='/static/uploads'
app.config['MAX_CONTENT_PATH']=16 * 1024 * 1024

mysql.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(vis)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#
if __name__ == "__main__":
    app.run(debug=true)