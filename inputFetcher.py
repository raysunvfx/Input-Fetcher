from PySide2 import QtWidgets, QtCore, QtGui
import uuid
import nuke


class InputFetcher(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        # Config input/output node class
        self.nodeClass = "Dot"

        # Config window defaults
        self.setWindowTitle('Input Fetcher')
        self.resize(500, 100)

        # Config font defaults;
        self.masterFont = 'Times'

        # Config search variables
        self.outputPrefix = 'OUT'
        self.inputPrefix = 'IN'
        self.separator = '_'
        self.tagKnob = 'inputFetcherTag'

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
            'PLATE': '#F5F5DC',
            'MATTE': '#3CB371',
            'RENDER': '#66FF66',
            'DEEP': '#00BFFF',
            'CAM': "#FA8072",
            'GEO': '#FFA500',
        }

        # Config commands
        self.commands = ['TAG', 'UNTAG']
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
        self.warningLabel = QtWidgets.QLabel('')
        self.warningLabel.setFont(QtGui.QFont(self.masterFont, 15, QtGui.QFont.Bold))
        self.warningLabel.setStyleSheet('color : yellow')

        # Config divider
        self.labelDivider = QtWidgets.QFrame()
        self.labelDivider.setFrameShape(QtWidgets.QFrame.HLine)
        self.labelDivider.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainLayout.addWidget(self.labellerLabel)
        self.mainLayout.addWidget(self.warningLabel)
        self.mainLayout.addWidget(self.labeller)
        self.mainLayout.addWidget(self.labelDivider)

    def is_duplicate_label(self, label):
        return label in [item['label'] for item in self.outputInfo]

    def has_valid_id(self, node):
        return 'id' in node.knobs()


    def is_valid_output(self, node):
        try:
            label = node['label'].getValue()
            has_valid_id = self.has_valid_id(node)
            has_valid_label = label.startswith(self.outputPrefix + self.separator) and label.count(self.separator) >= 2
            return has_valid_id and has_valid_label
        except NameError:
            return False

    def is_valid_input(self, node):
        try:
            label = node['label'].getValue()
            return node['id'] and label.startswith(self.inputPrefix + self.separator) and label.count(self.separator) >= 2
        except NameError:
            return False

    def getFetcherLabel(self, node):
        return node['label'].getValue().upper()


    def getFetcherId(self, node):
        return node['id'].getValue()

    def getFetcherPrefix(self, node):
        if self.is_valid_input(node) or self.is_valid_output(node):
            return node['label'].getValue().split('_')[1]

    def makeDict(self, name, ident, label):
        return(
                {"name" : name,
                 "id" : ident,
                "label" : label}
               )


    def collectOutputs(self):
        for node in nuke.allNodes(self.nodeClass):
            if self.is_valid_output(node):
                    self.outputLabels.append(self.getFetcherLabel(node))
                    self.outputNodes.append(node)
                    self.outputInfo.append(self.makeDict(node.name(), self.getFetcherId(node), self.getFetcherLabel(node)))


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
                                    'label' : '_'.join(item['label'].split(self.separator)[2:]).upper(),
                                    'id' : item['id'],
                                    }
                                    )
            setattr(self, 'group{}'.format(curPrefix.capitalize()), tmpList)
            # reset tmpList before new loop begins
            tmpList = []

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


    def setMainLayout(self):
        self.setLayout(self.mainLayout)

    def convertHexColor(self, color):
        format = '0x_ff'
        return int(format.replace('_', color[1:]), 16)

    def colorNodeByPrefix(self, node, prefix):
        try:
            color = self.convertHexColor(self.prefixColor.get(prefix))
            node['tile_color'].setValue(color)
            node['note_font_color'].setValue(color)
        except:
            node['tile_color'].setValue(0)
            node['note_font_color'].setValue(0)

    def updateId(self, node, newId):
        try:
            if node['id'].getValue() != newId:
                node['id'].setValue(newId)
        except NameError:
            return False

    def updateLabel(self, node, newLabel):
        try:
            if node['label'].getValue() != newLabel:
                node['label'].setValue(newLabel)
        except NameError:
            return False

    def reset_labeller_state(self):
        QtCore.QTimer.singleShot(0, self.labeller.setFocus)
        self.labeller.selectAll()

    def eventButtonClicked(self):
        if self.output_in_selection():
            self.warningLabel.setText("SORRY, CAN'T CONVERT AN OUTPUT INTO AN INPUT.  \nPLEASE DESELECT ANY OUTPUT NODES!")
            self.reset_labeller_state()
            return False

        buttonId = [item['id'] for item in self.outputInfo if item['id'] == self.sender().objectName()][0]
        buttonLabel = [item['label'] for item in self.outputInfo if item['id'] == self.sender().objectName()][0]
        parent = self.getParentFromId(buttonId)

        if nuke.selectedNodes():
            for node in nuke.selectedNodes():
                if self.is_valid_input(node) and self.getFetcherId(node) != buttonId:
                    self.updateId(node, buttonId)
                    self.updateLabel(node, self.convertLabelToInput(buttonLabel))
                    self.connectInput(node, parent)
                    self.colorNodeByPrefix(node, self.getFetcherPrefix(node))
                elif node.Class() == 'Dot':
                    self.convert_default_node_to_input(node, buttonLabel,buttonId, parent)
            self.close()
            return True

        fetchNode = self.createFetchNode(self.convertLabelToInput(buttonLabel), buttonId)
        self.connectInput(fetchNode, parent)
        self.close()
        return True


    def connectInput(self, node, targetNode):
        node.setInput(0, targetNode)
        node['hide_input'].setValue(True)

    def set_label(self, node, label_text):
        font_size = 100 if node.Class() == 'BackdropNode' else 45
        node['note_font_size'].setValue(font_size)
        node['label'].setValue(label_text)
        node['note_font'].setValue('Bold')

    def updateOuputAndChildren(self, ident, label):
        for item in self.outputInfo:
            if item['id'] == ident:
                parent = nuke.toNode(item['name'])
                prefix = label.split(self.separator)[1]
                if self.is_valid_output(parent):
                    self.set_label(parent, label)
                    self.colorNodeByPrefix(parent, prefix)
                for node in nuke.allNodes(self.nodeClass):
                    if self.is_valid_input(node) and node['id'].getValue() == ident:
                        self.set_label(node, label.replace(self.outputPrefix + self.separator, self.inputPrefix + self.separator))
                        self.colorNodeByPrefix(node, prefix)

    def output_in_selection(self):
        try:
            if nuke.selectedNodes(self.nodeClass):
                for node in nuke.selectedNodes():
                    if self.is_valid_output(node):
                        raise StopIteration
        except StopIteration:
            return True
        else:
            return False

    def multiple_outputs_selected(self, nodes):
        outputCounter = 0
        for node in nodes:
            if self.is_valid_output(node):
                outputCounter += 1
        if outputCounter > 1:
            return True
        return False

    def input_nodes_selected(self, nodes):
        foundInput = False
        foundOutput = False
        for node in nodes:
            if self.is_valid_input(node):
                foundInput = True
                break
        for node in nodes:
            if self.is_valid_output(node):
                foundOutput = True
                break
        if foundOutput:
            return False
        else:
            return foundInput

    def inputIsCommand(self, input):
        return input in self.commands

    def multiple_default_node_selected(self, nodes):
        default_node_counter = 0
        try:
            for node in nodes:
                if node.Class() == self.nodeClass and not self.is_valid_output(node) and not self.is_valid_input(node):
                    default_node_counter += 1
                if default_node_counter == 2:
                    raise StopIteration
        except StopIteration:
            return True
        return False


    def labelNode(self):
        input = self.labeller.text().upper()
        n = nuke.selectedNodes()

        if not n:
            # print("\nFailed at {}.".format(inputFetcher.setLabel.__name__)) this prints the name of the function
            self.createFetchNode(input)
            self.close()

        if self.is_duplicate_label(input):
            self.warningLabel.setText(input + ' already exists.  Please enter a different name.')
            self.reset_labeller_state()
            return

        if self.multiple_outputs_selected(n):
            self.warningLabel.setText("CAN'T RENAME MULTIPLE OUTPUTS AT THE SAME TIME.  RENAME ONE AT A TIME PLEASE!")
            self.reset_labeller_state()
            return

        if self.multiple_default_node_selected(n) and self.validateLabelFormat(input):
            self.warningLabel.setText("CAN'T CREATE MORE THAN ONE OUTPUT AT THE SAME TIME!\nMULTIPLE {} NODES SELECTED!".format(self.nodeClass.upper()))
            self.reset_labeller_state()
            return

        if self.input_nodes_selected(n):
            self.warningLabel.setText("CAN'T RENAME INPUT NODES.")
            self.reset_labeller_state()
            return

        if len(n) == 1 and nuke.selectedNode().Class() == 'BackdropNode':
            self.set_label(nuke.selectedNode(), input)
            self.close()
            return

        if len(n) == 1 and self.is_valid_output(nuke.selectedNode()) and self.validateLabelFormat(input):
            self.updateOuputAndChildren(self.getFetcherId(nuke.selectedNode()), input.upper())
            self.close()
            return

        if len(n) == 1 and not self.is_valid_output(nuke.selectedNode()) and self.validateLabelFormat(input) and nuke.selectedNode().Class() == 'Dot':
            self.createFetchNode(input, node=nuke.selectedNode())
            self.close()
            return

        for node in n:
            if self.inputIsCommand(input):
                cmd = getattr(self, input.lower())
                cmd(nuke.toNode(node.name()))
            if not self.is_valid_input(node):
                if input not in self.commands:
                    if self.is_valid_output(node):
                        self.warningLabel.setText("TRYING TO RENAME AN OUTPUT NODE WITH AN INVALID LABEL.  SYNTAX = OUT_PREFIX_LABEL")
                        self.reset_labeller_state()
                        return False
                    elif not input.startswith(self.outputPrefix + self.separator):
                        self.set_label(node, input)
                    elif input.startswith(self.outputPrefix + self.separator):
                        if node.Class() == self.nodeClass:
                            self.createFetchNode(input, node=node)
                self.close()

    def tag(self, node):
        if not node.knob(self.tagKnob):
            knob = nuke.Boolean_Knob(self.tagKnob, self.tagKnob, 1)
            node.addKnob(knob)
            knob.setVisible(False)
            node.knob(0).setFlag(0)

    def findTaggedNodes(self):
        for node in nuke.allNodes():
            if node.knob(self.tagKnob):
                self.taggedNodes.append(node)


    def convertLabelToInput(self, label):
        return label.replace(self.outputPrefix + self.separator, self.inputPrefix + self.separator)

    def assign_id(self, node, ident=''):
        if not ident:
            id = uuid.uuid4().hex[:16]
            knob = nuke.String_Knob('id')
            node.addKnob(knob)
            node['id'].setValue(id)
        else:
            knob = nuke.String_Knob('id')
            node.addKnob(knob)
            node['id'].setValue(ident)
        node['id'].setFlag(0x0000000000000080)


    def getParentFromId(self, id):
        for node in nuke.allNodes('Dot'):
            if self.is_valid_output(node) and node['id'].getValue() == id:
                return node

    def interface2rgb(self, hexValue):
        return [(0xFF & hexValue >> i) / 255.0 for i in [24, 16, 8]]

    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def invert_rgb(self, rgb):
        return [1 - rgb[0], 1 - rgb[1], 1 - rgb[2]]

    def calc_rgb_luminance(self, rgb):
        luminance = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
        print(luminance)
        return luminance

    def layoutTaggedNodes(self):
        if self.taggedNodes:
            labelFont = QtGui.QFont(self.masterFont, 15, QtGui.QFont.Bold)
            buttonFont = QtGui.QFont('PMingLiU-ExtB', 10, QtGui.QFont.Bold)

            label = QtWidgets.QLabel('TAGGED')
            label.setFont(labelFont)

            buttonsLayout = setattr(self, '{}ButtonsLayout'.format('tagged'), QtWidgets.QHBoxLayout())
            buttonsLayoutRef = getattr(self, '{}ButtonsLayout'.format('tagged'))

            for node in self.taggedNodes:
                name = node.name()
                node_default_color = nuke.defaultNodeColor(node.Class())
                node_default_rgb_color = self.interface2rgb(node_default_color)
                if self.calc_rgb_luminance(node_default_rgb_color) < .5:
                    text_color = 'white'
                else:
                    text_color = 'black'
                node_default_hex_code = self.rgb_to_hex(node_default_rgb_color)
                button = QtWidgets.QPushButton(name)
                button.setStyleSheet("background-color : {}; color : {}".format(node_default_hex_code, text_color))
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
        self.untag(nuke.selectedNode())

        self.close()

    def untag(self, node):
        if node.knob(self.tagKnob):
            for x in range(node.numKnobs()):
                knob = node.knob(x)
                if knob.name() == self.tagKnob:
                    node.removeKnob(knob)

    def clearSelection(self):
        allNodes = nuke.allNodes()
        for node in allNodes:
            node.setSelected(False)

    def resetLayout(self, layout):
        self.resize(500, 100)
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

    def validateLabelFormat(self, label):
        return label.count(self.separator) >= 2

    def get_prefix_from_label(self, label):
        return label.split(self.separator)[1]

    def convert_default_node_to_input(self, node, label, ident, parent):
        self.set_label(node, self.convertLabelToInput(label))
        self.assign_id(node, ident)
        self.colorNodeByPrefix(node, self.get_prefix_from_label(label))
        self.connectInput(node, parent)

    def hide_fetcher_knobs(self, node):
        for knob in node.knobs():
            if knob != 'id':
                node[knob].setVisible(False)


    def createFetchNode(self, label, ident=None, node=None, parent=None):
        if not node:
            fetchNode = nuke.createNode(self.nodeClass)
            self.set_label(fetchNode, label)
        else:
            fetchNode = node

        self.set_label(fetchNode, label)
        self.hide_fetcher_knobs(fetchNode)
        try:
            prefix = label.split(self.separator)[1].upper()
            self.colorNodeByPrefix(fetchNode, prefix)
        except IndexError:
            return False
        if self.validateLabelFormat(label):
            try:
                if fetchNode['id']:
                    pass
            except NameError:
                self.assign_id(fetchNode, ident)
        return fetchNode

    def goFetch(self):
        self.resetLayout(self.mainLayout)
        self.setModal(True)
        self.collectOutputs()
        self.initLayout()
        self.show()
        self.groupOutputs()
        self.findUniquePrefixes()
        self.sortUniquePrefixes()
        self.findTaggedNodes()
        self.layoutTaggedNodes()
        self.createButtonsFromLabels()

        self.setMainLayout()


inputFetcher = InputFetcher()
nuke.menu('Nuke').addCommand('Edit/Input Fetcher', inputFetcher.goFetch, 'shift+n')

