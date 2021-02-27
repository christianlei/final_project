from data_cleaner_manual import data_cleaner_manual
import timeit
import psutil,os

def main():
    start_time = timeit.default_timer()
    data_cleaner_manual()
    end_time = timeit.default_timer()
    print ("Runtime: ", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()