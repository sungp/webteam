import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)

    def do_serialize(self, posts=[]):
        return {
            'id': self.id,
            'name': self.name,
            'Post': [post.serialize for post in posts]
        }

    serialize = property(do_serialize)


class Post(Base):
    __tablename__ = 'post'

    subject = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    content = Column(String(10000))
    group_name = Column(Integer, ForeignKey('group.name'))
    group = relationship(Group)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    date_added = Column(DateTime)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'group_name': self.group_name,
            'content': self.content,
            'id': self.id,
            'subject': self.subject,
        }


engine = create_engine('sqlite:///grouppost.db')


Base.metadata.create_all(engine)
