from sqlalchemy import Column, String, INT, DATETIME, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RentingHouse(Base):
    __tablename__ = 'tb_rentinghouse'
    id = Column(INT, primary_key=True)
    city = Column(String(20))
    area = Column(String(20))
    article_id = Column(INT)
    url = Column(String(255))
    title = Column(String(255))
    author_url = Column(String(255))
    publish_time = Column(DATETIME)
    create_time = Column(DATETIME)


engine = create_engine('mysql+pymysql://root:123456@localhost:3306/myspider', encoding='utf-8')
DBSession = sessionmaker(bind=engine)




