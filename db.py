from sqlalchemy import Column, String, INT, DATETIME, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

Base = declarative_base()


class Dbzf(Base):
    __tablename__ = 'tb_dbzf'
    id = Column(INT, primary_key=True)
    city = Column(String)
    area = Column(String)
    article_id = Column(INT)
    url = Column(String)
    title = Column(String)
    author_url = Column(String)
    publish_time = Column(DATETIME)
    create_time = Column(DATETIME)


class Dict(Base):
    __tablename__ = 'tb_dict'
    id = Column(INT, primary_key=True)
    code = Column(String)
    value = Column(String)
    remark = Column(String)
    sort = Column(INT)
    type = Column(String)
    status = Column(INT)
    create_time = Column(DATETIME)
    creator_id = Column(String)
    creator_name = Column(String)
    update_time = Column(DATETIME)
    updater_id = Column(String)
    updater_name = Column(String)


user = config.db('user')
password = config.db('password')
url = config.db('url')
name = config.db('name')
max_overflow = int(config.db('max_overflow'))
db = 'mysql+pymysql://' + user + ':' + password + '@' + url + '/' + name
engine = create_engine(db, max_overflow=max_overflow)
DBSession = sessionmaker(bind=engine)




