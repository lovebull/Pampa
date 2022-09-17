from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
SECRET_KEY = 'l%3ya7fn3moipdpcltj(tdfcv5^@lj=t5d&72levvls+y*@_4^'
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/flask_emascm'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True   #  自动提交数据处理
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO=False

import  os
#配置文件
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PAMPA_UPLOAD_PATH = os.path.join(basedir, 'uploads')