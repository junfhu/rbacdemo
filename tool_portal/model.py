from flask_sqlalchemy import SQLAlchemy
from tool_portal import app
import os


USERDBPATH='sqlite:///users.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'userdb':USERDBPATH}
dbusers=SQLAlchemy(app)


class USERS(dbusers.Model):
    __bind_key__ = 'userdb'
    __tablename__ = 'users'
    userid = dbusers.Column(dbusers.Integer, primary_key=True)
    username = dbusers.Column(dbusers.Text, nullable=False)
    userrole = dbusers.Column(dbusers.Integer)
    password=dbusers.Column(dbusers.Text)


class ROLES(dbusers.Model):
    __bind_key__ = 'userdb'
    __tablename__ = 'roles'
    roleid = dbusers.Column(dbusers.Integer, primary_key=True)
    rolename = dbusers.Column(dbusers.Text, nullable=False)

class MENUS(dbusers.Model):
    __bind_key__ = 'userdb'
    __tablename__ = 'menus'
    menuid = dbusers.Column(dbusers.Integer, primary_key=True)
    menuname = dbusers.Column(dbusers.Text, nullable=False)
    parentmenu = dbusers.Column(dbusers.Integer, nullable=False)
    menuorder = dbusers.Column(dbusers.Integer, nullable=False)
    
    
class ROLEMAPPINGS(dbusers.Model):
    __bind_key__ = 'userdb'
    __tablename__ = 'rolemappings'
    mappingid=dbusers.Column(dbusers.Integer,primary_key=True)
    roleid = dbusers.Column(dbusers.Integer,nullable=False)
    menuid = dbusers.Column(dbusers.Integer, nullable=False)

