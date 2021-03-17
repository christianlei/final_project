Predicting Bitcoin with Machine Learning in 5 Different Programming Languages

The purpose of this repository is to illustrate the similarities and differences between the implemtation of a Logistic Regression Machine Learning model.
To implement our project there are two parts, the data cleaning portion and the machine learning model. These were implemented in 5 languages, Python, Java,
C++, Rust and Go. 

This ReadMe details how to run our program in each of the 5 programming languages.

First download the required data from https://www.kaggle.com/mczielinski/bitcoin-historical-data and rename the downloaded file to 'bitcoin_raw.csv'

Python
- required dependencies:
Pytz

cd python
copy 'bitcoin_raw.csv' into this directory
python3 main.py

C++
cd cpp
copy 'bitcoin_raw.csv' into this directory
make
./driver

Java
cd java
copy 'bitcoin_raw.csv' into this directory
make

Rust
cd rust
copy 'bitcoin_raw.csv' into rust/src directory
cargo build
cargo run

Go
cd go
copy 'bitcoin_raw.csv' into go/driver directory
go run main.go
