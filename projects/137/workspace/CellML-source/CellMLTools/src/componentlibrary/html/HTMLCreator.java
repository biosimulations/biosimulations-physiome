package componentlibrary.html;

import java.util.TreeMap;

import componentlibrary.RCellMLComponent;
import componentlibrary.RComponent;
import componentlibrary.RComponentImporter;

/** Create the HTML documentation. */
public class HTMLCreator {

	/** Create the HTML file for the given components by rendering the
	 * template file. */
	public static void createHTML(String f_components, String f_template, String f_html) throws Exception{
		
		// Get the components
		TreeMap<String, RComponent> cMap = RComponentImporter.readComponentsFromCSV(f_components);
		TreeMap<String, RCellMLComponent> rccMap = RCellMLComponent.generateRCellMLComponents(cMap);
		
		// Get the template renderer and render with the list of components
		HTMLTemplateRenderer tR = new HTMLTemplateRenderer(f_template, f_html);
		tR.render(rccMap);
	}
	
	
	public static void main(final String[] args) throws Exception{
		// Used files for creating the HTML documentation
		String folder = "C:/Users/mkoenig/Desktop/CellML/models/MetabolicLibraryCellML";
		String f_components = folder + "/MCL-components.csv";
		String f_template = "template/components.vm";
		String f_html = folder + "/html/MCL.html";
		
		System.out.println("*** START MCL HTML RENDERING ***");
		System.out.println("f_components : " + f_components);
		System.out.println("f_template : " + f_template);
		System.out.println("f_html : " + f_html);
		
		
		// Create the HTML Documenation
		HTMLCreator.createHTML(f_components, f_template, f_html);
		
		System.out.println("*** END MCL HTML RENDERING ***");
	}
}
