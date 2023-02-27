import nukescripts


def validateFetchInput(node):
    inputPrefix = 'IN_'
    label = node['label'].getValue()[:3]
    if inputPrefix in label:
        return True


def validateFetchOutput(node):
    inputPrefix = 'OUT_'
    label = node['label'].getValue()[:4]
    if inputPrefix in label:
        return True


def findFetcherOutput(suffix):
    n = nuke.allNodes('Dot')
    for node in n:
        if validateFetchOutput(node):
            labelSuffix = node['label'].getValue()[4:]
            if labelSuffix == suffix:
                return node


def connectFetchInput(node, targetNode):
    node.setInput(0, targetNode)


def rsCopy():
    if not nuke.selectedNodes():
        return False
    nuke.nodeCopy('%clipboard3%')
    for node in nuke.selectedNodes('Dot'):
        if validateFetchInput(node):
            suffix = node['label'].getValue()[3:]
            targetNode = findFetcherOutput(suffix)
            connectFetchInput(node, targetNode)


def rsPaste():
    print('oh hi')
    nuke.nodePaste('%clipboard3%')
    for node in nuke.selectedNodes('Dot'):
        if validateFetchInput(node):
            suffix = node['label'].getValue()[3:]
            targetNode = findFetcherOutput(suffix)
            connectFetchInput(node, targetNode)


nuke.menu('Nuke').addCommand('Edit/rsCopy', rsCopy, 'ctrl+c')
nuke.menu('Nuke').addCommand('Edit/rsPaste', rsPaste, 'ctrl+v')
