import os
import  uuid
from werkzeug.utils import secure_filename
from RealProject.settings import  BASE_DIR

import click
from flask import Flask
from app.auth.models import User
from werkzeug.security import generate_password_hash
from RealProject import db

def _file_path(directory_name):
    """判断该路径是否存在不存在则创建
    """
    file_path = BASE_DIR / f'uploads/{directory_name}'
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path

def update_filename(f):
    """修改文件名
    """
    names = list(os.path.splitext(secure_filename(f.filename)))
    # print('names===',names)
    names[0] = ''.join(str(uuid.uuid4()).split('-'))
    return ''.join(names)

def upload_file_path(directory_name, f):
    # 构造上传文件路径
    file_path = _file_path(directory_name)
    filename = update_filename(f)
    # print('filename====',filename)
    return file_path / filename, filename


# 在终端命令行中输入  flask createsuperuser
def init_script(app:Flask):
    #创建超级管理员命令
    @app.cli.command()
    @click.option("--username",prompt=True,help="请输入用户名!")
    @click.option("--password",prompt=True,hide_input=True,confirmation_prompt=True,help="请输入密码!")
    def createsuperuser(username,password):
        click.echo('创建超级管理员')
        user=User(username=username,password=generate_password_hash(password),is_super_user=True)
        db.session.add(user)
        db.session.commit()
        click.echo(f'超级管理员{username}创建成功')
