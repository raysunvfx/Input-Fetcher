from PySide2 import QtWidgets, QtCore, QtGui
import uuid
import time
import nuke


class inputFetcher(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        # Config input/output node class
        self.nodeClass = "Dot"

        # Config window defaults
        self.setWindowTitle('Input Fetcher')
        self.resize(500, 500)

        # Config font defaults;
        self.masterFont = 'Times'

        # Config search variables
        self.outputPrefix = 'OUT'
        self.inputPrefix = 'IN'
        self.separator = '_'
        self.tag = 'inputFetcherTag'

        # Config label variables
        self.prefixDefaults = ['PLATE', 'MATTE', 'RENDER', 'DEEP', 'CAM', 'GEO']
        self.outputLabels = []
        self.cleanedLabels = []
        self.uniquePrefixList = []
        self.outputNodes = []
        # Prepare a dict with LABEL + ID // Reset each instance
        self.outputInfo = []

        # Config tagged nodes
        self.taggedNodes = []

        # Config group prefixes and colors
        self.prefixColor = {
            'PLATE': 'beige',
            'MATTE': 'mediumseagreen',
            'RENDER': 'chartreuse',
            'DEEP': 'deepskyblue',
            'GEO': 'orange',
            'CAM': "\#fa8072",
        }

        # Config layout
        self.mainLayout = QtWidgets.QVBoxLayout()

    def initLayout(self):
        # Config labeller
        placeHolderText = 'Ex. OUT_MATTE_CHARACTER01'
        if len(nuke.selectedNodes()) == 1:
            n = nuke.selectedNode()
            placeHolderText = n['label'].getValue()
        self.labeller = QtWidgets.QLineEdit(placeHolderText)
        self.labeller.setPlaceholderText("Enter a command or label ... ")
        self.labeller.returnPressed.connect(self.labelNode)
        self.labeller.selectAll()
        QtCore.QTimer.singleShot(0, self.labeller.setFocus)
        self.labellerLabel = QtWidgets.QLabel('ENTER LABEL:')
        self.labellerLabel.setFont(QtGui.QFont(self.masterFont, 15, QtGui.QFont.Bold))

        # Config divider
        self.labelDivider = QtWidgets.QFrame()
        self.labelDivider.setFrameShape(QtWidgets.QFrame.HLine)
        self.labelDivider.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainLayout.addWidget(self.labellerLabel)
        self.mainLayout.addWidget(self.labeller)
        self.mainLayout.addWidget(self.labelDivider)


    def isValidOutput(self, node):
        return node['id'] and node['label'].getValue().startswith(self.outputPrefix + self.separator)


    def getOutputLabel(self, node):
        return node['label'].getValue().upper()


    def getOutputId(selfself, node):
        return node['id'].getValue().upper()


    def makeDict(self, name, ident, label):
        return(
                {"name" : name,
                 "id" : ident,
                "label" : label}
               )


    def getCatagory(self, label):
        return label.split('_')[1]


    def collectOutputs(self):
        for node in nuke.allNodes(self.nodeClass):
            try:
                if self.isValidOutput(node):
                        self.outputLabels.append(self.getOutputLabel(node))
                        self.outputNodes.append(node)
                        self.outputInfo.append(self.makeDict(node.name(), node['id'].getValue(), node['label'].getValue()))
            except NameError:
                return False


    # def cleanOutputLabels(self):
    #     # Remove 'OUT_' prefix from labels
    #     # Example: OUT_MATTE_CHARACTER --> MATTE_CHARACTER
    #     for l in self.outputLabels:
    #         self.cleanedLabels.append(l.replace(self.outputPrefix + self.separator, ""))
    #     self.cleanedLabels = sorted(self.cleanedLabels)

    def findUniquePrefixes(self):
        # EXAMPLE: MATTE_CHARACTER --> MATTE
        for item in self.outputInfo:
            prefix = item['label'].replace(self.outputPrefix + self.separator, "").split(self.separator)[0]
            if prefix not in self.uniquePrefixList:
                self.uniquePrefixList.append(prefix)


    def sortUniquePrefixes(self):
        # get all unique prefixes
        origList = self.uniquePrefixList
        # get all deafult prefixes
        defaultList = self.prefixDefaults

        # remove default prefixes that aren't in current script
        # we end up with a new default prefix list in proper order
        for label in defaultList:
            defaultList = [i for i in defaultList if i in origList]

        # remove valid default prefixes from current script's prefix list
        for label in origList:
            origList = [i for i in origList if i not in defaultList]

        # join the two lists together which will have the correct default prefix ordering
        defaultList += origList
        # update uniquePrefixList with new defaultList
        self.uniquePrefixList = defaultList


#self.cleanedLabels no longer exists, will need to update below code to work with the self.outputInfo dict format
    def groupOutputs(self):
        tmpList = []
        # first loop to find first prefix
        for item in self.outputInfo:
            curPrefix = item['label'].split(self.separator)[1]
            for item in self.outputInfo:
                lookupPrefix = item['label'].split(self.separator)[1]
                if lookupPrefix == curPrefix:
                    tmpList.append(
                                    {
                                    'label' : item['label'].split(self.separator)[2].capitalize(),
                                    'id' : item['id'],
                                    }
                                    )
            setattr(self, 'group{}'.format(curPrefix.capitalize()), tmpList)
        # for l in self.cleanedLabels:
        #     # set current prefix to work on
        #     curPrefix = l.split(self.separator)[0]
        #     # second loop to compare to curPrefix from first loop
        #     for k in self.cleanedLabels:
        #         lookupPrefix = k.split(self.separator)[0]
        #         if lookupPrefix == curPrefix:
        #             tmpList.append(k)
        #     dynamically create attribute based on curPrefix

            # reset tmpList before new loop begins
            tmpList = []

    # def markDuplicates(self):
    #     # look for any duplicated labels and mark them to warn the user
    #     duplicates = []
    #     for index, value in enumerate(self.cleanedLabels):
    #         if value == self.cleanedLabels[index - 1] and index > 0:
    #             duplicates.append(value)
    #     # for index, value in enumerate(self.cleanedLabels):
    #     #     if value in duplicates:
    #     #         self.cleanedLabels[index] = value + ' (DUPLICATE)'

    def createButtonsFromLabels(self):
        # config font
        labelFont = QtGui.QFont(self.masterFont, 15, QtGui.QFont.Bold)
        buttonFont = QtGui.QFont(self.masterFont, 10, QtGui.QFont.Bold)
        for p in self.uniquePrefixList:
            # config color by prefix
            color = self.prefixColor.get(p)
            x = getattr(self, 'group{}'.format(p.capitalize()))
            label = QtWidgets.QLabel(p)
            label.setFont(labelFont)
            label.setStyleSheet('color : {}'.format(color))
            labelDivider = QtWidgets.QFrame()
            labelDivider.setFrameShape(QtWidgets.QFrame.HLine)
            labelDivider.setFrameShadow(QtWidgets.QFrame.Sunken)
            # dynamically create QHBoxLayout for each label as class attribs
            labelLayout = setattr(self, '{}LabelLayout'.format(p.lower()), QtWidgets.QHBoxLayout())
            # reference newly created QHBoxLayout obj
            labelLayoutRef = getattr(self, '{}LabelLayout'.format(p.lower()))

            labelLayoutRef.addWidget(label)
            # dynamically create QHBoxLayout for each button as class attribs
            buttonsLayout = setattr(self, '{}ButtonsLayout'.format(p.lower()), QtWidgets.QHBoxLayout())
            # reference newly created QHBoxLayout obj
            buttonsLayoutRef = getattr(self, '{}ButtonsLayout'.format(p.lower()))

            for l in x:
                #label = self.createButtonLabels(l)
                # switch from label to l to make it work again!
                button = QtWidgets.QPushButton(l['label'])
                button.setObjectName(l['id'])
                button.setStyleSheet("color : {}".format(color))
                button.setFont(buttonFont)
                button.clicked.connect(self.eventButtonClicked)
                buttonsLayoutRef.addWidget(button)
            buttonsLayoutRef.addStretch()
            self.mainLayout.addLayout(labelLayoutRef)
            self.mainLayout.addWidget(labelDivider)
            self.mainLayout.addLayout(buttonsLayoutRef)
            self.mainLayout.addStretch()

    # def createButtonLabels(self, origLabel):
    #     # this doesn't work, beacuse when we click the button the sender's name does not include the prefix of the output, and fails to find it .. think of another way to hide the prefixes on the labels!
    #     # skipping this func for now, until i can rework this tool to search via ID
    #     label = ''
    #     elements = origLabel.split('_')
    #     if elements > 0 and elements[0] in self.uniquePrefixList:
    #         label = origLabel.replace(elements[0] + self.separator, '')
    #         return label

    def setMainLayout(self):
        self.setLayout(self.mainLayout)

    def eventButtonClicked(self):
        senderName = self.sender().objectName()
        # if '(DUPLICATE)' in senderName:
        #     QtWidgets.QMessageBox.warning(self, 'UH-OH!', (
        #         "Multiple OUT_{0} found, and I couldn't figure out which one you wanted!\n\nPlease remove the duplicates!").format(
        #         senderName.split(' ')[0]))
        #     return False
        for item in self.outputInfo:
            if item['id'] == self.sender().objectName():
                self.createFetchNode(self.convertLabelToInput(item['label']), item['id'])

        # l = []
        # if not nuke.selectedNodes():
        #     n = self.createFetchNode(self.inputPrefix + self.separator + senderName)
        #     # n = nuke.createNode(self.nodeClass)
        #     # n['label'].setValue()
        #     l.append(n)
        # else:
        #     for node in nuke.selectedNodes():
        #         if not node['label'].getValue()[:4] == self.outputPrefix + self.separator:
        #             l.append(node)
        #         else:
        #             QtWidgets.QMessageBox.warning(self, 'UH-OH!',
        #                                           "Sorry, one or more nodes you selected are OUTPUTs!\n\nI'm not allowed to overwrite an OUTPUT with an INPUT!")
        #             return False
        #
        # for x in l:
        #     for node in self.outputNodes:
        #         outputLabel = self.outputPrefix + self.separator + senderName
        #         inputLabel = self.inputPrefix + self.separator + senderName
        #         if node['label'].getValue() == outputLabel:
        #             if x.Class() == self.nodeClass:
        #                 self.connectInput(x, node)
        #                 self.setLabel(x, inputLabel)
        #                 # why did i want to set name to empty string???
        #                 # self.setEmptyLabel(x)
        #                 self.close()

    # def findOutputNode(label, node):
    #     outputLabel = self.outputPrefix + self.separator + senderName
    #     inputLabel = self.inputPrefix + self.separator + senderName

    def connectInput(self, curNode, targetNode):
        curNode.setInput(0, targetNode)
        curNode['hide_input'].setValue(True)

    def setLabel(self, curNode, label_text):
        font_size = 45
        if curNode.Class() == 'BackdropNode':
            font_size = 100
        curNode['note_font_size'].setValue(font_size)
        curNode['label'].setValue(label_text)
        curNode['note_font'].setValue('Bold')

    def setEmptyLabel(self, node):
        node['name'].setValue('')

    def labelNode(self):
        input = self.labeller.text().upper()
        n = nuke.selectedNodes()
        if not n:
            # print("\nFailed at {}.".format(inputFetcher.setLabel.__name__)) this prints the name of the function
            self.createFetchNode(input)
            self.close()

        for node in n:  #
            if not input == 'TAG' and not input == 'UNTAG':
                self.setLabel(node, input)
            else:
                if input == 'TAG':
                    self.tagNode(node)
                if input == 'UNTAG':
                    self.untagNode(node)
            self.close()

    def tagNode(self, node):  #
        if not node.knob(self.tag):
            knob = nuke.Boolean_Knob(self.tag, self.tag, 1)
            node.addKnob(knob)
            knob.setVisible(False)
            node.knob(0).setFlag(0)

    def findTaggedNodes(self):
        for node in nuke.allNodes():
            if node.knob(self.tag):
                self.taggedNodes.append(node)


    def convertLabelToInput(self, label):
        return label.replace(self.outputPrefix + self.separator, self.inputPrefix + self.separator)

    def convertToInput(self, node):
        label = node['label'].getValue().replace(self.outputPrefix, self.inputPrefix)
        node['label'].setValue(label)

    def isOutput(self, node):
        if node['label'].getValue()[:4] == self.outputPrefix + self.separator:
            print('output node yes')
            return True

#     def addOnCreateCommand(self, node):
         #removed because this runs when script loads, and will turn all OUT_ to IN_, which sucks.
         #functionality moved to rsCopyPaste instead
#         command = """
# mySelf = nuke.thisNode()
# myId = inputFetcher.fetchId(mySelf)
# parent = inputFetcher.getParentFromId(myId)
# print(parent)
#
# if parent:
#     inputFetcher.convertToInput(mySelf)
#     #inputFetcher.connectInput(nuke.thisNode(), parent)
#     #mySelf.setInput(0, nuke.toNode(parent))
#
#
#
#         """
#         node['onCreate'].setValue(command)

    def assignId(self, node, id=''):
        if not id:
            id = uuid.uuid4().hex[:16]
            knob = nuke.String_Knob('id')
            node.addKnob(knob)
            node['id'].setValue(id)
        else:
            knob = nuke.String_Knob('id')
            node.addKnob(knob)
            node['id'].setValue(id)
        node['id'].setFlag(0x0000000000000080)


    def getParentFromId(self, id):
        result = []
        try:
            for node in nuke.allNodes('Dot'):
                targetId = node['id'].getValue()
                if id == targetId:
                    result.append(node.name())
        except NameError:
            pass
        return result[1]

    def fetchId(self, node):
        return node['id'].getValue()

    def layoutTaggedNodes(self):
        if self.taggedNodes:
            labelFont = QtGui.QFont(self.masterFont, 15, QtGui.QFont.Bold)
            buttonFont = QtGui.QFont(self.masterFont, 10, QtGui.QFont.Bold)

            label = QtWidgets.QLabel('TAGGED')
            label.setFont(labelFont)

            buttonsLayout = setattr(self, '{}ButtonsLayout'.format('tagged'), QtWidgets.QHBoxLayout())
            buttonsLayoutRef = getattr(self, '{}ButtonsLayout'.format('tagged'))

            for node in self.taggedNodes:
                name = node.name()
                button = QtWidgets.QPushButton(name)
                button.setStyleSheet("color : white")
                button.setFont(buttonFont)
                button.clicked.connect(self.taggedButton)
                buttonsLayoutRef.addWidget(button)
            buttonsLayoutRef.addStretch()

            labelDivider = QtWidgets.QFrame()
            labelDivider.setFrameShape(QtWidgets.QFrame.HLine)
            labelDivider.setFrameShadow(QtWidgets.QFrame.Sunken)

            self.mainLayout.addWidget(label)
            self.mainLayout.addWidget(labelDivider)
            self.mainLayout.addLayout(buttonsLayoutRef)

    def taggedButton(self):
        # get pressed button id and copy/paste the node
        senderName = self.sender().text()
        self.clearSelection()
        for node in nuke.allNodes():
            if senderName == node.name():
                node.setSelected(True)
        nuke.duplicateSelectedNodes()
        self.untagNode(nuke.selectedNode())

        self.close()

    def untagNode(self, node):
        if node.knob(self.tag):
            for x in range(node.numKnobs()):
                knob = node.knob(x)
                if knob.name() == self.tag:
                    node.removeKnob(knob)

    def clearSelection(self):
        allNodes = nuke.allNodes()
        for node in allNodes:
            node.setSelected(False)

    def resetLayout(self, layout):
        self.outputLabels = []
        self.cleanedLabels = []
        self.uniquePrefixList = []
        self.outputNodes = []
        self.outputInfo = []
        self.taggedNodes = []
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

                else:
                    self.resetLayout(item.layout())

    def createFetchNode(self, label, id=''):
        # rename this method to createFetchNode
        fetchNode = nuke.createNode(self.nodeClass)
        fetchNode['label'].setValue(label)
        fetchNode['note_font_size'].setValue(45)
        fetchNode['note_font'].setValue('Bold')
        self.assignId(fetchNode, id)
        #self.assignId(fetchNode)
        #self.addOnCreateCommand(fetchNode)

        return fetchNode

    def goFetch(self):
        self.resetLayout(self.mainLayout)
        self.initLayout()
        self.setModal(True)
        self.show()
        self.collectOutputs()
        #self.cleanOutputLabels()
        #self.markDuplicates()
        self.groupOutputs()
        self.findUniquePrefixes()
        self.sortUniquePrefixes()
        self.findTaggedNodes()
        self.layoutTaggedNodes()
        self.createButtonsFromLabels()

        self.setMainLayout()


inputFetcher = inputFetcher()
#inputFetcher.goFetch()
nuke.menu('Nuke').addCommand('Edit/Input Fetcher', inputFetcher.goFetch, 'shift+n')

# give all outputs a random id
# when copy pasting OUTPUT node, first check if there's an identical id on another node, if yes, this is a duplicate OUTPUT node, and should be converted to an INPUT node, if not, then check if there's another node with the same label, if yes, that means we're pasting into a different script, and we conver the OUTPUT to an INPUT and connect to the pre-existing OUTPUT node, if neither, then that means we're pasting into a new script without this OUTPUT, and leave it as is

# if label == self label, connect, then change self to input
# if self is input node:
# look for output by label and connect

# nuke oncreate is not working with setInput(), look into modifying the native copy/paste functions inside of nuke

#command: rename output, will rename selected output and all inputs