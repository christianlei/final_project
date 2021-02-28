import java.io.*;
import model.LogReg;
import model.DataCleanerManual;

class Driver{
	public static void main(String[] args) throws IOException {
		double start, end;
		start = System.currentTimeMillis();
		DataCleanerManual.data_cleaner_manual();
		LogReg.log_reg();
		end = System.currentTimeMillis();;
		System.out.println("runtime = "+String.valueOf((end-start)/1000));

		return;
	}
}
