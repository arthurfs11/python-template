import sys
import os
from functools import wraps
from Config.loguru import logger
from Config import BotConfig
import Config as cf


def replace_chars(text):
    chars = ["{","}"]
    for ch in chars:
        text = text.replace(ch, ch*2)
    return text

def logger_start(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            logger.success("START",func_name = function.__name__)
            logger_manager(function)(*args, **kwargs)

            fnc = logger.error if cf.loguru.HAS_ERROR else (logger.warning if cf.loguru.HAS_WARNING else logger.success)
            fnc("FINISHED",func_name = function.__name__)
        except ValueError: logger.error("FINISHED",func_name = function.__name__)
        except Exception : logger.critical("FINISHED",func_name = function.__name__)
        BotConfig.ID_PROC = None
        cf.loguru.HAS_ERROR  =None
        cf.loguru.HAS_WARNING = None
    return wrapper

def logger_manager(function,raise_value_error=False):
    file_name = os.path.basename(function.__code__.co_filename)
    params = lambda : {"line_exec":sys.exc_info()[2].tb_next.tb_lineno if sys.exc_info()[2].tb_next else None,"func_name":function.__name__,"file_name":file_name}

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
           return function(*args, **kwargs)
        except ValueError as e:
            logger.error(replace_chars(str(e)),**params())
            if raise_value_error:raise
        except Exception as e:
            logger.critical(replace_chars(str(e)),**params())
            raise
    return wrapper

def logger_class(raise_value_error=False):
    def wraps(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, logger_manager(getattr(cls, attr),raise_value_error=raise_value_error))
        return cls
    return wraps


