package cellmlexamples;
import java.io.File;

import sun.rmi.runtime.NewThreadAction;
import tools.CellMLReader;
import tools.CellMLWriter;
import cellml_api.CellMLBootstrap;
import cellml_api.Model;
import cellml_services.TeLICeMModelResult;
import cellml_services.TeLICeMService;


public class TeLICeMTest {
	
	private CellMLBootstrap bootstrap;
	private TeLICeMService ts;
	
	public TeLICeMTest() {
		System.loadLibrary("java_cellml");
		bootstrap = cellml_bootstrap.CellMLBootstrap.createCellMLBootstrap();
		
		System.loadLibrary("java_telicems");
		ts = cellml_bootstrap.TeLICeMSService.createTeLICeMService();
	}

	public String getTeliFromURL(String url){
		Model model = CellMLReader.loadFromURL(bootstrap, url);
		return getTeliFromModel(model);
	}
	
	public String getTeliFromModel(Model model){
		return ts.showModel(model);
	}
	
	public void writeModelFromTeliToFile(String teli, String fname){
		Model model = getModelFromTeli(teli);
		CellMLWriter.writeToFile(model, fname);
	}
	
	public Model getModelFromTeli(String teli){
		TeLICeMModelResult tsRes = ts.parseModel(teli);
		return tsRes.getModelResult();
	}
	
	
	public static void main(String[]args){
		TeLICeMTest teliTools = new TeLICeMTest();
		
		// Load CellML model
		String url = "TestModelRDF.cellml";
		String url2 = "test_import/Example_MassAction_1_flat.cellml";
		String url3 = "test_import/Example_MassAction_1.cellml";
		
		String teli = teliTools.getTeliFromURL(url3);
		System.out.println(teli);
		
		// Create new Model from Teli format
		Model model_out = teliTools.getModelFromTeli(teli);
		
		// Write model
		CellMLWriter.writeToFile(model_out, "teli_test.cellml");
	}
}
