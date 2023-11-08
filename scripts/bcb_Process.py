
from scripts.bcb_Bot import BOT
from scripts.spreadSheets import customers_data


def my_function():
    try:
        customers = customers_data()
        for customer in customers.customer_list:
            bot_customer = BOT(customer)
            bot_customer.workFlow()
    except KeyboardInterrupt:
        print('Process Interrupted')


if __name__ == '__main__':
    print("This code will run only if the script is executed directly.")
    my_function()