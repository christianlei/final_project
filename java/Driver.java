import java.io.*;
import model.LogReg;
import model.DataCleanerManual;

class Driver{
	public static void main(String[] args) throws IOException {
		double start, middle, end;
		start = System.currentTimeMillis();
		DataCleanerManual.data_cleaner_manual();
		middle = System.currentTimeMillis();
		LogReg.log_reg();
		end = System.currentTimeMillis();;
		System.out.println("total runtime = "+String.valueOf((end-start)/1000));
		System.out.println("data cleaner runtime = "+String.valueOf((middle-start)/1000));
		System.out.println("log reg runtime = "+String.valueOf((end-middle)/1000));

		return;
	}
}
