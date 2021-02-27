from models.Bitcoin import Bitcoin
from models.Day import Day
import sys
import os
import psutil

filepath = "bitcoin_raw.csv"
output_filemath = "bitcoin_clean_python.csv"
str_to_file = ""
thirty_day_buffer = []
FIRST_DATE_TO_PARSE = 1325376000

def data_cleaner_manual():
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    original_stdout = sys.stdout
    p = psutil.Process(os.getpid())
    print(os.getpid())
    print(p.cpu_percent())
    sys.stdout = open(output_filemath, "w")

    with open(filepath) as bitcoin_file:
        header = bitcoin_file.readline().rstrip()
        save_columns_from_header(header)

        first_day = bitcoin_file.readline().rstrip()
        line_list = []
        line_list = first_day.split(",")
        while ("NaN" in line_list or float(line_list[0]) < FIRST_DATE_TO_PARSE):
            first_day = bitcoin_file.readline().rstrip()
            line_list = first_day.split(",")
        first_day = Bitcoin(line_list[0], line_list[-1])
        day = Day(first_day)
        day.add_bitcoin(first_day)
        for row in bitcoin_file:
            row_list = []
            row = row.rstrip()
            row_list = row.split(",")
            if "NaN" in row_list:
                continue
            bitcoin = Bitcoin(row_list[0], row_list[-1])
            if bitcoin.timestamp != day.day:
                day.calculate_average_of_bitcoin()
                returned_day = add_and_retrieve_day(day)
                if(isinstance(returned_day, Day)):
                    if returned_day.average_price <= day.average_price:
                        returned_day.label = 1.0
                    else:
                        returned_day.label = 0.0
                if returned_day is not None:
                    print(returned_day)
                day = Day(bitcoin)
            day.add_bitcoin(bitcoin)
        day.calculate_average_of_bitcoin()
        thirty_day_buffer.append(day)
    returned_day = retrieve_day()
    while(isinstance(returned_day, Day)):
        print(returned_day)
        returned_day = retrieve_day()
    sys.stdout = original_stdout

def add_and_retrieve_day(day):
    thirty_one = 31
    if day != None:
        thirty_day_buffer.append(day)
    if len(thirty_day_buffer) == thirty_one:
        return thirty_day_buffer.pop(0)
    return None

def retrieve_day():
    if len(thirty_day_buffer) == 1:
        return None
    return thirty_day_buffer.pop(0)

def save_columns_from_header(first_line):
    first_line_list = first_line.split(",")
    new_line_list = [first_line_list[0]]
    new_line_list.append(first_line_list[-1])
    new_line_list.append("labels")
    print(', '.join(new_line_list))
