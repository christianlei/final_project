use std::io;

mod data_cleaner_manual;


fn main() -> io::Result<()> {
    data_cleaner_manual::clean_data_file()
}
