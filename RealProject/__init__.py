# -*- coding: UTF-8 -*-
import os

from RealProject.settings import BASE_DIR
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db=SQLAlchemy()
migrate=Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'     
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        app.config.from_mapping(test_config)
    db.init_app(app)  
    migrate.init_app(app, db) 
    from app.blog import views as blog
    app.register_blueprint(blog.bp)

    from app.auth import views as auth
    app.register_blueprint(auth.bp)

    from app.admin import  views as admin

    app.register_blueprint(admin.bp)

    from app.blog import models
    from app.auth import models
    from app.admin import models

   
    app.context_processor(inject_category)

    from app.util.utils import init_script
    init_script(app)
    app.add_url_rule('/', endpoint='index',view_func=blog.index)

    return app



def inject_category():
    from app.blog.models import Category
    categorys = Category.query.limit(6).all()  #获取六条数据
    return dict(categorys=categorys)