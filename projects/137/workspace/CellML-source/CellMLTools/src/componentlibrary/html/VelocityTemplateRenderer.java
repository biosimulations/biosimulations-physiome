package componentlibrary.html;

import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.Template;
import org.apache.velocity.app.Velocity;
import org.apache.velocity.exception.ResourceNotFoundException;
import org.apache.velocity.exception.ParseErrorException;
import org.apache.velocity.exception.MethodInvocationException;


/** 
 * Example how to use Apache Velocity to render an HTML template.
 * 
 */
public class VelocityTemplateRenderer {

	public static void render() throws IOException{
		Velocity.init();

		// Generate the Context for the Template
		VelocityContext context = new VelocityContext();
		context.put( "name", new String("Velocity") );

		// Generate the Template
		Template template = null;
		try
		{
		   template = Velocity.getTemplate("template/mytemplate.vm");
		}
		catch( ResourceNotFoundException rnfe )
		{
		   // couldn't find the template
		   System.out.println("Template not found.");
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
		FileWriter fw = new FileWriter("template/mytemplate.html");
		StringWriter sw = new StringWriter();
		template.merge( context, sw );
		
		fw.write(sw.toString());
		fw.close();
	}
		
	public static void main(String[] args) throws IOException{
		render();
	}
}

