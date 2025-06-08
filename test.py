import pandas as pd
from datetime import datetime
import csv

class CSV:
    CSV_FILE = "finance_data.csv"

    @classmethod
    def initialize_file(cls):

        df=pd.read_csv(cls.CSV_FILE)
        print(df.head())

CSV.initialize_file()
