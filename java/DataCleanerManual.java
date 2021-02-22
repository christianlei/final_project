import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import models.Bitcoin;
import models.Day;

class DataCleanerManual {

  static LinkedList<Day> pastDays = new LinkedList<>();

  public static void main(String[] args) throws IOException {
    String line = "";
    String splitBy = ",";
    List<String> oneRow = new ArrayList<>();
    try {
      FileWriter writer = new FileWriter("bitcoin_clean_java.csv");
      BufferedReader br = new BufferedReader(new FileReader("bitcoin_raw.csv"));
      //header
      line = br.readLine();
      String[] header = line.split(splitBy);
      writer.append(header[0]).append(",").append(header[7]).append(",label\n");
      //First Day
      line = br.readLine();
      String[] firstLine = line.split(splitBy);
      Day day = new Day(new Bitcoin(firstLine[0], firstLine[7]));

      while ((line = br.readLine()) != null) {
        String[] row = line.split(splitBy);
        if (Arrays.asList(row).contains("NaN"))
          continue;

        Bitcoin bitcoin = new Bitcoin(row[0], row[7]);
        if (!bitcoin.getTimestamp().equals(day.getTimestamp())) {
          day.calculateAveragePrice();
          Day returned_day = addAndRetrievePastDay(day);
          if (returned_day != null) {
            if (returned_day.getAveragePrice() <= day.getAveragePrice())
              returned_day.setLabel(1);
            else
              returned_day.setLabel(0);
          }
          if (returned_day != null && !returned_day.getTimestamp().equals("2011-12-30")
              && !returned_day.getTimestamp().equals("2011-12-31"))
            writer.append(returned_day.toString());
          day = new Day(bitcoin);
        }
        day.addBitcoin(bitcoin);

      }
      day.calculateAveragePrice();
      pastDays.addLast(day);

      Day returned_day = retrievePastDay();
      while(returned_day != null ) {
        writer.append(returned_day.toString());
        returned_day = retrievePastDay();
      }

      writer.flush();
      writer.close();
      br.close();
    } catch (Exception e) {
        System.out.println(e.toString());
    }
  }


  static Day addAndRetrievePastDay(Day day) {
    final int THIRTY = 30;
    pastDays.addLast(day);
    if(pastDays.size() == THIRTY)
      return pastDays.remove();
    return null;
  }

  static Day retrievePastDay() {
    if(!pastDays.isEmpty())
      return pastDays.remove();
    return null;
  }

}