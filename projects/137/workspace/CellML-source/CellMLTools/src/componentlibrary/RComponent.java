package componentlibrary;
import java.util.HashSet;

/* Stores the information for an individual component in the Metabolic
 * Component Library. */
public class RComponent {
		
	public enum Reversibility {
		REVERSIBLE, IRREVERSIBLE;
		
		public String getAbbreviation(){
			String abb = null;
			switch (this){
				case REVERSIBLE:
					abb = "Rev";
					break;
				case IRREVERSIBLE:
					abb = "Irrev";
					break;
				}
			return abb;
		}
	}
	public enum Modifier {
		NONE, INHIBITOR, ACTIVATOR, MODIFIER, MODIFIER2;
		
		public String getAbbreviation(){
			String abb = null;
			switch (this){
				case NONE:
					abb = "";
					break;
				case INHIBITOR:
					abb = "_I";
					break;
				case ACTIVATOR:
					abb = "_A";
					break;
				case MODIFIER:
					abb = "_M";
					break;
				case MODIFIER2:
					abb = "_M2";
					break;
			}
			return abb;
		}
		
	}
	public enum Mechanism implements Comparable<Mechanism> {
		NullUni, NullBi, NullTri,
		UniNull, UniUni, UniBi, UniTri,
		BiNull, BiUni, BiBi, BiTri,
		TriNull, TriUni, TriBi, TriTri
	}
	
	public HashSet<String> getSBGNSet(){
		HashSet<String> sbgnSet = new HashSet<String>();
		String sbgn = null;
		for (Mechanism m: this.mechanisms){
			sbgn = m.name() + this.getReversibility().getAbbreviation() 
						    + this.getModifier().getAbbreviation();
			sbgnSet.add(sbgn);
		}
		return sbgnSet;
	}
	
	private String name; 
	private Reversibility reversibility;
	private Modifier modifier;
	private HashSet<Mechanism> mechanisms;
	
	public String getName() {
		return name;
	}
	public Reversibility getReversibility() {
		return reversibility;
	}
	public Modifier getModifier() {
		return modifier;
	}
	public HashSet<Mechanism> getMechanisms() {
		return mechanisms;
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setReversibility(Reversibility reversibility) {
		this.reversibility = reversibility;
	}
	public void setModifier(Modifier modifier) {
		this.modifier = modifier;
	}
	public void setMechanisms(HashSet<Mechanism> mechanisms) {
		this.mechanisms = mechanisms;
	}
	
	/* Create component from parsed CSV data. */
	public RComponent(){}
	
	/* Copy Constructor */
	public RComponent(RComponent c){
		this.name = c.getName();
		this.reversibility = c.getReversibility();
		this.modifier = c.getModifier();
		this.mechanisms = c.getMechanisms();	
	}
		
	public String toString(int index){
		String s = "*** Component <" + index + "> ***\n";
		s += "name : " + this.getName() + "\n";
		s += "reversibility : " + this.getReversibility() + "\n";
		s += "modifier : " + this.getModifier() + "\n";
		s += "mechanisms : ";
		for (Mechanism m: mechanisms){
			s += m.name() + ";";
		}
		s += "\n";
		return s;
	}
	
	public void print(int index){
		String s = this.toString(index);
		System.out.println(s);
	}
	
}
