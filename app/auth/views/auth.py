import functools
from flask import render_template, Blueprint, redirect, url_for,request,session,flash,g
from werkzeug.security import  check_password_hash ,generate_password_hash
from ..models import User
from RealProject import  db
bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates', static_folder='../static')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       redirect_to=request.args.get('redirect_to')
       error = None
       user =  User.query.filter_by(username=username).first()
       if user is None:
           error = '该用户不存在！'
       elif not check_password_hash(user.password, password):
           error = '密码不正确.'
       if error is None:
           session.clear()
           session['user_id'] = user.id
           if redirect_to is not  None:
               return redirect(redirect_to)
           return redirect(url_for('admin.index'))
       flash(error)
    return render_template('login.html')
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        if password != password1:
            flash('两次密码输入不一致！')
            return redirect(url_for('auth.register'))
        exists_user = User.query.filter_by(username=username).first()
        if exists_user:
            flash('该用户名已经存在，请更换其他用户名！')
            return redirect(url_for('auth.register'))
        else:
            user = User(username=username, password=generate_password_hash(password1))
            db.session.add(user)
            db.session.commit()
            session.clear()
            session['user_id'] = user.id
        return redirect(url_for('admin.index'))
    return render_template('register.html')
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
@bp.before_app_request
def load_logged_in_user():
    urls = ['/auth/']
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(int(user_id))
        if g.user.is_super_user and g.user.is_active:
            g.user.has_perm = 1
        elif not g.user.is_super_user and g.user.is_active and not g.user.is_staff and request.path in urls:
            g.user.has_perm = 1
        else:
            g.user.has_perm = 0
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            redirect_to=f"{url_for('auth.login')}?redirect_to={request.path}"
            return redirect(redirect_to)
        if g.user.has_perm:
            pass
        else:
            return '<h1>无权限查看！</h1>'
        return view(**kwargs)
    return wrapped_view

@bp.route('/')
@login_required
def userinfo():
    # 用户中心
    return render_template('userinfo.html')