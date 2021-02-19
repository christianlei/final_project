from models.Bitcoin import Bitcoin
from models.Day import Day
import sys
import os
import datetime


filepath = "bitcoin_raw.csv"
output_filemath = "bitcoin_clean_python.csv"
str_to_file = ""
thirty_day_buffer = []

def main():
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    sys.stdout = open(output_filemath, "w")

    with open(filepath) as bitcoin_file:
        header = bitcoin_file.readline().rstrip()
        save_columns_from_header(header)

        first_day = bitcoin_file.readline().rstrip()
        line_list = []
        line_list = first_day.split(",")
        first_day = Bitcoin(line_list[0], line_list[-1])
        day = Day(first_day)
        for row in bitcoin_file:
            row_list = []
            row = row.rstrip()
            row_list = row.split(",")
            if "NaN" in row_list:
                continue
            bitcoin = Bitcoin(row_list[0], row_list[-1])
            if bitcoin.timestamp != day.day:
                returned_day = add_and_retrieve_day(day)
                day.calcuate_average_of_bitcoin()
                if(isinstance(returned_day, Day)):
                    if returned_day.average_price > day.average_price:
                        day.label = 1.0
                    else:
                        day.label = 0.0
                print(day)
                day = Day(bitcoin)

            day.add_bitcoin(bitcoin)
def add_and_retrieve_day(day):
    THIRTY = 30
    thirty_day_buffer.append(day)
    if len(thirty_day_buffer) == THIRTY:
        return thirty_day_buffer.pop(0)

def save_columns_from_header(first_line):
    first_line_list = first_line.split(",")
    new_line_list = first_line_list[0:1]
    new_line_list.append(first_line_list[-1])
    new_line_list.append("label")
    print(', '.join(new_line_list))

if __name__ == "__main__":
    main()
