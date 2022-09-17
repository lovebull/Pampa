from  datetime import datetime,timedelta
from RealProject import  db
class BaseModel(db.Model):
    __abstract__=True
    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, ) 
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 

class Banner(BaseModel):
    id=db.Column(db.Integer,primary_key=True)
    img=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(200),nullable=True)
    url=db.Column(db.String(200),nullable=True)
    def __repr__(self)->str:
        return f'{self.id}=>{self.img}'