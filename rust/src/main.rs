use std::io;
use std::time::Instant;

mod data_cleaner_manual;


fn main() -> io::Result<()> {
    let start = Instant::now();
    let return_file = data_cleaner_manual::clean_data_file();
    let duration = start.elapsed();
    println!("Time elapsed in expensive_function() is: {:?}", duration);
    return_file
}
