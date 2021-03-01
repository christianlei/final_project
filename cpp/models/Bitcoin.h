#ifndef CPP_BITCOIN_H
#define CPP_BITCOIN_H

#include <string>

using namespace std;

class Bitcoin {
public:
    Bitcoin(const string &originalTimestamp, float weightPrice);
    float getWeightPrice() const;
    const string &getTimestamp() const;

private:
    float weight_price;
    string timestamp;
};

#endif //CPP_BITCOIN_H
