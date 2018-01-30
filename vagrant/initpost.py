from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import User, Group, Post 

from datetime import datetime

Base = declarative_base()

engine = create_engine('sqlite:///grouppost.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
user1= User(name="gloomy", email="gloomy@paly.edu");
session.add(user1)
session.commit()

user2= User(name="happy", email="happy@paly.edu");
session.add(user2)
session.commit()

user3= User(name="funny", email="funny@paly.edu");
session.add(user3)
session.commit()


design_group = Group(name="design");
session.add(design_group)
session.commit()

art_group = Group(name="art");
session.add(art_group)
session.commit()



post1 = Post(subject="a sad day", 
    content="i'm depressed", 
    group=design_group, user=user1, 
    date_added = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')) 
session.add(post1)
session.commit()

post2 = Post(subject="a happy day", 
    content="i'm happy", 
    group=art_group, 
    user=user2,
    date_added = datetime.strptime('Dec 25 2017  2:00PM', '%b %d %Y %I:%M%p'))
session.add(post2)
session.commit()

post3 = Post(subject="a funny day", 
    content="i'm laughing", 
    group=art_group, 
    user=user2,
    date_added = datetime.strptime('Jan 1 2018  12:01AM', '%b %d %Y %I:%M%p'))
session.add(post3)
session.commit()


print "added posts!"
