from data_cleaner_manual import data_cleaner_manual
from log_reg import log_reg
import timeit

def main():
	start_time = timeit.default_timer()
	data_cleaner_manual()
	log_reg()
	end_time = timeit.default_timer()
	print("runtime = {}".format(end_time-start_time))
	return

if __name__ == '__main__':
	main()
