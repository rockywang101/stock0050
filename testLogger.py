'''
logger test
Created on 2018年2月26日
@author: rocky.wang
'''
import datetime, logging

if __name__ == "__main__":
    
    log_filename = datetime.datetime.now().strftime("tk%Y-%m-%d.log")
    
    # dateformat 為自定義格式，但其實不是很需要
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-10s %(levelname)-6s %(message)s',
                datefmt='%m-%d %H:%M:%S',
                filename=log_filename)
    
    logger = logging.getLogger(__name__)
    
    # 定義 handler 輸出 console
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-8s: %(levelname)-8s %(message)s'))
    logger.addHandler(streamHandler) # 加入 hander 到 root logger
    

    logger.debug("Hello debug 中文")
    logger.info("Hello info")
    logger.warning("Hello warning")
    logger.error("Hello error")
    logger.critical("Hello critical")
