use std::time::Instant;

mod log_reg;
mod data_cleaner_manual;

fn main(){
	let start = Instant::now();
	let mut _ret = data_cleaner_manual::clean_data_file();
	let intermediate = start.elapsed();
	let mid = Instant::now();
	_ret = log_reg::log_reg();
	let duration = start.elapsed();
	let log_reg_duration = mid.elapsed();
	println!("total runtime = {:?}", duration);
	println!("data cleaner runtime = {:?}", intermediate);
	println!("log reg runtime = {:?}", log_reg_duration);
	return;
}
