package componentlibrary;


import pjm.XPCOMDerived;
import tools.CellMLReader;
import tools.CellMLWriter;
import cellml_api.CellMLBootstrap;
import cellml_api.CellMLElement;
import cellml_api.Model;
import cellml_api.Units;
import cellml_api.UnitsIterator;
import cellml_api.UnitsSet;
import dom.Document;
import dom.Element;
import dom.NamedNodeMap;
import dom.Node;
import dom.NodeList;

public class ComponentCopy {
	
	/*
	 * I want to copy a unit or component from one model to another model.
	 * This always throws native code exceptions.
	 * It seems that this is not possible ?????? This is most basic functionality ?
	 * I found in the C++ source code the following which seems to be the problem.
	 * 
	 * This next bit is a very pragmatic way of deciding when to throw away the
	 * caches. We need to know when the cache might be stale, while at the same
	 * time changes must be efficient. This problem is not as easy as checking the
	 * root, since we could easily be working with partial fragments, which get
	 * re-arranged. We could do this properly by visiting all elements connected to
	 * the element being changed, and invalidating the cache at that time, but that
	 * would be too slow. Instead, we have a single global serial number, which we
	 * touch every time a change is made. If the current serial number doesn't
	 * match the number on the cache, we throw the cache away and rebuild. This
	 * does, of course, have the downside that if you have two models open, changes
	 * to one model will wipe the cache of the other, completely separate model.
	 * The other issue is that serial numbers wrap, so we should make sure the type
	 * is big enough. At 1000 changes/second, it would take 49 days to get a
	 * conflict with 32 bits, or about 585 million years with 64 bits.
	 * 
	 * This should be the way to go to handle copying via the API !!!
	 */
	 public static void copyClassic(){
			System.loadLibrary("java_cellml");
		    CellMLBootstrap bootstrap =  cellml_bootstrap.CellMLBootstrap.createCellMLBootstrap();
			
		    // Create new model
		    Model lib_model = CellMLReader.createModel(bootstrap, "1.1");
		    lib_model.setName("MetabolicComponentLibrary" );
			
		    // Copy units from second model !!!
		    Model m = CellMLReader.loadFromURL(bootstrap, "test.cellml");
		    
		    UnitsSet unitsSet = m.getAllUnits();
			UnitsIterator iter = unitsSet.iterateUnits();
			for (int i=0; i<unitsSet.getLength(); i++){
				Units units = iter.nextUnits();
				lib_model.addElement(units);
			}
			// Identical problem with copying components between models!!!
	 }
	
	 
	 /* This is the way it has to be done !*/
	 public static void copyUnitsTest(){
			System.loadLibrary("java_cellml");
		    CellMLBootstrap bootstrap =  cellml_bootstrap.CellMLBootstrap.createCellMLBootstrap();
			
		    // Create new model
		    Model lib_model = CellMLReader.createModel(bootstrap, "1.1");
		    lib_model.setName("MetabolicComponentLibrary" );
			
		    // Copy units from second model !!!
		    Model m = CellMLReader.loadFromURL(bootstrap, "test.cellml");
		    
		    UnitsSet unitsSet = m.getAllUnits();
			UnitsIterator iter = unitsSet.iterateUnits();
			for (int i=0; i<unitsSet.getLength(); i++){
				Units units = iter.nextUnits();
				insertCellMLElementToModel((CellMLElement) units, lib_model);
			}
			unitsSet = m.getAllUnits();
			iter = unitsSet.iterateUnits();
			for (int i=0; i<unitsSet.getLength(); i++){
				Units units = iter.nextUnits();
				insertCellMLElementToModel((CellMLElement) units, lib_model);
			}
			
			CellMLWriter.writeToFile(lib_model, "lib_model.cellml");
	 }
	 
	 /* Copying of CellMLelements via the DOM necessary.
	  * Instances can't be copied between different models !
	  * 
	  * Tests for uniqueness of components necessary! The DOM will just add the same
	  * Elements over and over again, so existence test based on "name" attribute in the
	  * respective elements necessary. 
	  * 
	  * Use for : Units, Components, Mappings
	  */
	 public static boolean insertCellMLElementToModel(CellMLElement element, Model model){
		 	Element modelElement = 
					pjm2pcm.cellml_api.CellMLDOMElement.queryInterface((XPCOMDerived) model).getDomElement();
			Element componentToCopyEl =
					pjm2pcm.cellml_api.CellMLDOMElement.queryInterface((XPCOMDerived) element).getDomElement();
			if (isElementInModelElement(componentToCopyEl, modelElement)){
				return false;
			}
			Document modelDoc = modelElement.getOwnerDocument();
			// deep = true -> full copy 
			modelElement.appendChild(modelDoc.importNode(componentToCopyEl, true));
			return true;
	 }
	 
	 /* Test if the element identified by tuple (CellMlComponent, name) is already in the model.
	  *	This is stuff the API should handle! Now we are writing XML and traversing the DOM (WTF).
	  * This will work for my models but will break against the specifications !. 
	  */
	 public static boolean isElementInModelElement(Element element, Element modelElement){
		 // Element is uniquely identified via type (Unit, Component, Mapping, ...?) & name
		 // Is this true? Who knows?
		 String name = element.getAttribute("name");
		 String tagName = element.getTagName();
		 //System.out.println(tagName + " : name=" + name);
		 
		 NodeList nodes = modelElement.getElementsByTagName(tagName);
		 for (int k=0; k<nodes.getLength(); ++k){
			 
			 Node testNode = nodes.item(k);
			 NamedNodeMap map = testNode.getAttributes();
			 String testName = map.getNamedItem("name").getNodeValue();

			 //System.out.println("exists -> " + tagName + " : name=" + testName);
			 if(testName.equals(name)){
				 return true;
			 }
		 }
		 return false;
	 }
	 
	public static void main(String[] args){
		copyUnitsTest();
	}		
}
