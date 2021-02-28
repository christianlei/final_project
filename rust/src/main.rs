use std::time::Instant;

mod log_reg;
mod data_cleaner_manual;

fn main(){
	let start = Instant::now();
	let mut _ret = data_cleaner_manual::clean_data_file();
	_ret = log_reg::log_reg();
	let duration = start.elapsed();
	println!("runtime = {:?}", duration);
	return;
}
