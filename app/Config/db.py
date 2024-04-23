from Config.loguru import logger
from Config import DbConfig
from SqlUts import DbSqlA
import urllib.parse
import sys

PWD = urllib.parse.quote(DbConfig.PWD)

db = DbSqlA(f"postgresql+psycopg2://{DbConfig.USER}:{PWD}@{DbConfig.SERVER}:5432/postgres",fast_executemany=False)

try:
    db.session.connection()
except Exception as e:
    logger.critical(str(e))
    sys.exit()