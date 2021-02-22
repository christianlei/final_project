//
// Created by Christian C Lei on 2/19/21.
//
#include <iostream>
#include "Day.h"

Day::Day() {
    empty = true;
}

Day::Day(Bitcoin bitcoin) {
    empty = false;
    label = -1;
    timestamp = bitcoin.getTimestamp();
    bitcoins.push_back(bitcoin);
}

const string &Day::getTimestamp() const {
    return timestamp;
}

void Day::add_bitcoin(Bitcoin bitcoin)
{
    bitcoins.push_back(bitcoin);
}

void Day::calculate_average_weighted_price()
{
    float sum_of_weighted_price = 0.0;
    float num_of_bitcoin_per_day = bitcoins.size();
    for (const Bitcoin& bitcoin : bitcoins)
    {
        sum_of_weighted_price += bitcoin.getWeightPrice();
    }

    average_price =  sum_of_weighted_price / num_of_bitcoin_per_day;
};

ostream& operator<<(std::ostream &strm, const Day &day) {
    if (day.label != -1)
        return strm << day.timestamp << "," << day.average_price << "," << day.label;
    else
        return strm << day.timestamp << "," << day.average_price << ",";
}

bool Day::isEmpty() const {
    return empty;
}

float Day::getAveragePrice() const {
    return average_price;
}

void Day::setLabel(int label) {
    Day::label = label;
}
