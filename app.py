import flask
from flask import Flask, request, session, redirect, flash, json, \
    render_template, abort, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from hashlib import sha256 
import bcrypt
from functools import wraps
import sys

application = flask.Flask(__name__)
application.config.from_pyfile('app.cfg')
db = SQLAlchemy(application)

@application.route('/', methods=['GET'])
def index_page():
	return "Hello World!"


@application.route('/login', methods=['GET'])
def login_page():
	return render_template('login.html', error="Invalid Credentials")


@application.route('/handler/login', methods=['POST'])
def login_handler():
	query = '''
		SELECT salt, password
		FROM users
		WHERE username=:username
	'''
	try:
		result = db.session.execute(query, {
			'username': request.form['username']
		}).first()
		if result:
			salt, password = result
			if(bcrypt.hashpw(request.form['password'], salt) == password):
				session['auth'] = username
				return redirect(url_for('index_page'))
			else: ## Password is incorrect
				flash("Invalid Credentials")
				return redirect(url_for('login_page'))
		else: ## User does not exist
			flash("Invalid Credentials")
			return redirect(url_for('login_page'))
	except:
		print sys.exc_info()
		return '-1'

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)