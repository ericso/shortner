from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    ForeignKey
    )

import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


# class MyModel(Base):
#     __tablename__ = 'models'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)

# Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Url(Base):
    """ The SQLAlchemy declarative model class for a Url object. """
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    url_link = Column(Text)
    url_short = Column(Text)
    time_created = Column(DateTime)

    def __init__(self, url_link, url_short, time_created=datetime.datetime.now()):
        self.url_link = url_link
        self.url_short = url_short
        self.time_created = time_created
    
    def __repr__(self):
        return "<Url('%s', '%s', '%s')>" % (self.url_link, self.url_short, self.time_created)
        pass

class Hit(Base):
    """ The SQLAlchemy declarative model class for a Hits object. """
    __tablename__ = 'hits'
    id = Column(Integer, primary_key=True)
    ip = Column(Text)
    referer = Column(Text)
    url_id = Column(Integer, ForeignKey('urls.id'))
    time_visited = Column(DateTime)

    def __init__(self, ip, referer, url_id, time_visited=datetime.datetime.now()):
        self.ip = ip
        self.referer = referer
        self.url_id = url_id
        self.time_visited = time_visited

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s')>" % (self.ip, self.referer, self.url_id, self.time_visited)
        pass
