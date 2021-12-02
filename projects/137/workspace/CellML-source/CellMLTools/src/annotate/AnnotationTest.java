package annotate;


import pjm.XPCOMDerived;
import cellml_api.CellMLComponent;
import cellml_api.Model;
import cellml_api.RDFRepresentation;

import rdf_api.TripleEnumerator;
import rdf_api.TripleSet;
import rdf_api.Triple;
import rdf_api.RDFAPIRepresentation;
import rdf_api.DataSource;
import rdf_api.Node;
import rdf_api.URIReference;
import tools.CellMLWriter;


/*
 * Model annotations should be generated as RDF bags in the following format:
 	SBML annotation:
 		 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
            <rdf:Description rdf:about="#metaid_0000003">
              <bqbiol:is>
                <rdf:Bag>
                  <rdf:li rdf:resource="http://identifiers.org/obo.go/GO:0005737"/>
                </rdf:Bag>
              </bqbiol:is>
            </rdf:Description>
         </rdf:RDF>
         
          <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:bqmodel="http://biomodels.net/model-qualifiers/" xmlns:bqbiol="http://biomodels.net/biology-qualifiers/">
            <rdf:Description rdf:about="#metaid_0000004">
              <bqbiol:is>
                <rdf:Bag>
                  <rdf:li rdf:resource="http://identifiers.org/obo.chebi/CHEBI:17234"/>
                  <rdf:li rdf:resource="http://identifiers.org/kegg.compound/C00293"/>
                </rdf:Bag>
              </bqbiol:is>
            </rdf:Description>
          </rdf:RDF>
     CellML annotation:
     	<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
			<rdf:Description rdf:about="#id_00001">
				<is xmlns="http://biomodels.net/biology-qualifiers/">
					<rdf:Description rdf:about="http://identifiers.org/obo.go/GO:0005829"/>
				</is>
			</rdf:Description>
		</rdf:RDF>
 */
