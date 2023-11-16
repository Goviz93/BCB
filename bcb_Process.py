
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
    codes = { '4u2S84NSAaaNMP': '2023-11-14',
              '5GsieqHkXJPyQD': '2023-12-02',
              'cUf4UJio2Gqmo5': '2023-12-09',
              'PNmKhS7BVyn2FZ': '2023-12-16',
              '7M9RYy3f5X2NQW': '2023-12-23',
              '4ZMo2MQx4BiA9T': '2023-12-30'
              }
    Token = input('Ingrese Token: ')

    if Token in codes.keys():
        if validate_date_with_worldtimeapi(codes.get(Token)):
            my_function()
    else:
        print('Token Invalido')
