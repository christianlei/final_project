#include "data_cleaner_manual.h"

Day* add_and_retrieve_past_day(queue<Day*> *past_days, Day* day);

Day* retrieve_past_day(queue<Day*> *past_days);

void data_cleaner_manual() {

    ifstream rawcsv;
    ofstream *cleancsv = new ofstream();
    queue<Day*> *past_days = new queue<Day*>;
    stringstream ss;
    bool nan_in_line = false;
    const int FIRST_DATE_TO_PARSE = 1325376000;

    rawcsv.open("bitcoin_raw.csv");
    (*cleancsv).open("bitcoin_clean_cpp.csv");

    if (rawcsv.is_open()) {
        string line;
        getline(rawcsv, line);
        ss.str(line);

        //header
        vector<string> one_row;
        string token;
        while (getline(ss, token, ',')) {
            one_row.push_back(token);
        }

        *cleancsv << one_row[0] << "," << one_row[7] << ",label" << endl;

        //first day
        one_row.clear();
        getline(rawcsv, line);
        ss.clear();
        ss.str(line);
        while (getline(ss, token, ',')) {
            one_row.push_back(token);
        }
        if (find(one_row.begin(), one_row.end(), "NaN") != one_row.end())
            nan_in_line = true;
        while (nan_in_line or stoi(one_row[0]) < FIRST_DATE_TO_PARSE) {
            one_row.clear();
            getline(rawcsv, line);
            ss.clear();
            ss.str(line);
            while (getline(ss, token, ',')) {
                one_row.push_back(token);
            }
            if (find(one_row.begin(), one_row.end(), "NaN") != one_row.end())
                nan_in_line = true;
            else
                nan_in_line = false;
        }

        Bitcoin bitcoin = Bitcoin(one_row[0], stof(one_row[7]));
        Day* day = new Day(bitcoin);
        day->add_bitcoin(bitcoin);

        //Rest of days
        while (getline(rawcsv, line)) {
            one_row.clear();
            ss.clear();
            ss.str(line);
            while (getline(ss, token, ',')) {
                one_row.push_back(token);
            }
            if (find(one_row.begin(), one_row.end(), "NaN") != one_row.end())
                nan_in_line = true;
            if (nan_in_line) {
                nan_in_line = false;
                continue;
            }


            bitcoin = Bitcoin(one_row[0], stof(one_row[7]));

            if (bitcoin.getTimestamp() != day->getTimestamp()) {
                day->calculate_average_weighted_price();
                Day* returned_day = add_and_retrieve_past_day(past_days, day);
                if (returned_day != nullptr) {
                    if (returned_day->getAveragePrice() <= day->getAveragePrice()) {
                        returned_day->setLabel(1.0);
                    } else {
                        returned_day->setLabel(0.0);
                    }
                }
                if (returned_day != nullptr) {
                    *cleancsv << *returned_day << endl;
                }
                delete returned_day;
                day = new Day(bitcoin);
            }
            day->add_bitcoin(bitcoin);
        }
        day->calculate_average_weighted_price();
        past_days->push(day);

        Day* returned_day = retrieve_past_day(past_days);
        while (returned_day != nullptr) {
            *cleancsv << *returned_day << endl;
            delete returned_day;
            returned_day = retrieve_past_day(past_days);
        }
        rawcsv.close();
        delete cleancsv;
        delete past_days;
    } else cout << "Unable to open file";
}

Day* add_and_retrieve_past_day(queue<Day*> *past_days, Day *day) {
    const int THIRTY_ONE = 31;
    past_days->push(day);
    if (past_days->size() == THIRTY_ONE) {
        Day *past_day = past_days->front();
        past_days->pop();
        return past_day;
    }
    return nullptr;
}

Day* retrieve_past_day(queue<Day*> *past_days) {
    if (!(*past_days).empty()) {
        Day* past_day = past_days->front();
        past_days->pop();
        return past_day;
    }
    return nullptr;
}