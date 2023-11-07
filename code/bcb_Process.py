
from customer_dataclass import Customer
from spreadSheets import DataFrame_Handler

def read_clients():
    _path = r"clientes.xlsx"
    ExcelReader = DataFrame_Handler().create_sheets(_path)
    df_hoja = ExcelReader.Read('Hoja1')
    return  df_hoja.get('Hoja1')

def num_clients(dataframe):
    return dataframe.shape[0]




if __name__ == 'main':

