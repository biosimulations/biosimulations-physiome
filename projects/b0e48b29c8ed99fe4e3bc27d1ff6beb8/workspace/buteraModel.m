
% This program creates an XML file in the current directory. The file can
% be run in OpenCell to simulate the neuron model given on p.400 in Butera      
% et. al 1999b. g_syn_e is given pseudo-random values from a normal
% distribution of user specified mean and standard deviation.
%
% Note: To run the outputted file in OpenCell, the one cell model from the
% repository must be in the same folder, and its name should not have been
% changed.

% Ask user how many neurons are to be modelled
disp (' ') ; neuronCount = input ('How many neurons are to be modelled : ') ;

% Prompt user to enter the seed of the random number generation
disp (' ') ; SEED = input ('Please enter the seed of the random number generation: ') ;

% Prompt user to enter the mean and standard deviation of the normal dist.
disp (' ') ;
g_syn_e_mean = input ('Please enter the mean of g_syn_e normal distribution : ') ;
g_syn_e_stdDev = input ('Please enter the standard deviation of g_syn_e normal distribution : ') ;

% Create array of pseudo-random g_syn_e values
randn ('seed', SEED) ;
g_syn_e = g_syn_e_mean + g_syn_e_stdDev * randn (neuronCount, neuronCount) ;

% Begin XML code, and add imports and connections
f = [ 
'<?xml version="1.0"?>\n' ...
'  <model \n' ...
'    xmlns="http://www.cellml.org/cellml/1.1#" \n' ...
'    xmlns:cmeta="http://www.cellml.org/metadata/1.0#" \n' ...
'    cmeta:id="butera_%d_cell_1999" \n' ...
'    name="butera_%d_cell_1999"> \n\n'  ...
'\n'  ...
'<!-- seed %d -->\n'  ...
'<!-- g_syn_e_mean %d -->\n'  ...
'<!-- g_syn_e_stdDev %d -->\n'  ...
];
xmlCode = sprintf (f , neuronCount, neuronCount, SEED, g_syn_e_mean, g_syn_e_stdDev) ;

for i = 1 : neuronCount
f = [  ...
'  <import xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="butera_single_cell_1999.cellml">\n' ...
'     <component component_ref="single_neuron_model" name="single_neuron_model%d"/>\n' ...
'  </import>\n' ...
'\n' ...
'  <connection>\n' ...
'      <map_components component_1="single_neuron_model%d" component_2="synaptic_coupling"/>' ...
'      <map_variables variable_1="s" variable_2="s%d"/>\n' ...
'      <map_variables variable_1="sum_g_syn_e_s" variable_2="sum_g_syn_e_s_%d"/>\n' ...
'  </connection> \n\n' ...
];
    importsConnections = sprintf (f, i, i, i,i) ;
   
    xmlCode = [xmlCode importsConnections] ;
end

% Adding g_syn_e units, and initialising the synaptic component code
f = [ ...
'  <units name="nanoS">\n' ...
'    <unit prefix="nano" units="siemens"/>\n' ...
'  </units>\n' ...
'\n' ...
'  <units name="millivolt">\n' ...
'    <unit prefix="milli" units="volt"/>\n' ...
'  </units>\n' ...
'\n' ...
'  <units name="millisecond">\n' ...
'    <unit prefix="milli" units="second"/>\n' ...
'  </units>\n' ...
'\n' ...
'  <component cmeta:id="synaptic_coupling" name="synaptic_coupling"> \n' ...
] ;
g_syn_e_misc = sprintf (f) ;
  
xmlCode = [xmlCode g_syn_e_misc] ;

% Adding sum_g_syn_e_s variables and g_syn_e values
for i = 1 : neuronCount
    sum_g_syn_e_s_variables = sprintf ('    <variable name="sum_g_syn_e_s_%d" public_interface="out" units="nanoS"/> \n', i) ;
    xmlCode = [xmlCode sum_g_syn_e_s_variables] ;
end

formatting = sprintf ('\n') ;
xmlCode = [xmlCode formatting] ;

for i = 1 : neuronCount
    for j = 1 : neuronCount
        if (i ~= j)
            g_syn_e_values = sprintf ('    <variable initial_value="%f" name="g_syn_e_%d_%d" units="nanoS"/> \n', g_syn_e (i, j), i, j) ;
            xmlCode = [xmlCode g_syn_e_values] ;
        end
    end
