from db import DBSession, Dict

blacklist = []

def loadBlackList():
    session = DBSession()
    global blacklist
    blacklist = session.query(Dict).filter_by(type='dbzf_blacklist').filter_by(status=1).all()
