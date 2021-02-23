extern crate chrono;

use chrono::prelude::*;
use std::fs::{OpenOptions, File};
use std::io::{self, prelude::*, BufReader};
use std::str::FromStr;
use std::collections::VecDeque;

#[derive(Debug, Clone)]
struct Bitcoin {
    timestamp: String,
    weighted_price: f64,
}

impl Bitcoin {
    fn new(timestamp: String, weighted_price: String) -> Bitcoin {
        let timestamp_string = timestamp.parse::<i64>().unwrap();
        let naive = NaiveDateTime::from_timestamp(timestamp_string, 0);
        let datetime: DateTime<Utc> = DateTime::from_utc(naive, Utc);
        let timestamp = datetime.format("%Y-%m-%d").to_string();
        let weighted_price = f64::from_str(&weighted_price).unwrap();
        Bitcoin { timestamp, weighted_price }
    }
}

#[derive(Debug, Clone)]
struct Day {
    timestamp: String,
    average_price: f64,
    bitcoins: Vec<Bitcoin>,
    label: f64,
    number_of_bitcoin: i16,
}

impl Day {
    fn new(timestamp: &String) -> Day {
        let timestamp = timestamp.to_owned();
        let average_price = 0.0;
        let bitcoins: Vec<Bitcoin> = Vec::new();
        let label = -1.0;
        let number_of_bitcoin = 0;
        Day { timestamp, average_price, bitcoins, label, number_of_bitcoin }
    }

    fn add_bitcoin(&mut self, bitcoin: Bitcoin) -> () {
        self.bitcoins.push(bitcoin);
        self.number_of_bitcoin = self.bitcoins.len() as i16;
    }

    fn calculate_average_bitcoin_price(&mut self) -> () {
        let mut sum = 0.0;
        for bitcoin in self.bitcoins.clone() {
            sum += bitcoin.weighted_price;
        }
        self.average_price = sum / self.number_of_bitcoin as f64;
    }

    fn to_string(&self) -> String {
        let mut output_line: String = "".to_owned();
        output_line.push_str(&self.timestamp);
        output_line.push_str(",");
        output_line.push_str(&self.average_price.to_string());
        output_line.push_str(",");
        if self.label != -1.0 {
            output_line.push_str(&self.label.to_string());
        }
        output_line.push_str("\n");
        output_line
    }
}

pub(crate) fn clean_data_file() -> io::Result<()> {
    let input_file_name = "bitcoin_raw.csv";
    let output_file_name = "bitcoin_clean_rust.csv";
    let mut parse_header: bool = false;
    let mut first_day = false;
    let mut row_vector: Vec<String> = Vec::new();
    let split_by = ',';
    let first_date_to_parse = 1325376000;
    let mut skip_line: bool = false;
    let mut thirty_day_buffer: VecDeque<Day> = VecDeque::new();

    let mut output_file = OpenOptions::new()
        .write(true)
        .open(output_file_name)
        .unwrap();
    let file = File::open(input_file_name)?;
    let reader = BufReader::new(file);
    let mut day: Day = Day {
        timestamp: "".to_string(),
        average_price: 0.0,
        bitcoins: vec![],
        label: 0.0,
        number_of_bitcoin: 0,
    };


    for line in reader.lines() {
        let mut file_line: String = "".to_owned();
        //header
        if !parse_header {
            for s in line?.split(split_by) {
                let column = s.to_owned();
                row_vector.push(column);
            }
            file_line.push_str(&row_vector[0]);
            file_line.push(',');
            file_line.push_str(&row_vector[7]);
            file_line.push_str(",label\n");
            write!(&mut output_file, "{}", file_line)?;
            parse_header = true;
            row_vector.clear();
            continue;
        }
        //first day
        if !first_day {
            for s in line?.split(split_by) {
                let column = s.to_owned();
                if column == "NaN" {
                    skip_line = true;
                }
                row_vector.push(column);
            }
            let timestamp = row_vector.get(0).unwrap().parse::<i64>().unwrap();
            if timestamp < first_date_to_parse {
                skip_line = true;
            }
            if skip_line {
                row_vector.clear();
                skip_line = false;
                continue;
            }
            let bitcoin = Bitcoin::new(row_vector.remove(0), row_vector.remove(6));
            day = Day::new(&bitcoin.timestamp);
            day.add_bitcoin(bitcoin);
            row_vector.clear();
            first_day = true;
            continue;
        }
        //rest of file
        for s in line?.split(split_by) {
            let column = s.to_owned();
            if column == "NaN" {
                skip_line = true;
            }
            row_vector.push(column);
        }
        if skip_line {
            row_vector.clear();
            skip_line = false;
            continue;
        }
        let bitcoin = Bitcoin::new(row_vector.remove(0), row_vector.remove(6));
        let day_timestamp = day.timestamp.clone();
        row_vector.clear();

        if bitcoin.timestamp.clone() != day_timestamp {
            day.calculate_average_bitcoin_price();
            let mut returned_day: Day = add_and_retrieve_day(&day, &mut thirty_day_buffer);
            if returned_day.timestamp.clone() != "" {
                // println!("{:?}", returned_day);
                if returned_day.average_price <= day.average_price {
                    returned_day.label = 1.0;
                } else {
                    returned_day.label = 0.0;
                }
            }
            if returned_day.timestamp.clone() != "" {
                write!(&mut output_file, "{}", &returned_day.to_string())?;
            }
            day = Day::new(&bitcoin.timestamp);
        }
        day.add_bitcoin(bitcoin);
    }
    day.calculate_average_bitcoin_price();
    thirty_day_buffer.push_back(day.to_owned());
    let mut returned_day: Day = retrieve_day(&mut thirty_day_buffer);
    while returned_day.timestamp.clone() != "" {
        write!(&mut output_file, "{}", &returned_day.to_string())?;
        returned_day = retrieve_day(&mut thirty_day_buffer);
    }
    Ok(())
}

fn add_and_retrieve_day(day: &Day, thirty_day_buffer: &mut VecDeque<Day>) -> Day {
    let mut day_to_return: Day = Day {
        timestamp: "".to_string(),
        average_price: 0.0,
        bitcoins: vec![],
        label: 0.0,
        number_of_bitcoin: 0,
    };
    let thirty_one = 31;
    thirty_day_buffer.push_back(day.to_owned());
    if thirty_day_buffer.len() as i32 == thirty_one {
        day_to_return = thirty_day_buffer.pop_front().unwrap();
    }
    day_to_return
}

fn retrieve_day(thirty_day_buffer: &mut VecDeque<Day>) -> Day {
    let mut day: Day = Day{
        timestamp: "".to_string(),
        average_price: 0.0,
        bitcoins: vec![],
        label: 0.0,
        number_of_bitcoin: 0
    };
    if !thirty_day_buffer.is_empty() {
        day = thirty_day_buffer.pop_front().unwrap();
    }
    day
}