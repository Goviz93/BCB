
import csv
import pandas as pd
from pathlib import Path
from copy import deepcopy




class spreadSheet:
    spreadsheets = []

    def __int__(self, file_path):
        self.file_path = Path(file_path)
        spreadSheet.spreadsheets.append(self)


    def UpdateFilePath(self, new_path):
        self.file_path = Path(new_path)

    def getFile_Path(self):
        return self.file_path

    def Read(self):
        pass

    def Write(self, data):
        pass


class CSV(spreadSheet):

    def __init__(self, file_path):
        super().__int__(file_path)

    def Read(self, filename='read_file'):
        with open(self.file_path, 'r') as file:
            _data = csv.DictReader(file)
            data = list(_data)
            return data

    def Write(self, data):
        fieldnames = data[0].keys()
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


class Excel(spreadSheet):

    def __init__(self, file_path):
        super().__int__(file_path)

    def Read(self, filename='read_file', sheet_name=None):
        dataframe = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return dataframe

    def Read_csv(self, sheet_name=None):
        dataframe = pd.read_csv(self.file_path)
        return dataframe

    def Write(self, data, sheet_name=None, override=False):
        if sheet_name is None:
            print("Provide a sheet name")
        else:
            _override = override ^ False
            data.to_excel(self.file_path, sheet_name=sheet_name, index=_override)


class SpreadSheet_Factory:

    @staticmethod
    def get_spreadsheet(condition, file_path):
        if condition == "csv":
            return CSV(file_path)
        elif condition == "excel":
            return Excel(file_path)


#Only to handle dataframes using excel.
class DataFrame_Handler():

    def __int__(self):
        pass

    def create_sheets(self, file_path):
        return SpreadSheet_Factory.get_spreadsheet('excel', file_path)

    def get_child_dataframe(self, dataframe, headers: list):
        return dataframe[headers]

    def filter_dedup_columns(self, dataframe, header: str):
        return dataframe[~dataframe[header].duplicated()]

    def filter_column_values(self, dataframe, column, value: str, is_regex=False):
        return dataframe[dataframe[column].str.contains(value, regex=is_regex)]

    def concat_dataframes(self, dataframe_1, dataframe_2):
        return pd.concat([dataframe_1, dataframe_2], ignore_index=True)

    def copy_dataframe(self, dataframe):
        return deepcopy(dataframe)

    def get_row(self, dataframe, index):
        return dataframe.iloc[[index]]

    def get_column(self, dataframe, column):
        return dataframe[column]

    def create_mask(self, dataframe, column_name: str, regex: str):
        return dataframe[column_name].str.contains(regex)



