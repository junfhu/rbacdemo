#!/usr/bin/env python
from flask import Flask,render_template
from tool_portal import app
import os

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.urandom(24)


from tool_portal.views import login
app.register_blueprint(login.bp)
app.add_url_rule("/", endpoint="login.login")

@app.route('/', methods=['GET', 'POST'])
def index():
    print("here")
    return render_template('index.html')
    
app.run(host='0.0.0.0',port=5000,debug=True)
