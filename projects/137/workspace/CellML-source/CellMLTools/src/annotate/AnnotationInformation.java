package annotate;

/** Stores the information which should be annotated. 
 * 
 * TODO: proof of principle single annotation of variable and component with RDF information
 * Use the C++ sample code to get it to work.
 * 
 * */
public class AnnotationInformation {
	String component;
	String variable;
	
	// RDF triple to annotate
	String rdf1;
	String rdf2;
	String rdf3;
	
	/* Component Annotation */
	public boolean isComponentAnnotation(){
		return (component != null) && (variable == null);
	}
	
	/* Variable Annotation */
	public boolean isVariableAnnotation(){
		return (component != null) && (variable != null);
	}
	
	public void getRDF(){
		return;
	}
	
	
}
