# make outer shell of elements use version 2 of d3 & add to nodes
from opencmiss.utils.zinc.general import ChangeManager
from opencmiss.utils.zinc.finiteelement import get_element_node_identifiers
from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field
from opencmiss.zinc.node import Node
from opencmiss.zinc.result import RESULT_OK


def remapEftNodeValueLabelsVersion(eft, localNodeIndexes, valueLabels, version):
    '''
    Remap all uses of the given valueLabels to use the version.
    :param localNodeIndexes:  List of local node indexes >= 1 to remap at.
    :param valueLabels:  List of node value labels to be remapped.
    :param version: Version >= 1
    '''
    functionCount = eft.getNumberOfFunctions()
    for f in range(1, functionCount + 1):
        termCount = eft.getFunctionNumberOfTerms(f)
        for t in range(1, termCount + 1):
            localNodeIndex = eft.getTermLocalNodeIndex(f, t)
            valueLabel = eft.getTermNodeValueLabel(f, t)
            if (localNodeIndex in localNodeIndexes) and (valueLabel in valueLabels):
                result = eft.setTermNodeParameter(f, t, localNodeIndex, valueLabel, version)
                #print('remap result', result)


context = Context('add_discontinuity')
logger = context.getLogger()
region = context.getDefaultRegion()
region.readFile('body_groups11.exf')
fieldmodule = region.getFieldmodule()
mesh = fieldmodule.findMeshByDimension(3)
group = fieldmodule.findFieldByName('non_core').castGroup()
elementGroup = group.getFieldElementGroup(mesh)
meshGroup = elementGroup.getMeshGroup()
print('meshGroup size', meshGroup.getSize())
nodes = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
coordinates = fieldmodule.findFieldByName('coordinates').castFiniteElement()
elementtemplate = mesh.createElementtemplate()
undefineNodetemplate = nodes.createNodetemplate()
undefineNodetemplate.undefineField(coordinates)
nodetemplate = nodes.createNodetemplate()
fieldcache = fieldmodule.createFieldcache()
with ChangeManager(fieldmodule):
    elementIter = meshGroup.createElementiterator()
    element = elementIter.next()
    localNodeIndexes = [1, 2, 3, 4]
    valueLabel = Node.VALUE_LABEL_D_DS3
    while element.isValid():
        print('Element', element.getIdentifier())
        eft = element.getElementfieldtemplate(coordinates, -1)
        nodeIds = get_element_node_identifiers(element, eft)
        for localNodeIndex in localNodeIndexes:
            node = element.getNode(eft, localNodeIndex)
            print('    Node', node.getIdentifier())
            nodetemplate.defineFieldFromNode(coordinates, node)
            versionsCount = nodetemplate.getValueNumberOfVersions(coordinates, -1, valueLabel)
            if versionsCount == 1:
                fieldcache.setNode(node)
                result0,  x = coordinates.getNodeParameters(fieldcache, -1, Node.VALUE_LABEL_VALUE, 1, 3)
                result0, d1 = coordinates.getNodeParameters(fieldcache, -1, Node.VALUE_LABEL_D_DS1, 1, 3)
                result0, d2 = coordinates.getNodeParameters(fieldcache, -1, Node.VALUE_LABEL_D_DS2, 1, 3)
                result0, d3 = coordinates.getNodeParameters(fieldcache, -1, valueLabel, 1, 3)
                result1 = node.merge(undefineNodetemplate)
                result2 = nodetemplate.setValueNumberOfVersions(coordinates, -1, valueLabel, 2)
                result3 = node.merge(nodetemplate)
                result4 = coordinates.setNodeParameters(fieldcache, -1, Node.VALUE_LABEL_VALUE, 1,  x)
                result4 = coordinates.setNodeParameters(fieldcache, -1, Node.VALUE_LABEL_D_DS1, 1, d1)
                result4 = coordinates.setNodeParameters(fieldcache, -1, Node.VALUE_LABEL_D_DS2, 1, d2)
                result4 = coordinates.setNodeParameters(fieldcache, -1, valueLabel, 1, d3)
                result5 = coordinates.setNodeParameters(fieldcache, -1, valueLabel, 2, d3)
                #print('Results:', result0, result1, result2, result3, result4, result5)
                if result3 == 0:
                    loggerMessageCount = logger.getNumberOfMessages()
                    if loggerMessageCount > 0:
                        for i in range(1, loggerMessageCount + 1):
                            print(logger.getMessageTypeAtIndex(i), logger.getMessageTextAtIndex(i))
                        logger.removeAllMessages()
                        exit()
        remapEftNodeValueLabelsVersion(eft, localNodeIndexes, [ valueLabel ], 2)
        result1 = elementtemplate.defineField(coordinates, -1, eft)
        result2 = element.merge(elementtemplate)
        result3 = element.setNodesByIdentifier(eft, nodeIds)
        #print('Element merge result',result1, result2, result3)
        if (result1 != RESULT_OK) or (result2 != RESULT_OK):
            loggerMessageCount = logger.getNumberOfMessages()
            if loggerMessageCount > 0:
                for i in range(1, loggerMessageCount + 1):
                    print(logger.getMessageTypeAtIndex(i), logger.getMessageTextAtIndex(i))
                logger.removeAllMessages()
                exit()
        element = elementIter.next()
region.writeFile('body_groups_discontinuity11.exf')
