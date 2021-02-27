package models;

import java.util.ArrayList;
import java.util.List;

public class Day {

  String timestamp;
  double averagePrice;
  List<Bitcoin> bitcoins;
  float label;
  int numberOfBitcoin;


  public Day(Bitcoin bitcoin) {
    this.timestamp = bitcoin.getTimestamp();
    bitcoins = new ArrayList<>();
    this.label = -1;
    this.numberOfBitcoin = 0;
  }

  public void addBitcoin(Bitcoin bitcoin) {
    this.bitcoins.add(bitcoin);
    this.numberOfBitcoin = this.bitcoins.size();
  }

  public void calculateAveragePrice() {
    double sum_of_prices = 0;
    for (Bitcoin bitcoin : this.bitcoins) {
      sum_of_prices += bitcoin.getWeightPrice();
    }
    averagePrice = sum_of_prices / bitcoins.size();
  }

  public String getTimestamp() {
    return timestamp;
  }

  public void setLabel(float label) {
    this.label = label;
  }

  public double getAveragePrice() {
    return averagePrice;
  }

  @Override
  public String toString() {
    if (this.label != -1)
      return timestamp + "," + averagePrice + "," + label + '\n';
    else
      return timestamp + "," + averagePrice + "," + '\n';
  }
}
