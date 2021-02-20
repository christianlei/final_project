//
// Created by Christian C Lei on 2/19/21.
//

#include <chrono>
#include "Bitcoin.h"

using namespace std;

Bitcoin::Bitcoin(const string &originalTimestamp, float weightPrice) : weight_price(weightPrice) {
    char buffer[256];
    long temp = stol(originalTimestamp);
    const time_t old = (time_t)temp;
    struct tm *oldt = gmtime(&old);
    strftime(buffer, sizeof(buffer), "%Y-%m-%d", oldt);
    timestamp = buffer;
}

float Bitcoin::getWeightPrice() const {
    return weight_price;
}

const string &Bitcoin::getTimestamp() const {
    return timestamp;
}