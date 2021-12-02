package componentlibrary;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.HashSet;
import java.util.List;
import java.util.TreeMap;

import componentlibrary.RComponent.*;
import tools.opencsv.CSVReader;

/** CSV import of the component information and creating of the list of components .
 * 
 * @author mkoenig
 */
public class RComponentImporter {
	
	public static TreeMap<String, RComponent> readComponentsFromCSV(String f_components) throws Exception{
		TreeMap<String, RComponent> cMap = new TreeMap<String, RComponent>();
		
		CSVReader reader;
		try {
			reader = new CSVReader(new FileReader(f_components));
			List<String []> lines = reader.readAll();
			String [] line;
			
			// ignore the header line
			
			System.out.println("*** START COMPONENT PARSING ***");
			for(int i=1; i<lines.size(); ++i){
				line = lines.get(i);
				// printLine(line, i);
				
				/* Create the component and set the fields
				 * name : line[0]
				 * mechanisms : line[1]
				 * reversibility : line[2]
				 * modifier : line[3]
				 */		
				RComponent c = new RComponent();
				c.setName(parseName(line[0]));
				c.setMechanisms(parseMechanisms(line[1]));
				c.setReversibility(parseReversibilty(line[2]));
				c.setModifier(parseModifier(line[3]));
				cMap.put(c.getName(), c);
			}
			System.out.println("*** END COMPONENT PARSING ***");
			reader.close();
			
		} catch (FileNotFoundException e) {
			System.err.println("Component file not found: " + f_components);
			e.printStackTrace();
		}
		
		return cMap;
	}
	
	private static String parseName(String text) throws Exception{
		if (text==null || text.length()==0)
			raiseParseError("Name", text);
		return text.trim();
	}
	
	private static Reversibility parseReversibilty(String text) throws Exception{
		Reversibility rev = null;
		text = text.trim();
		switch (text){
			case "Rev":
				rev = Reversibility.REVERSIBLE;
				break;
			case "Irrev":
				rev = Reversibility.IRREVERSIBLE;
				break;
			default:
				raiseParseError(Reversibility.class.getName(), text);
		}
		return rev;
	}
	
	private static Modifier parseModifier(String text) throws Exception{
		Modifier mod = null;
		text = text.trim();
		switch (text){
			case "None":
				mod = Modifier.NONE;
				break;
			case "I":
				mod = Modifier.INHIBITOR;
				break;
			case "A":
				mod = Modifier.ACTIVATOR;
				break;
			case "M": 
				mod = Modifier.MODIFIER;
				break;
			case "M2": 
				mod = Modifier.MODIFIER2;
				break;
			default:
				raiseParseError(Modifier.class.getName(), text);
		}
		return mod;
	}
	
	private static HashSet<Mechanism> parseMechanisms(String text) throws Exception{
		HashSet<Mechanism> mSet = new HashSet<Mechanism>();
		// Split the text & parse all the single mechanisms
		String[] tokens = text.split(";");
		for (String token: tokens){
			token = token.trim();
			if (token.length()>0){
				Mechanism m = parseMechanism(token);
				mSet.add(m);
			}
		}
		return mSet;
	}
	
	private static Mechanism parseMechanism(String text) throws Exception{
		Mechanism m = findMechanismByName(text);
		if (m == null){
			raiseParseError(Mechanism.class.getName(), text);
		}
		return m;
	}
	
	private static Mechanism findMechanismByName(String name){
	    for(Mechanism m : Mechanism.values()){
	        if( m.name().equals(name)){
	            return m;
	        }
	    }
	    return null;
	}
	
	private static void raiseParseError(String type, String text) throws Exception{
		throw new Exception(type + ": |" + text + "|");
	}
	
	private static void printLine(String[] line, int i){
		System.out.println("*** Component <" + i + ">");
		System.out.println("name : " + line[0]);
		System.out.println("mechanisms : " + line[1]);
		System.out.println("reversibility : " + line[2]);
		System.out.println("modifier : " + line[3]);
		System.out.println("--------------------------");
	}
	
	public static void main(String[] args) throws Exception{
		String f_components = "C:/Users/mkoenig/Desktop/CellML/models/MetabolicLibraryCellML/MCL-components.csv";
		TreeMap<String, RComponent> cSet = readComponentsFromCSV(f_components);
		int count = 1;
		for (RComponent c: cSet.values()){
			c.print(count);
			count++;
		}
	}
}
