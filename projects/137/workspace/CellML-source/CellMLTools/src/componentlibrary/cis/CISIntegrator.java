package componentlibrary.cis;

import java.util.Vector;

import tools.CellMLReader;
import cellml_api.CellMLBootstrap;
import cellml_api.CellMLVariable;
import cellml_api.Model;
import cellml_services.CellMLIntegrationService;
import cellml_services.CodeInformation;
import cellml_services.ComputationTarget;
import cellml_services.ComputationTargetIterator;
import cellml_services.IntegrationProgressObserver;
import cellml_services.ODESolverCompiledModel;
import cellml_services.ODESolverRun;
import cellml_services.VariableEvaluationType;

/** Perform the integration of a CellML model via CIS. */
public class CISIntegrator {
	
	private Model model;
	private CellMLIntegrationService cis;
	
	boolean gFinished = false;
	
	double gStart = 0.0;
	double gStop = 10.0;
	double gDensity = 1000.0;
	double gTabStep = 0.0;
	boolean gTStrict = false;
		
	public CISIntegrator(Model model){
		System.loadLibrary("java_cis");
		System.out.println("# Creating integration service...");
		cis = cellml_bootstrap.CISBootstrap.createIntegrationService();
		this.model = model; 
	}
	
	public CellMLIntegrationService getCIS(){
		return cis;
	}
	
	public void runIntegration(){
			System.out.println("# Compiling ODE model ...");
			ODESolverCompiledModel ccm = cis.compileModelODE(model);
			
			System.out.println("# Creating run...\n");
			ODESolverRun osr = cis.createODEIntegrationRun(ccm);  
			
			
			// Progress Observer
			TestProgressObserver tpo = new TestProgressObserver(ccm);
			osr.setProgressObserver(tpo);
			
			// Here the keywords are parsed and set to the cir
			this.setParameters(osr);
			
			// Start integration
			osr.start();
			
			while (!gFinished)
				try {
					Thread.sleep(1);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
	}
	
	public void setParameters(ODESolverRun osr){
		// Step Type
		cellml_services.ODEIntegrationStepType ist = cellml_services.ODEIntegrationStepType.RUNGE_KUTTA_2_3;
		osr.setStepType(ist);
		
		// Step Size Control (epsAbs, epsRel, scalVar, scalRate, maxStep)
		double epsAbs = 1E-6;
		double epsRel = 1E-6;
		double scalVar = 1.0;
		double scaleRate = 0.0;
		double maxStep = 1.0;
		osr.setStepSizeControl(epsAbs, epsRel, scalVar, scaleRate, maxStep);
		
		// Range
		double start = 0.0;
		double stop = 10.0;
		double density = 1000.0;
		osr.setResultRange(start, stop, density);
		gStart = start;
		gStop = stop;
		gDensity = density;

		// Tabulation
	    double tabStep = 0.1;
	    boolean tstrict = false;
		osr.setTabulationStepControl(tabStep, tstrict);
		gTabStep = tabStep;
		gTStrict = tstrict;
	}
	
	/** Implement a concrete IntegrationProgressObserver.*/
	public class TestProgressObserver implements IntegrationProgressObserver{
		private ODESolverCompiledModel mCCM; 
		private CodeInformation mCI;

		public TestProgressObserver(ODESolverCompiledModel ccm) {
			mCCM = ccm;
			mCI = ccm.getCodeInformation();
			
			// iterate over the ComputationTargets
			ComputationTargetIterator cti = mCI.iterateTargets();
			while(true){
				ComputationTarget ct = cti.nextComputationTarget();
				if (ct == null){
					break;
				}
				VariableEvaluationType veType = ct.getType();
				if((veType == VariableEvaluationType.STATE_VARIABLE ||
						veType == VariableEvaluationType.ALGEBRAIC ||
						veType == VariableEvaluationType.VARIABLE_OF_INTEGRATION)
					&& ct.getDegree() == 0){
					CellMLVariable source = ct.getVariable();
					String n = source.getName();
					System.out.print(String.format("%s, ", n));
				}
			}
		}

		public void results(Vector<Double> values) {
			long aic = mCI.getAlgebraicIndexCount();
			long ric = mCI.getRateIndexCount();
			long recsize = 2 * ric + aic + 1;

			for (int i = 0; i < values.size(); i+= recsize) {

				// iterate over the ComputationTargets
				ComputationTargetIterator cti = mCI.iterateTargets();
				while (true) {
					ComputationTarget ct = cti.nextComputationTarget();
					if (ct == null) {
						break;
					}
					if (ct.getDegree() != 0) {
						continue;
					}
					VariableEvaluationType et = ct.getType();
					long varOff = 0;
					switch (et) {
					case STATE_VARIABLE:
						varOff = 1 + ct.getAssignedIndex();
						break;
					case VARIABLE_OF_INTEGRATION:
						varOff = 0;
						break;
					case ALGEBRAIC:
						varOff = 1 + 2 * ric + ct.getAssignedIndex();
						break;
					default:
						continue;
					}
					System.out.print(String.format("%g, ",
							values.get((int) (i + varOff))));
				}
				System.out.print("\n");	
			}

		}
		
		public void failed(String errmsg){
			 System.out.println(String.format("# Integration failed (%s)\n", errmsg));
			 gFinished = true;
		}
		
		public void done() {
			   System.out.println("# Run completed.");
			   gFinished = true;
		}
		
		public void computedConstants(Vector<Double> arg0) {
			// TODO Auto-generated method stub
			
		}
	}
	
	
	
	
	
	public static void main(String args[]){
		// Load Model
		System.loadLibrary("java_cellml");
	    CellMLBootstrap bootstrap =  cellml_bootstrap.CellMLBootstrap.createCellMLBootstrap();
		Model model = CellMLReader.loadFromURL(bootstrap, "MassActionBiBiRev.cellml");
		
		// Run integration
		CISIntegrator cisIntegrator = new CISIntegrator(model);
		cisIntegrator.runIntegration();
	}
}
