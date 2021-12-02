package componentlibrary;

import java.util.LinkedList;
import java.util.List;
import java.util.TreeMap;

import tools.CellMLLoader;
import tools.CellMLReader;
import cellml_api.CellMLComponent;
import cellml_api.CellMLComponentIterator;
import cellml_api.CellMLComponentSet;
import cellml_api.CellMLVariable;
import cellml_api.CellMLVariableIterator;
import cellml_api.CellMLVariableSet;
import cellml_api.Model;
import cellml_services.CellMLValidityError;
import cellml_services.CellMLValidityErrorSet;
import cellml_services.VACSService;

/* Exented RComponent which also handles the CellMLComponent information 
 * defined for the RComponent, thereby providing access to the variables 
 * and math.
 */
public class RCellMLComponent extends RComponent{
	private static String LIBRARY_FOLDER = "C:/Users/mkoenig/Desktop/CellML/models/MetabolicLibraryCellML/";
	
	private CellMLLoader cLoader;
	private Model model;
	
	public RCellMLComponent(RComponent c){
		super(c);
		cLoader = new CellMLLoader();
		model = loadCellmlModelForRComponent();
		
		assert(model.getName() == this.getName());
		assert(getKineticsComponent() != null);
		assert(getTestComponent() != null);
		//TODO: how to make asserts that are tested?
		
	}
	
	public Model getModel(){
		return model;
	}
	
	public String getCellmlFile(){
		return LIBRARY_FOLDER + "library/" + this.getName() + ".cellml";
	}
	
	private Model loadCellmlModelForRComponent() {
		Model model = CellMLReader.loadFromURL(cLoader.getCellMLBootstrap(), this.getCellmlFile());
		return model;
	}
	
	private CellMLComponent getComponentByName(String name){
		CellMLComponentSet componentSet = model.getModelComponents();
		
		// use the iterator to find the respective component
		CellMLComponentIterator iter = componentSet.iterateComponents();
		for(int i = 0; i < componentSet.getLength(); i++){
	    	CellMLComponent c = iter.nextComponent();
			if (c.getName().equals(name)){
				return c;
			}
		}
		return null;
	}
	
	/* Returns the test component */
	public CellMLComponent getTestComponent(){
		String name = "Test";
		return getComponentByName(name);
	}
	
	/* Returns the kinetics component */
	public CellMLComponent getKineticsComponent(){
		String name = this.getName();
		return getComponentByName(name);
	}
	
	public List<String> getVariablesFromKineticsComponent(){
		CellMLComponent comp = this.getKineticsComponent();
		List<String> vars = getVariablesFromComponent(comp);
		return vars;
	}
	
	/* Returns list of the variables and the respective units for the components */
	private static List<String> getVariablesFromComponent(CellMLComponent c){
		List<String> vars = new LinkedList<String>();
		
		CellMLVariableSet variableSet = c.getVariables();
		CellMLVariableIterator varIter = variableSet.iterateVariables();
		for (int j = 0; j < variableSet.getLength(); j++) {
			CellMLVariable variable = varIter.nextVariable();
			String s = (variable.getName() + " ["+ variable.getUnitsName() + "]");
			vars.add(s);
		}
		return vars;
	}
	
	public static TreeMap<String, RCellMLComponent> generateRCellMLComponents(TreeMap<String, RComponent> cMap){
		TreeMap<String, RCellMLComponent> rccMap = new TreeMap<String, RCellMLComponent>();
		for (String key: cMap.keySet()){
			RCellMLComponent rcc = new RCellMLComponent(cMap.get(key));
			rccMap.put(key, rcc);
		}
		return rccMap;
	}
	
	/* TODO: proper parsing of the validation information
	 * TODO: every call makes a full validation against the CellML
	 * 		API specification */
	public long getNValidationErrors(){
		// validate the CellML file (VACSS)
		System.loadLibrary("java_vacss");
		VACSService vService = cellml_bootstrap.VACSSBootstrap.createVACSService();
		CellMLValidityErrorSet vErrorSet = vService.validateModel(model);
		long NErrors = vErrorSet.getNValidityErrors();
		
		if (NErrors != 0){
			System.out.println("Validation errors: " + NErrors);
			for (int k=0; k<vErrorSet.getNValidityErrors(); ++k){
				CellMLValidityError vError = vErrorSet.getValidityError(k);
				System.out.println("<" + k + "> " + vError.toString());
				System.out.println(vError.getDescription());
			}
		}
		return NErrors;
	}
	

}
