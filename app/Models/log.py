from datetime import datetime
import sqlalchemy as sa
from Config.db import db
from Config import BotConfig
import os
import psutil
import socket
from datetime import date
from sqlalchemy import cast,Date,desc
from SqlUts import tblUts
import platform
from dateUts import now

if not "Windows" in platform.platform():
    import pwd


class Log(db.base,tblUts(db)):
    __tablename__ = 'tbs_logs'
    __table_args__ = {"schema": 'python'}

    id_proc           = sa.Column(sa.Integer)
    datetime          = sa.Column(sa.DateTime,nullable=False)
    botname           = sa.Column(sa.String(100),nullable=False)
    level             = sa.Column(sa.String(50),nullable=False)
    function          = sa.Column(sa.String(100))
    message           = sa.Column(sa.TEXT)
    file              = sa.Column(sa.String(100))
    path              = sa.Column(sa.String(100))
    module            = sa.Column(sa.String(100))
    line              = sa.Column(sa.Integer)
    hostname          = sa.Column(sa.String(100),nullable=False)
    user_pc           = sa.Column(sa.String(255),nullable=False)
    ram               = sa.Column(sa.Float,nullable=False)
    ram_available     = sa.Column(sa.Float,nullable=False)
    cpu_usage_percent = sa.Column(sa.Float,nullable=False)


    def __init__(self,level,date=None,function=None,file=None,module=None,path=None,line=None,message=None):
        self.user_pc           = os.getlogin() if "Windows" in platform.platform() else pwd.getpwuid(os.getuid())[0]
        self.cpu_usage_percent = psutil.cpu_percent()
        self.ram               = round(psutil.virtual_memory().total/1000000000, 0)
        self.ram_available     = round(psutil.virtual_memory().available/1000000000, 0)
        self.hostname          = socket.gethostname()
        self.datetime          = now().date if not date else date
        self.function         = function
        self.level             = level
        self.message           = message
        self.file              = file
        self.module            = module
        self.path              = path
        self.line              = line
        self.botname           = BotConfig.NAME
        self.id_proc           = self.get_id_proc()
        
    def get_id_proc(self):
        if self.level == 'DEBUG': return None
        if not "ID_PROC" in dir(BotConfig):
            BotConfig.ID_PROC = None
        if BotConfig.ID_PROC or BotConfig.ID_PROC == 0:
            return BotConfig.ID_PROC
        
        # lg = Log.query.filter(cast(Log.datetime,Date) == date.today(),Log.hostname == self.hostname,Log.user_pc == self.user_pc,Log.botname == BOTNAME).order_by(desc(Log.id_proc)).first()
        lg = Log.query.filter(cast(Log.datetime,Date) == date.today(),Log.botname == BotConfig.NAME).filter(Log.id_proc != None).order_by(desc(Log.id_proc)).first()
        if not lg or lg.id_proc is None:
            BotConfig.ID_PROC = 0
        else:
            BotConfig.ID_PROC = lg.id_proc+1
        return BotConfig.ID_PROC

#Log.init()
#a  =1
# if not db.engine.dialect.has_table(db.engine.connect(),Log.__tablename__):
#     db.create_all()
    

    
