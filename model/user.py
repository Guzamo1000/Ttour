from database.db import mysql
from flask import Flask, render_template, redirect,url_for,request,Blueprint
user=Blueprint("user",__name__)
