
import logging
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from scripts.spreadSheets import customers_data
from scripts.getTime_API import validate_date_with_worldtimeapi

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a TimedRotatingFileHandler
logPath = f"./Logs/{datetime.now().strftime('%Y-%m-%d')}"
file_handler = TimedRotatingFileHandler(logPath, when="midnight", interval=1, backupCount=7)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)






def validateLicense(date):
    return validate_date_with_worldtimeapi(date)

def my_function():
    try:
        from scripts.bcb_Bot import BOT
        customers = customers_data()
        bot_customer = BOT(customers.customer_list[0])
        bot_customer.workFlow()
        """
        for customer in customers.customer_list:
            bot_customer = BOT(customer)
            bot_customer.workFlow()        
        """

    except KeyboardInterrupt:
        print('Process Interrupted')


if __name__ == '__main__':
    codes = { '4u2S84NSAaaNMP': '2023-11-14',
              '5GsieqHkXJPyQD': '2023-12-02',
              'cUf4UJio2Gqmo5': '2023-12-09',
              'PNmKhS7BVyn2FZ': '2023-12-16',
              '7M9RYy3f5X2NQW': '2023-12-23',
              '4ZMo2MQx4BiA9T': '2023-12-30'
              }
    logger.info("--- N E W  C Y C L E ---")
    logger.info("Reading Licence")
    with open("./Licencia.txt", "r") as file:
        Token = file.readline()

    logger.info(f"Licence -> {Token}")

    if Token in codes.keys():
        if validate_date_with_worldtimeapi(codes.get(Token)):
            my_function()
    else:
        logger.info(f"Token Invalido -> {Token}")
        print('Token Invalido')
