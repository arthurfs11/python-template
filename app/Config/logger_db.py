from Config.settings import ini
from Config.loguru import logger
from Models.log import Log
from datetime import datetime as dt
from dateUts import fmtDate
import json

def handler_db(data):
    if not ini.in_prd: return
    data2 = json.loads(data)["record"]
    extra = data2["extra"]
    args = {
        "date"    : fmtDate(dt.strptime(data2["time"]["repr"],"%Y-%m-%d %H:%M:%S.%f%z"),fmt="sql+hr"),
        "function": extra["func_name"] or data2["function"],
        "level"   : data2["level"]["name"],
        "file"    : extra["file_name"] or data2["file"]["name"],
        "module"  : data2["module"],
        "path"    : data2["name"],
        "line"    : extra["line_exec"] or data2["line"],
        "message" : data2["message"]
    }
    Log(**args).save()


logger.add(
    handler_db,
    serialize=True
    )
