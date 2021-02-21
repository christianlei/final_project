package models;

import java.util.ArrayList;
import java.util.List;

public class Day {

  String timestamp;
  double averagePrice;
  List<Bitcoin> bitcoins;
  int label;


  public Day(Bitcoin bitcoin) {
    this.timestamp = bitcoin.getTimestamp();
    bitcoins = new ArrayList<>();
    this.bitcoins.add(bitcoin);
  }

  public void addBitcoin(Bitcoin bitcoin) {
    this.bitcoins.add(bitcoin);
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

  public void setLabel(int label) {
    this.label = label;
  }

  public double getAveragePrice() {
    return averagePrice;
  }

  @Override
  public String toString() {
    return timestamp + "," + averagePrice + "," + label + '\n';
  }
}
