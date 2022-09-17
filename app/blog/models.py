from datetime import  datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from RealProject import db
from enum import IntEnum
class BaseModel(db.Model):
    __abstract__ = True
    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, ) # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # 更新时间

class Category(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)
    post=db.relationship('Post',back_populates='category',cascade="all,delete",passive_deletes=True) # 2022.9.18 增加 #级联删除
    def __repr__(self):
        return '<Category %r>' % self.name

class PostPublishType(IntEnum):
    draft = 1
    show = 2 
    tags = db.Table('tags',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
        db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
    )
class Post(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    has_type = db.Column(db.Enum(PostPublishType), server_default='show', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id',ondelete="CASCADE"), nullable=False) ##2022.9.18  增加 ondelete="CASCADE"  #级联删除
    content = db.Column(LONGTEXT, nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('post', lazy=True))
    category=db.relationship("Category",back_populates="post")  #2022.9.18 增加  #级联删除
    def __repr__(self):
        return f'<Post {self.title}>'
class Tag(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    def __repr__(self):
        return f'<Tag {self.name}>'