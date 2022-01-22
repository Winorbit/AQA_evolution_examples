import sys

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

called_from = sys.modules['__main__'].__file__
if "unittest" in called_from or "pytest" in called_from:
    from .settings import DB_PATH
else:
    from settings import DB_PATH

DeclarativeBase = declarative_base()
engine = create_engine(DB_PATH)  

class User(DeclarativeBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column('username', String)
    email = Column('email', String)
    password = Column('password', String)

    def __repr__(self):
        return "".format(self.username)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {'id': self.id,
               'username': self.username,
               'email': self.email,
               'password': self.password,}

class Post(DeclarativeBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column('name', String)
    text = Column('email', String)
    author_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return self.title

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {'id': self.id,
               'title': self.title,
               'text': self.text,
               'author_id': self.author_id,}
