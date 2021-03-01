from data_cleaner_manual import data_cleaner_manual
from log_reg import log_reg
import timeit

def main():
	start_time = timeit.default_timer()
	data_cleaner_manual()
	middle_time = timeit.default_timer()
	log_reg()
	end_time = timeit.default_timer()
	print("total runtime = {}".format(end_time-start_time))
	print("data cleaner runtime = {}".format(middle_time-start_time))
	print("log reg runtime = {}".format(end_time-middle_time))
	return

if __name__ == '__main__':
	main()
