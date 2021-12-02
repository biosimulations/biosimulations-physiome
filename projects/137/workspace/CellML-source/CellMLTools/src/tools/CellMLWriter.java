package tools;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import cellml_api.Model;

public class CellMLWriter {
  public static void writeToFile(Model model, String outputFileName ){
    try{
      PrintWriter writer = new PrintWriter(new FileWriter(outputFileName));
      writer.println(model.getSerialisedText());
      writer.close();
    }
    catch(IOException e)
    {
      e.printStackTrace();
    }
  }
}