public class AnnotationTest {

	
	public static void getTripletsFromModel(Model model){
		// Retrieve the RDF representation for the model
		RDFRepresentation rdfrep = model.getRDFRepresentation("http://www.cellml.org/RDF/API");
		RDFAPIRepresentation rar = pjm2pcm.rdf_api.RDFAPIRepresentation.queryInterface( 
							(XPCOMDerived)  model.getRDFRepresentation( "http://www.cellml.org/RDF/API" ) );
		DataSource ds = rar.getSource(); 

		TripleSet tripleSet = ds.getAllTriples();
		TripleEnumerator tripleEnumerator = tripleSet.enumerateTriples();
		
		System.out.println("RDF Triplets in current model:");
        while (true) {
            Triple triple = tripleEnumerator.getNextTriple();
            if (triple == null)
                break;
            System.out.println("--------------------");
            // TODO: better RDF output
            Node nObject = triple.getObject();
            System.out.println(nObject.toString());
            		
            Node pObject = triple.getPredicate();
            System.out.println(pObject.toString());
            
            Node sObject = triple.getSubject();
            System.out.println(sObject.toString());
        }
        
        // TODO: make changes and write the source back
        rar.setSource(ds);   
        
	}

	
    /* Generate the following RDF annotation
	<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
		<rdf:Description rdf:about="../../#0001">
			<title xmlns="http://purl.org/dc/elements/1.1/" rdf:datatype="http://purl.org/dc/elements/1.1/title">test title
			
			</title>
		</rdf:Description>
	</rdf:RDF>
	
	<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
		<rdf:Description rdf:about="#id_00001">
		
				<is xmlns="http://biomodels.net/biology-qualifiers/">
					<rdf:Description rdf:about="http://identifiers.org/obo.go/GO:0005829"/>
				</is>
		</rdf:Description>
	</rdf:RDF>
	
    */
	private static void setComponentRdfInModel(CellMLComponent c, Model model){
		
		// get/set the metaID for the component so one can refer in the RDF to it
		String metaID = c.getCmetaId();
		if (metaID == null || metaID.length()==0){
			//TODO: what is standard way to create metaIDs?
			metaID = c.getName() + "_0001";
			c.setCmetaId(metaID);
		}
		System.out.println("metaID: "+metaID);

	    rdf_api.RDFAPIRepresentation rar = 
	    		pjm2pcm.rdf_api.RDFAPIRepresentation.queryInterface( (XPCOMDerived) model.getRDFRepresentation( "http://www.cellml.org/RDF/API" ) );
	    DataSource ds = rar.getSource( );
	    rar.setSource( ds );
	    
	    // Get the link reference
	    URIReference compResource = ds.getURIReference( "#" + metaID );
	    String titleURI = "http://purl.org/dc/elements/1.1/title";
	    String title = "test title";
	    URIReference uriRef = ds.getURIReference( titleURI );
	        
	    
	    compResource.createTripleOutOf( uriRef, ds.getTypedLiteral(title, titleURI ) ); 
	    rar.setSource( ds );
	        
	    //String s = model.getSerialisedText( );
	    //String formattedS = new XMLFormatter( ).format( s ); 
	    //System.out.println( formattedS );

	}
	
	
	public void createTriplett(String pSubject, String pBioQualifier, String pResource, String pId){

		//When setting RDF annotations, you can use the rdf_api methods (see the documentation for details), e.g.
		// To refer to a component from RDF, you need to give the component a unique
		// cmeta:id (if it doesn't already have one)...
		
		// mycomponent.setCmetaId("someuniqueidentifier");
		// URIReference compResource = ds.getURIReference("#" + mycomponent.getCmetaId());
		// compResource.createTripleOutOf(ds.getURIReference("http://example.org/mypredicate"), ds.getPlainLiteral("my plain English value", "en"));
		
        /*
			new CellmlFileRdfTriple(this, rdfTriple);
			
			CellmlFileRdfTriple
			mType = pType;
	        mModelQualifier = pModelQualifier;
    	 	mBioQualifier = pBioQualifier;
			mResource = pResource;
    		mId = pId;
    		
    		// needs the file reference for init
    		CellmlFileRdfTriple
    		CellmlFileRdfTripletElement
		*/
		
		
		//Node mSubject = new CellmlFileRdfTripleElement()
		/*
		CellmlFileRdfTriple::CellmlFileRdfTriple(CellmlFile *pCellmlFile,
	            const QString pSubject,
	            const BioQualifier &pBioQualifier,
	            const QString &pResource,
	            const QString &pId){
			// Construct ourselves
			
			constructor(pCellmlFile, 0, BioModelsDotNetQualifier,
			ModelUnknown, pBioQualifier, pResource, pId);
			
			// Create our RDF triple elements
			
			mSubject   = new CellmlFileRdfTripleElement(pSubject);
			mPredicate = new CellmlFileRdfTripleElement(QString("http://biomodels.net/biology-qualifiers/%1").arg(bioQualifierAsString(pBioQualifier).remove(QRegularExpression("^bio:"))));
			mObject    = new CellmlFileRdfTripleElement(QString("http://identifiers.org/%1/%2").arg(pResource, pId));
		}
		*/
	}


	public static void main(String[] args){
		//String url = "http://www.cellml.org/models/hodgkin_huxley_1952_version07/download";
		String url = "./models/TestModel.cellml";
	    AnnotateVariable avtest = new AnnotateVariable(url);
	    //avtest.iterateModelElements();
		
	    Model model = avtest.getModel();
	    getTripletsFromModel(model);
	    
	    // set RDF for the first component
	    CellMLComponent c = model.getAllComponents().getComponent("component1");
	    setComponentRdfInModel(c, model);
	    
	    CellMLWriter.writeToFile(model, "./models/TestModelRDF.cellml");
	    
	    
	}
}
