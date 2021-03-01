import java.io.*;
import model.LogReg;
import model.DataCleanerManual;

class Driver{
	public static void main(String[] args) throws IOException {
		double start, end, intermediate;
		start = System.currentTimeMillis();
		DataCleanerManual.data_cleaner_manual();
		intermediate = System.currentTimeMillis();
		LogReg.log_reg();
		end = System.currentTimeMillis();;
		System.out.println("total runtime = "+String.valueOf((end-start)/1000));
		System.out.println("data cleaner runtime = "+String.valueOf((intermediate-start)/1000));
		System.out.println("log reg runtime = "+String.valueOf((end-intermediate)/1000));
		return;
	}
}
