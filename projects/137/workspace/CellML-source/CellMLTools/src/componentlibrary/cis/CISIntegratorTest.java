package componentlibrary.cis;

import tools.CellMLReader;
import cellml_api.CellMLBootstrap;
import cellml_api.Model;
import cellml_services.CellMLIntegrationService;
import cellml_services.DAESolverCompiledModel;
import cellml_services.ODESolverCompiledModel;

public class CISIntegratorTest {
	public static void main(String args[]){
		// Load Model
		System.loadLibrary("java_cellml");
	    CellMLBootstrap bootstrap =  cellml_bootstrap.CellMLBootstrap.createCellMLBootstrap();
		Model model = CellMLReader.loadFromURL(bootstrap, "MassActionBiBiRev.cellml");
		
		// Compile Model
		System.out.println("# Compiling ODE model ...");
		
		System.loadLibrary("java_cis");
		System.out.println("# Creating integration service...");
		CellMLIntegrationService cis = cellml_bootstrap.CISBootstrap.createIntegrationService();
		ODESolverCompiledModel ccm = cis.compileModelODE(model);
		//DAESolverCompiledModel ccm = cis.compileModelDAE(model);
	}
}
