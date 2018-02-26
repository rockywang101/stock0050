'''
logger test
Created on 2018年2月26日
@author: rocky.wang
'''
import datetime, logging

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-10s %(levelname)-6s %(message)s',
                handlers=[logging.StreamHandler(), logging.FileHandler(datetime.datetime.now().strftime("tk%Y-%m-%d.log"), encoding='utf-8')])
    logger = logging.getLogger(__name__)
    
    logger.debug("Hello debug 中文")
    logger.info("Hello info")
    logger.warning("Hello warning")
#     logger.error("Hello error")
#     logger.critical("Hello critical")
    
