package models;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Bitcoin {

  String timestamp;
  double weight_price;

  public Bitcoin(String timestamp, String weight_price) {
    Date date = new Date(Long.parseLong(timestamp) * 1000);
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
    this.timestamp = sdf.format(date);
    this.weight_price = Double.parseDouble(weight_price);
  }

  public String getTimestamp() {
    return timestamp;
  }

  public double getWeightPrice() {
    return weight_price;
  }
}