end

% Adding a variable to represent each neuron and g_syn_e math code
xmlCode = [xmlCode formatting] ;

for i = 1 : neuronCount
    neuronVariables = sprintf ('    <variable name="s%d" public_interface="in" units="dimensionless"/> \n', i) ;
    xmlCode = [xmlCode neuronVariables] ;
end

xmlCode = [xmlCode formatting] ;

initialMath = sprintf ('    <math xmlns="http://www.w3.org/1998/Math/MathML"> \n') ;
xmlCode = [xmlCode initialMath] ;

for j = 1 : neuronCount
    sum_g_syn_e_s_math = sprintf ('      <apply><eq /> \n        <ci> sum_g_syn_e_s_%d </ci> \n        <apply><plus /> \n', j) ;
    xmlCode = [xmlCode sum_g_syn_e_s_math] ;
    
    for i = 1 : neuronCount
        if (i ~= j)
f = [ ...
'		  <apply>\n' ...
'            <times/>\n' ...
'            <ci> g_syn_e_%d_%d </ci>\n' ...
'            <ci> s%d </ci>\n' ...
'          </apply> \n' ...
] ;
            g_syn_e_math = sprintf (f, i, j, i) ;
          
            xmlCode = [xmlCode g_syn_e_math] ;
        end
    end
    
    mathEnd = sprintf ('		</apply> \n	  </apply> \n\n') ;
    xmlCode = [xmlCode mathEnd] ;
end

ending = sprintf ('	</math> \n  </component> \n\n') ;
xmlCode = [xmlCode ending] ;

% Adding code for the component which allows session file creation
initialise = sprintf ('  <component name="ModelInterfacing"> \n') ;
xmlCode = [xmlCode initialise] ;
timeDuplicateA = sprintf ('    <variable cmeta:id="ModelInterfacing_timeDuplicate" name="timeDuplicate" units="millisecond"/> \n') ;
xmlCode = [xmlCode timeDuplicateA] ;
timeDuplicateB = sprintf ('    <variable name="time" public_interface="in" units="millisecond"/> \n\n') ;
xmlCode = [xmlCode timeDuplicateB] ;

for i = 1 : neuronCount
f = [ ...
'    <variable name="V%d" public_interface="in" units="millivolt"/>\n' ...
'    <variable cmeta:id="ModelInterfacing_V%dDuplicate" name="V%dDuplicate" units="millivolt"/> \n	\n' ...
    ] ;
    sessionComponent = sprintf (f, i,i,i) ;
    xmlCode = [xmlCode sessionComponent] ;
end

% Adding math for above component
xmlCode = [xmlCode initialMath] ;
timeDuplicateMath = sprintf(	'    <apply><eq/><ci>timeDuplicate</ci><ci>time</ci></apply> \n\n') ;
xmlCode = [xmlCode timeDuplicateMath] ;

for  i = 1 : neuronCount
    sessionMath = sprintf ('    <apply><eq/><ci>V%dDuplicate</ci><ci>V%d</ci></apply> \n\n', i,i) ;
    xmlCode = [xmlCode sessionMath] ;
end

xmlCode = [xmlCode ending] ;

f = [ ...
'  <connection> \n' ...
'    <map_components component_1="single_neuron_model1" component_2="ModelInterfacing"/> \n' ...
'    <map_variables variable_1="time" variable_2="time"/> \n' ...
'  </connection> \n\n' ...
] ;
timeConnection = sprintf (f , i,i,i) ;
xmlCode = [xmlCode timeConnection] ;


% Adding connections for session file creation
for i = 1 : neuronCount
f = [ ...    
'  <connection> \n' ...
'    <map_components component_1="single_neuron_model%d" component_2="ModelInterfacing"/> \n' ...
'    <map_variables variable_1="V" variable_2="V%d"/> \n' ...
' </connection> \n\n' ...
] ;
    sessionConnections = sprintf (f, i,i) ;
    xmlCode = [xmlCode sessionConnections] ;
end

xmlCode = [xmlCode '</model>'] ;

% Create XML file
myfid = fopen ('buteraModelXML.cellml','w') ;

% Write code to file
fprintf (myfid, '%s', xmlCode) ;

% Close file
fclose(myfid) ;

