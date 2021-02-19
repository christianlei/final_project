from models.Bitcoin import Bitcoin
from models.Day import Day
import sys
import os
import datetime


filepath = "bitcoin_raw.csv"
output_filemath = "bitcoin_clean_python.csv"
str_to_file = ""

def main():
    new_line_list = []
    last_date = None

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
        for line in bitcoin_file:
            #create list of one row, with timestamp as date.
            line = line.rstrip()
            line_list = []
            line_list = line.split(",")
            bitcoin = Bitcoin(line_list[0], line_list[-1])

            if bitcoin.timestamp is not day.day:
                print(new_line_list)
                day = Day(bitcoin)

            if "NaN" in new_line_list:
                continue


def average_weighted_price_of_same_date(line_list):
    unix_to_date = datetime.datetime.fromtimestamp(float(line_list[0]))
    new_line_list = []
    new_line_list = line_list[0:1]
    new_line_list.append(line_list[-1])
    new_line_list[0] = unix_to_date.strftime("%Y-%m-%d")

def save_columns_from_header(first_line):
    first_line_list = first_line.split(",")
    new_line_list = first_line_list[0:1]
    new_line_list.append(first_line_list[-1])
    new_line_list.append("label")
    print(', '.join(new_line_list))



if __name__ == "__main__":
    main()
