'''
logger test
ref:
https://stackoverflow.com/questions/1383254/logging-streamhandler-and-standard-streams

Created on 2018年2月26日
@author: rocky.wang
'''
import datetime, logging, sys

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-10s %(levelname)-6s %(message)s',
                handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(datetime.datetime.now().strftime("tk%Y-%m-%d.log"), encoding='utf-8')])
    logger = logging.getLogger(__name__)
    
    logger.debug("Hello debug 中文")
    logger.info("Hello info")
    logger.warning("Hello warning")
#     logger.error("Hello error")
#     logger.critical("Hello critical")
    
