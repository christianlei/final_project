//
// Created by Christian C Lei on 2/19/21.
//

#ifndef CPP_DAY_H
#define CPP_DAY_H

#include <vector>
#include <iostream>
#include "Bitcoin.h"

using namespace std;

class Day {
    public:
        Day();
        Day(Bitcoin bitcoin);
        void add_bitcoin(Bitcoin bitcoin);
        void calculate_average_weighted_price();
        const string &getTimestamp() const;
        bool isEmpty() const;
        float getAveragePrice() const;
        void setLabel(float label);

private:
        string timestamp;
        float average_price;
        bool empty;
        vector<Bitcoin> bitcoins;
        float label;
        int number_of_bitcoin;
        friend ostream& operator<<(ostream&, const Day&);
};
#endif //CPP_DAY_H

