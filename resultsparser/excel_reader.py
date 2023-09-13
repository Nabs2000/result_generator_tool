import pandas as pd
import argparse

class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self):
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(self.file_path)
            return df
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
            return None

# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument("-f", "--filename")
    excel_reader = ExcelReader(parser.filename)
    data_frame = excel_reader.read_excel()

    if data_frame is not None:
        print(data_frame)
