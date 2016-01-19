package test;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class AssignmentTestTest {
	public static void main(String[] args){
		int ct_points = 0; //Correct type points out of 1
		int tc_points = 0; //Test case points out of 3
		String result = "";
		String filename = "filename";

		if(args.length > 0) {
			filename = args[0];
		}
		
		String type = getType(AssignmentTest.helloWorld());
		
		if(type.equals("java.lang.String")){ //Check for correct type
			ct_points += 1;
			result = AssignmentTest.helloWorld();
			
			result = result.replaceAll("[^A-Za-z]", "");
			result = result.toLowerCase();

			
			if(result.equals("helloworld")){
				tc_points += 3;
			}
		}

		try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter((filename + ".txt"), true)))) {
		    out.println("Correct Return Type ............." + ct_points + " out of 1");
		    out.println("-Expected: java.lang.String | Type: " + type);
		    out.println("Test Case ......................." + tc_points + " out of 3");
		    out.println("-Summary: Striped all non-letters from result and set all letters to lowercase");
		    out.println(" Expected: \"helloworld\" | Result: \"" + result + "\"");
		} catch (IOException ex) {
			System.out.println("There was a problem writing to file.");
		}
		System.out.print(ct_points + "|" + tc_points);
	}
	
	public static String getType(Object obj){
		return obj.getClass().getName();
	}
	
	
}
