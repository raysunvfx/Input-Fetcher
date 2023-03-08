import nuke
import nukescripts


def validateFetchInput(node):
    inputPrefix = 'IN_'
    label = node['label'].getValue()[:3]
    if inputPrefix in label:
        return True


def validateFetchOutput(node):
    try:
        if node['label'].getValue().startswith('OUT_') and node['id']:
            return True
    except NameError:
        return False

def getFetcherId(node):
    return node['id'].getValue()

def findFetcherOutputFrom(id, selfName):
    for node in nuke.allNodes('Dot'):
        if validateFetchOutput(node) and node.name() != selfName:
            tmpId = getFetcherId(node)
            if tmpId == id:
                return node

def convertToInput(node):
    label = node['label'].getValue().replace('OUT_', 'IN_')
    node['label'].setValue(label)

def appendParentName():
    parent = nuke.text_knob(nuke.thisNode().name())
    nuke.thisNode().addKnob(parent)

def connectFetchInput(node, targetNode):
    node.setInput(0, targetNode)

def hideFetchInput(node):
    node['hide_input'].setValue(True)

def rsCopy():
    if not nuke.selectedNodes():
        return False
    nuke.nodeCopy('%clipboard%')
    for node in nuke.selectedNodes('Dot'):
        if validateFetchInput(node):
            print('got here')
            id = getFetcherId(node)
            targetNode = findFetcherOutputFrom(id, node.name())
            connectFetchInput(node, targetNode)


def rsPaste():
    nuke.nodePaste('%clipboard%')
    for node in nuke.selectedNodes('Dot'):
        if validateFetchOutput(node):
            convertToInput(node)
    for node in nuke.selectedNodes('Dot'):
        if validateFetchInput(node):
            id = getFetcherId(node)
            targetNode = findFetcherOutputFrom(id, node.name())
            print(targetNode.name())
            connectFetchInput(node, targetNode)
            hideFetchInput(node)



nuke.menu('Nuke').addCommand('Edit/rsCopy', rsCopy, 'ctrl+c')
nuke.menu('Nuke').addCommand('Edit/rsPaste', rsPaste, 'ctrl+v')

