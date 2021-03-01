use std::time::Instant;

mod log_reg;
mod data_cleaner_manual;

fn main(){
	let start = Instant::now();
	let mut _ret = data_cleaner_manual::clean_data_file();
	let middle = start.elapsed();
	_ret = log_reg::log_reg();
	let duration = start.elapsed();
	println!("total runtime = {:?}", duration);
	println!("data cleaner runtime = {:?}", middle);
	println!("log_reg runtime = {:?}", duration-middle);
	return;
}
