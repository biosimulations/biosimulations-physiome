package componentlibrary;


import java.util.TreeMap;


import tools.CellMLLoader;
import tools.CellMLReader;
import tools.CellMLWriter;

import cellml_api.CellMLComponent;
import cellml_api.CellMLElement;
import cellml_api.Model;
import cellml_api.Units;
import cellml_api.UnitsIterator;
import cellml_api.UnitsSet;


/**
 * TODO: Also create proper headers for all the CellML files, so they can be 
 * associated with the respective programs.
 */


/** Generates a compact library from the single components and units
 * for reuse. This is the file which is ultimately imported.
 * 
 * @author mkoenig
 */
public class LibraryCreator {

	private String f_lib;
	
	public LibraryCreator(String f_lib){
		this.f_lib = f_lib;
	}
	
	/** Collects all units and basic components in one CellML file. */
	public void generateCompactLibraryFile(TreeMap<String, RCellMLComponent> rccMap){
		CellMLLoader cLoader = new CellMLLoader();
		Model lib_model = CellMLReader.createModel(cLoader.getCellMLBootstrap(), "1.1");
	    lib_model.setName("MetabolicComponentLibrary");
	    
	    // TODO: write additional information via RDF (contact, version, author)
	    
	    // Get the kinetics components (library components & respective units)
		for (String key: rccMap.keySet()){
			
			RCellMLComponent rcc = rccMap.get(key);			
			Model model = rcc.getModel();
			
			// Copy the units
			UnitsSet unitsSet = model.getAllUnits();
			UnitsIterator iter = unitsSet.iterateUnits();
			for (int i=0; i<unitsSet.getLength(); i++){
				Units units = iter.nextUnits();
				ComponentCopy.insertCellMLElementToModel((CellMLElement) units, lib_model);
			}
			
			// Copy the kinetics component
			CellMLComponent component = rcc.getKineticsComponent(); 
			ComponentCopy.insertCellMLElementToModel((CellMLElement) component, lib_model);
		}
		
		// Write the model to the library file
		CellMLWriter.writeToFile(lib_model, f_lib);
	}
	
	
	public static void main(String[] args) throws Exception{
		
		String folder = "C:/Users/mkoenig/Desktop/CellML/models/MetabolicLibraryCellML";
		String f_components = folder + "/MCL-components.csv";
		String f_lib = folder + "/MCL-v0.2.cellml";

		// Read the components
		TreeMap<String, RComponent> cMap = RComponentImporter.readComponentsFromCSV(f_components);
		TreeMap<String, RCellMLComponent> rccMap = RCellMLComponent.generateRCellMLComponents(cMap);
		
		// Create the library
		LibraryCreator lc = new LibraryCreator(f_lib);
		lc.generateCompactLibraryFile(rccMap);	
	}
	
}
