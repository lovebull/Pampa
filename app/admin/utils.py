import os
import  uuid
from werkzeug.utils import secure_filename
from RealProject.settings import  BASE_DIR


def _file_path(directory_name):
    file_path = BASE_DIR / f'uploads/{directory_name}'
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path

def update_filename(f):
    names = list(os.path.splitext(secure_filename(f.filename)))
    names[0] = ''.join(str(uuid.uuid4()).split('-'))
    return ''.join(names)

def upload_file_path(directory_name, f):
    file_path = _file_path(directory_name)
    filename = update_filename(f)
    return file_path / filename, filename