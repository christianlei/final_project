import java.io.*;
import java.util.Arrays;
import java.util.LinkedList;
import models.Bitcoin;
import models.Day;

class DataCleanerManual {

  static LinkedList<Day> pastDays = new LinkedList<>();

  public void data_cleaner_manual() throws IOException {
    String line = "";
    String splitBy = ",";
    final int FIRST_DATE_TO_PARSE = 1325376000;

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
      while (Arrays.asList(firstLine).contains("NaN") || Float.parseFloat(firstLine[0]) < FIRST_DATE_TO_PARSE) {
        line = br.readLine();
        firstLine = line.split(splitBy);
      }
      Bitcoin bitcoin = new Bitcoin(firstLine[0], firstLine[7]);
      Day day = new Day(bitcoin);
      day.addBitcoin(bitcoin);

      while ((line = br.readLine()) != null) {
        String[] row = line.split(splitBy);
        if (Arrays.asList(row).contains("NaN"))
          continue;

        bitcoin = new Bitcoin(row[0], row[7]);
        if (!bitcoin.getTimestamp().equals(day.getTimestamp())) {
          day.calculateAveragePrice();
          Day returned_day = addAndRetrievePastDay(day);
          if (returned_day != null) {
            if (returned_day.getAveragePrice() <= day.getAveragePrice())
              returned_day.setLabel(1);
            else
              returned_day.setLabel(0);
          }
          if (returned_day != null)
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
  Day addAndRetrievePastDay(Day day) {
    final int THIRTY_ONE = 31;
    pastDays.addLast(day);
    if(pastDays.size() == THIRTY_ONE)
      return pastDays.remove();
    return null;
  }
  Day retrievePastDay() {
    if(!(pastDays.size() == 1))
      return pastDays.remove();
    return null;
  }
}