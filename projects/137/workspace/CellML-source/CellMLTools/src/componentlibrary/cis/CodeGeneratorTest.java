package componentlibrary.cis;

import tools.CellMLReader;
import cellml_api.CellMLBootstrap;
import cellml_api.Model;
import cellml_services.CodeGenerator;
import cellml_services.CodeGeneratorBootstrap;
import cellml_services.CodeInformation;
import cellml_services.IDACodeGenerator;

/** Generate C & Python Code from a given model */
public class CodeGeneratorTest {

	/* Use CCGS to generate code analog to 
	* 		CellML2C.cpp
	* 		CellML2Python.cpp
	*/
	private static void generateCode(Model model, boolean useida){
		System.loadLibrary("java_ccgs");
		CodeGeneratorBootstrap cgBootstrap = cellml_bootstrap.CCGSBootstrap.createCodeGeneratorBootstrap();
		
		model.fullyInstantiateImports();
		CodeInformation codeInfo = null;
		if (useida){
			CodeGenerator cg = cgBootstrap.createCodeGenerator();
			codeInfo = cg.generateCode(model);
		} else {
			IDACodeGenerator cgida = cgBootstrap.createIDACodeGenerator();
			codeInfo = cgida.generateCode(model);
		}
		
		// print errors
		String error = codeInfo.getErrorMessage();
		if (error!=null && error.length()>0){
			System.err.println("Code generation error: " + error);
			return;
		}
		
		//the usenames stuff form CellML2C & VellML2Python
		// -> doNameAnnotations()
		
		// How to write the code ???
		System.out.println("*** Code Generated ***");
		System.out.println("NONE: " +  codeInfo.toString());
		
		// String code = ??	
		// uses the -> WriteCode() functions in CellML2C & CellML2Python
		// but not accessible via the API ?
	}
	
	
	public static void main (String[] args){
		System.loadLibrary("java_cellml");
	    CellMLBootstrap bootstrap =  cellml_bootstrap.CellMLBootstrap.createCellMLBootstrap();
		Model model = CellMLReader.loadFromURL(bootstrap, "MassActionBiBiRev.cellml");
		generateCode(model, true);
	}
}
