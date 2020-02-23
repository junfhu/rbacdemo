import functools
from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from tool_portal.model import USERS
from tool_portal.model import ROLES
from tool_portal.model import ROLEMAPPINGS
from tool_portal.model import MENUS
from tool_portal.model import dbusers
from datetime import datetime
import hashlib




def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("username") == None:
            return redirect(url_for('login.login'))

        return view(**kwargs)

    return wrapped_view#

bp = Blueprint("login", __name__, url_prefix="/login", template_folder='templates', static_folder='static')




@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        username = request.form['username']
        password = hashlib.sha224(request.form['password'].encode()).hexdigest()

        user_info = USERS.query.filter_by(username=username,password=password).all()

        if len(user_info)==0:
            return render_template('login/login.html')     
        else:
            userrole = user_info[0].userrole


        session['username']=username
        session['userrole']=userrole

        return redirect(url_for('login.success'))
    return render_template('login/login.html')     
    


@bp.route('/success')
@login_required
def success():
    roleid=session['userrole']
    all_menus = MENUS.query.order_by(MENUS.menuorder).all()
    menus=[]
    for menu in all_menus:
        menu_detail=[menu.menuid,menu.menuname,menu.parentmenu]
        menus.append(menu_detail)
    session['menus']=menus
    mappings = ROLEMAPPINGS.query.filter_by(roleid=roleid).all()
    mapping_menus=[]
    for mapping in mappings:
        mapping_menus.append(mapping.menuid)
    session['mapping_menus']=mapping_menus
    return render_template('index.html')




@bp.route('/logout')
def logout():
    session['username']=False
    return redirect(url_for('login.login'))


@bp.route('/usermanagement',methods=['GET', 'POST'])
@login_required
def usermanagement():
    if request.method=="POST":
        userid=request.form['userid']
        userrole=request.form['userrole']
        userinfo=USERS.query.filter_by(userid=userid)
        userinfo[0].userrole=userrole
        dbusers.session.commit()
    users=USERS.query.all()
    userroles=ROLES.query.all()
    return render_template('login/user_management.html',users=users,userroles=userroles)

@bp.route('/rolemanagement',methods=['GET', 'POST'])
@login_required
def rolemanagement():
    roles=ROLES.query.all()
    return render_template('login/role_management.html',roles=roles)


@bp.route('/add_new_role/', methods=['GET', 'POST'])
@login_required
def add_new_role():
    if request.method == 'GET':
        menus = MENUS.query.order_by(MENUS.menuorder).all()
        return render_template('/login/role_add.html',menus=menus)

@bp.route('/role_add/', methods=['GET', 'POST'])
@login_required
def role_add():
    if request.method == 'POST':
        rolename = request.form['rolename']
        rolemenuidlist = request.form.getlist('rolemenu')
        rolemenuidlist = [int(i) for i in rolemenuidlist]
        newrole=ROLES(rolename=rolename)
        dbusers.session.add(newrole)
        dbusers.session.commit()
        newroleid=ROLES.query.filter_by(rolename=rolename).first().role_id
        for rolemenuid in rolemenuidlist:
            new_role_mapping = ROLEMAPPINGS(roleid=newroleid, menuid=rolemenuid)
            dbusers.session.add(new_role_mapping)
            dbusers.session.commit()
        return redirect(url_for('login.rolemanagement'))

@bp.route('/edit_role/', methods=['GET', 'POST'])
@login_required
def edit_role():
    if request.method == 'GET':
        menus = MENUS.query.order_by(MENUS.menuorder).all()
        roleid=request.args['roleid']
        roleinfo=ROLES.query.filter_by(roleid=roleid).first()
        mappings=ROLEMAPPINGS.query.filter_by(roleid=roleid).all()
        return render_template('/login/role_edit.html',menus=menus,roleinfo=roleinfo,mappings=mappings)

@bp.route('/role_edit/', methods=['GET', 'POST'])
@login_required
def role_edit():
    if request.method == 'POST':
        roleid = request.form['roleid']
        rolemenuidlist = request.form.getlist('rolemenu')
        rolemenuidlist = [int(i) for i in rolemenuidlist]
        #Remove the existing menus
        existingmenus = ROLEMAPPINGS.query.filter_by(roleid=roleid).all()
        for existingmenu in existingmenus:
            dbusers.session.delete(existingmenu)
            dbusers.session.commit()
        #Add new menus
        for rolemenuid in rolemenuidlist:
            new_role_mapping = ROLEMAPPINGS(roleid=roleid, menuid=rolemenuid)
            dbusers.session.add(new_role_mapping)
            dbusers.session.commit()
        return redirect(url_for('login.rolemanagement'))


@bp.route('/add_new_user/', methods=['GET', 'POST'])
@login_required
def add_new_user():
    if request.method == 'GET':
        userroles = ROLES.query.all()
        return render_template('/login/user_add.html',userroles=userroles)
    elif request.method == 'POST':
        username = request.form['username'].lower()
        existing_user=USERS.query.filter_by(username=username).first()
        if existing_user:
            flash ("User already exist")
            userroles = ROLES.query.all()
            return render_template('/login/user_add.html', userroles=userroles)
        else:
            password = hashlib.sha224(request.form['password'].encode()).hexdigest()
            userrole = request.form['userrole']

            new_user=USERS(username=username,password=password,userrole=userrole)
            dbusers.session.add(new_user)
            dbusers.session.commit()

            return redirect(url_for('login.usermanagement'))

#Delete User
@bp.route('/delete_user/', methods=['GET', 'POST'])
@login_required
def delete_user():
    if request.method == 'GET':
        userid = request.args['userid']
        user = USERS.query.filter_by(userid=userid).first()
        dbusers.session.delete(user)
        dbusers.session.commit()
        return redirect(url_for('login.usermanagement'))



@bp.route('/passwordmanagement',methods=['GET', 'POST'])
@login_required
def passwordmanagement():
    if request.method == 'POST':
        password = hashlib.sha224(request.form['password'].encode()).hexdigest()
        userinfo=USERS.query.filter_by(username=session['username']).first()
        userinfo.password=password
        dbusers.session.commit()
        flash("Password Updated")
        return redirect(url_for('login.passwordmanagement'))

    return render_template('login/change_password.html')