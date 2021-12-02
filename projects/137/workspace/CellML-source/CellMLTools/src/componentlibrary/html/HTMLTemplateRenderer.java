package componentlibrary.html;

import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.util.TreeMap;

import org.apache.velocity.Template;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.Velocity;
import org.apache.velocity.exception.MethodInvocationException;
import org.apache.velocity.exception.ParseErrorException;
import org.apache.velocity.exception.ResourceNotFoundException;

import componentlibrary.RCellMLComponent;

/**
 * Generate the documentation for the Metabolic Component Library 
 * using velocity templates and information stored for the individual components.
 * Here the MCL component information is written in the HTML template (*.vm).
 * 
 * @author mkoenig
 *
 */
public class HTMLTemplateRenderer {

	private String f_template;
	private String f_html;
	
	public HTMLTemplateRenderer(String f_template, String f_html) throws IOException{
		this.f_template = f_template;
		this.f_html = f_html;
	}
	
	/* Render the template with the given components */
	public void render(TreeMap<String, RCellMLComponent> cMap) throws IOException{
		System.out.println("*** START TEMPLATE RENDERING ***");
		
		Velocity.init();

		// Generate the Context for the Template
		// put the components in the context
		VelocityContext context = new VelocityContext();
		//context.put( "name", new String("Velocity") );
		context.put( "cSet", cMap.values());
		
		
		// Generate the Template
		Template template = null;
		try
		{
		   template = Velocity.getTemplate(f_template);
		}
		catch( ResourceNotFoundException rnfe )
		{
		   // couldn't find the template
		   System.out.println("Template not found.");
		   System.out.println(f_template);
		}
		catch( ParseErrorException pee )
		{
		  // syntax error: problem parsing the template
			System.out.println("Template not parsable.");
		}
		catch( MethodInvocationException mie )
		{
		  // something invoked in the template
		  // threw an exception
			System.out.println("Template method invocation error.");
		}
		catch( Exception e )
		{}
		
		// Render the Template
		FileWriter fw = new FileWriter(f_html);
		StringWriter sw = new StringWriter();
		template.merge( context, sw );
		
		fw.write(sw.toString());
		fw.close();
		System.out.println("HTML --> " + f_html);
		System.out.println("*** END TEMPLATE RENDERING ***");
	}
}
