package model;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

public class Bitcoin {

  String timestamp;
  double weight_price;

  public Bitcoin(String timestamp, String weight_price) {
    Date date = new Date(Long.parseLong(timestamp) * 1000);
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
    sdf.setTimeZone(TimeZone.getTimeZone("UTC"));
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
