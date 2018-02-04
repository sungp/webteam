from flask import Flask, render_template, request, redirect, jsonify,\
        url_for, flash
from functools import wraps
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Group, Post 

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///grouppost.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def showLink():
  postsOrdered = session.query(Post).order_by(asc(Post.date_added))
  htmlText = render_template('post.html', posts = postsOrdered)
  return htmlText; 

@app.route('/hello', methods=['GET', 'POST'])
def showHello():
  submitMsg = "";
  
  if request.method == 'POST':
    submitMsg = request.form['message'].strip()
  
  htmlText = render_template('hello.html', request = request, message = submitMsg) 
  print htmlText;
  return htmlText;

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
