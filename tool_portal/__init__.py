#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy







def create_app():
    app = Flask(__name__)
    return app

app=create_app()

