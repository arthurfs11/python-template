from Config import logger,show_config
from Libs.loguru import logger_start
from Modules.admin import Admin
from Modules.intranet import Intranet
from Config import *


@logger_start
def main():
    admin = Admin()
    intranet = Intranet()

    logger.success("1 - STEP_GOOGLE")
   
    
    logger.success("2 - STEP_EXPORT")




if __name__ ==  "__main__":
    show_config()
    main()



    

    
    


