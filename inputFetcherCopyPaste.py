import nuke
import nukescripts
import inputFetcherConfig
import inputFetcherUtils


def validateFetchInput(node):
    inputPrefix = 'IN_'
    label = node['label'].getValue()[:3]
    if inputPrefix in label and node['inputFetcherId']:
        return True


def validateFetchOutput(node):
    try:
        if node['label'].getValue().startswith('OUT_') and node['inputFetcherId']:
            return True
    except NameError:
        return False

def findFetcherOutputFrom(id, selfName):
    for node in nuke.allNodes(inputFetcherConfig._NODE_CLASS):
        if validateFetchOutput(node) and node.name() != selfName:
            tmpId = inputFetcherUtils.InputFetcherUtils().get_fetcher_id(node)
            if tmpId == id:
                return node

def convertToInput(node):
    label = node['label'].getValue().replace('OUT_', 'IN_')
    node['label'].setValue(label)

def outputExists(inputNode):
    for node in nuke.allNodes(inputFetcherConfig._NODE_CLASS):
        try:
            if inputNode['inputFetcherId'].getValue() == node['inputFetcherId'].getValue() and validateFetchOutput(node) and validateFetchInput(inputNode) or validateFetchOutput(inputNode):
                return True
        except NameError:
            pass
    return False

def hasDuplicateOutput(output):
    for node in nuke.allNodes(inputFetcherConfig._NODE_CLASS):
        try:
            if output['inputFetcherId'].getValue() == node['inputFetcherId'].getValue() and validateFetchOutput(node) and node != output:
                return True
        except NameError:
            pass
    return False

def createOutputFromInput(input_node):
    node_class_obj = getattr(nuke.nodes, inputFetcherConfig._NODE_CLASS)
    output = node_class_obj(label = input_node['label'].getValue().replace('IN_', 'OUT_'), note_font_size = 45, note_font = 'Bold')
    knob = nuke.String_Knob('inputFetcherId')
    output.addKnob(knob)
    output['inputFetcherId'].setValue(input_node['inputFetcherId'].getValue())
    output['inputFetcherId'].setEnabled(False)
    output['tile_color'].setValue(int(input_node['tile_color'].getValue()))
    output['note_font_color'].setValue(int(input_node['tile_color'].getValue()))
    inputFetcherUtils.InputFetcherUtils().label_as_name(output)
    for knob in output.knobs():
        if knob != 'inputFetcherId':
            output[knob].setVisible(False)
    xPos = input_node['xpos'].getValue()
    yPos = input_node['ypos'].getValue()
    output['xpos'].setValue(xPos)
    output['ypos'].setValue(yPos - 200)

def appendParentName():
    parent = nuke.text_knob(nuke.thisNode().name())
    nuke.thisNode().addKnob(parent)

def rsCopy():
    if not nuke.selectedNodes():
        return False
    nuke.nodeCopy('%clipboard%')
    for node in nuke.selectedNodes(inputFetcherConfig._NODE_CLASS):
        if validateFetchInput(node):
            id = inputFetcherUtils.InputFetcherUtils().get_fetcher_id(node)
            targetNode = findFetcherOutputFrom(id, node.name())
            inputFetcherUtils.InputFetcherUtils().connect_input(node, targetNode)

def hideFetcherKnobs(node):
    for knob in node.knobs():
        if knob != 'inputFetcherId':
            node[knob].setVisible(False)

def fetcher_is_tagged(node):
    for knob in node.knobs():
        if knob == 'inputFetcherSuffix' or knob == 'inputFetcherTag':
            return True
    return False

def untag_fetcher(node):
    try:
        node.removeKnob(node.knob('inputFetcherSuffix'))
        node.removeKnob(node.knob('inputFetcherTag'))
    except ValueError:
        pass

def rsPaste():
    nuke.nodePaste('%clipboard%')
    for node in nuke.selectedNodes(inputFetcherConfig._NODE_CLASS):
        if hasDuplicateOutput(node):
            convertToInput(node)
        if validateFetchInput(node) and not outputExists(node):
            createOutputFromInput(node)
        if validateFetchInput(node):
            id = inputFetcherUtils.InputFetcherUtils().get_fetcher_id(node)
            targetNode = findFetcherOutputFrom(id, node.name())
            inputFetcherUtils.InputFetcherUtils().connect_input(node, targetNode)
        hideFetcherKnobs(node)
    for node in nuke.selectedNodes():
        if fetcher_is_tagged(node):
            untag_fetcher(node)


nuke.menu('Nuke').addCommand('Edit/Input_Fetcher_Copy', rsCopy, 'ctrl+c')
nuke.menu('Nuke').addCommand('Edit/Input_Fetcher_Paste', rsPaste, 'ctrl+v')