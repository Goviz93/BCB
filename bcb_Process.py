
from scripts.bcb_Bot import BOT
from scripts.spreadSheets import customers_data
from scripts.getTime_API import validate_date_with_worldtimeapi


def validateLicense(date):
    return validate_date_with_worldtimeapi(date)

def my_function():
    try:
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

    if validate_date_with_worldtimeapi('2023-11-14'):
        my_function()