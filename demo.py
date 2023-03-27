set cut_paste_input [stack 0]
version 12.1 v2
BackdropNode {
 inputs 0
 name BackdropNode1
 tile_color 0x191919ff
 label PLATES
 note_font " Bold"
 note_font_size 100
 selected true
 xpos -1100
 ypos -1118
 bdwidth 2301
 bdheight 928
}
BackdropNode {
 inputs 0
 name BackdropNode10
 tile_color 0x717171ff
 note_font_size 42
 selected true
 xpos 9037
 ypos 7957
 bdwidth 2678
 bdheight 3280
}
BackdropNode {
 inputs 0
 name BackdropNode11
 tile_color 0x8e388e00
 note_font_size 42
 selected true
 xpos 5280
 ypos 11557
 bdwidth 1493
 bdheight 1513
}
BackdropNode {
 inputs 0
 name BackdropNode12
 tile_color 0x7171c600
 note_font_size 42
 selected true
 xpos 8399
 ypos 15199
 bdwidth 1790
 bdheight 1495
}
BackdropNode {
 inputs 0
 name BackdropNode17
 tile_color 0x8e8e3800
 note_font_size 42
 selected true
 xpos 6730
 ypos 20171
 bdwidth 1794
 bdheight 667
}
BackdropNode {
 inputs 0
 name BackdropNode18
 tile_color 0x4d4d4dff
 note_font_size 42
 selected true
 xpos 8693
 ypos 20177
 bdwidth 1955
 bdheight 660
}
BackdropNode {
 inputs 0
 name BackdropNode19
 onCreate nuke.thisNode().knob('init').execute()
 tile_color 0x71c67100
 label "INPUT FETCHER DEMO SCRIPT <1>"
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 7662
 ypos -7579
 bdwidth 3126
 bdheight 5933
 addUserKnob {20 User}
 addUserKnob {22 init T "from PySide2 import QtWidgets, QtCore, QtGui\nimport uuid\nimport nuke\nimport re\n\ninput_fetcher_prev_input = None\n\ndef zoomToParent():\n    try:\n        if len(nuke.selectedNodes()) == 1:\n            global input_fetcher_prev_input\n            if 'IN_' not in nuke.selectedNode()\['label'].getValue() and 'OUT_' not in nuke.selectedNode()\['label'].getValue():\n                input_fetcher_prev_input = None\n                return False\n            if input_fetcher_prev_input:\n                if nuke.selectedNode()\['inputFetcherId'].getValue() != input_fetcher_prev_input\['inputFetcherId'].getValue():\n                    input_fetcher_prev_input = None\n                    return False\n            if nuke.selectedNode()\['label'].getValue().startswith('IN_'):\n                global input_fetcher_prev_input\n                input_fetcher_prev_input = nuke.selectedNode()\n                ident = nuke.selectedNode()\['inputFetcherId'].getValue()\n                for node in nuke.selectedNodes():\n                    node.setSelected(False)\n                for node in nuke.allNodes('Dot'):\n                    if 'OUT_' in node\['label'].getValue() and node\['inputFetcherId'].getValue() ==ident:\n                        node.setSelected(True)\n                        nuke.zoom(.3, \[node\['xpos'].getValue(), node\['ypos'].getValue()])\n            else:\n                for node in nuke.selectedNodes():\n                    node.setSelected(False)\n                input_fetcher_prev_input.setSelected(True)\n                nuke.zoom(.3, \[input_fetcher_prev_input\['xpos'].getValue(), input_fetcher_prev_input\['ypos'].getValue()])\n                global input_fetcher_prev_input\n                input_fetcher_prev_input = None\n    except ValueError:\n            pass\n\nnuke.menu('Nuke').addCommand('Edit/Input Fetcher Zoom To Output', zoomToParent, 'a')\n\n\nclass InputFetcherUtils():\n    def label_as_name(self, node):\n        node\['autolabel'].setValue(\"nuke.thisNode()\['label'].getValue()\")\n\n    def connect_input(self, node, targetNode):\n        node.setInput(0, targetNode)\n        node\['hide_input'].setValue(True)\n\n    def get_fetcher_id(self, node):\n        return node\['inputFetcherId'].getValue()\n\n    def validate_output_label(self, label):\n        pattern = r'^OUT_\[^_]+_(.*)\$'\n        return bool(re.match(pattern, label))\n\n    def validate_input_label(self, label):\n        pattern = r'^IN_\[^_]+_(.*)\$'\n        return bool(re.match(pattern, label))\n\n    def clear_selection(self):\n        for node in nuke.allNodes():\n            node.setSelected(False)\n\n    def duplicate_expression_linked(self, node):\n        node.setSelected(True)\n        nuke.duplicateSelectedNodes()\n\n        ignoreKnobs = \['onDestroy', 'bookmark', 'autolabel', 'selected', 'rootNodeUpdated', 'help', 'updateUI',\n                       'onCreate', 'icon', 'xpos', 'ypos', 'panelDropped', 'maskFromFlag', 'name', 'maskFrom',\n                       'indicators', 'process_mask', 'label', 'knobChanged']\n\n        for knob in nuke.selectedNode().knobs():\n            if not any(item in knob for item in ignoreKnobs):\n                nuke.selectedNode()\[knob].setExpression('\{\}.\{\}'.format(node.name(), knob))\n        nuke.selectedNode()\['label'].setValue('CHILD OF \{\}'.format(node.name()))\n\n    def update_label(self, node, newLabel):\n        try:\n            if node\['label'].getValue() != newLabel:\n                node\['label'].setValue(newLabel)\n        except NameError:\n            return False\n\n\n\ninput_fetcher_class = 'Dot'\n\ndef validateFetchInput(node):\n    inputPrefix = 'IN_'\n    label = node\['label'].getValue()\[:3]\n    if inputPrefix in label and node\['inputFetcherId']:\n        return True\n\n\ndef validateFetchOutput(node):\n    try:\n        if node\['label'].getValue().startswith('OUT_') and node\['inputFetcherId']:\n            return True\n    except NameError:\n        return False\n\ndef findFetcherOutputFrom(id, selfName):\n    for node in nuke.allNodes(input_fetcher_class):\n        if validateFetchOutput(node) and node.name() != selfName:\n            tmpId = utils.get_fetcher_id(node)\n            if tmpId == id:\n                return node\n\ndef convertToInput(node):\n    label = node\['label'].getValue().replace('OUT_', 'IN_')\n    node\['label'].setValue(label)\n\ndef outputExists(inputNode):\n    for node in nuke.allNodes(input_fetcher_class):\n        try:\n            if inputNode\['inputFetcherId'].getValue() == node\['inputFetcherId'].getValue() and validateFetchOutput(node) and validateFetchInput(inputNode) or validateFetchOutput(inputNode):\n                return True\n        except NameError:\n            pass\n    return False\n\ndef hasDuplicateOutput(output):\n    for node in nuke.allNodes(input_fetcher_class):\n        try:\n            if output\['inputFetcherId'].getValue() == node\['inputFetcherId'].getValue() and validateFetchOutput(node) and node != output:\n                return True\n        except NameError:\n            pass\n    return False\n\ndef createOutputFromInput(input_node):\n    node_class_obj = getattr(nuke.nodes, input_fetcher_class)\n    output = node_class_obj(label = input_node\['label'].getValue().replace('IN_', 'OUT_'), note_font_size = 45, note_font = 'Bold')\n    knob = nuke.String_Knob('inputFetcherId')\n    output.addKnob(knob)\n    output\['inputFetcherId'].setValue(input_node\['inputFetcherId'].getValue())\n    output\['inputFetcherId'].setEnabled(False)\n    output\['tile_color'].setValue(int(input_node\['tile_color'].getValue()))\n    output\['note_font_color'].setValue(int(input_node\['tile_color'].getValue()))\n    utils.label_as_name(output)\n    for knob in output.knobs():\n        if knob != 'inputFetcherId':\n            output\[knob].setVisible(False)\n    xPos = input_node\['xpos'].getValue()\n    yPos = input_node\['ypos'].getValue()\n    output\['xpos'].setValue(xPos)\n    output\['ypos'].setValue(yPos - 200)\n\ndef appendParentName():\n    parent = nuke.text_knob(nuke.thisNode().name())\n    nuke.thisNode().addKnob(parent)\n\ndef rsCopy():\n    if not nuke.selectedNodes():\n        return False\n    nuke.nodeCopy('%clipboard%')\n    for node in nuke.selectedNodes(input_fetcher_class):\n        if validateFetchInput(node):\n            id = utils.get_fetcher_id(node)\n            targetNode = findFetcherOutputFrom(id, node.name())\n            utils.connect_input(node, targetNode)\n\ndef hideFetcherKnobs(node):\n    for knob in node.knobs():\n        if knob != 'inputFetcherId':\n            node\[knob].setVisible(False)\n\ndef fetcher_is_tagged(node):\n    for knob in node.knobs():\n        if knob == 'inputFetcherSuffix' or knob == 'inputFetcherTag':\n            return True\n    return False\n\ndef untag_fetcher(node):\n    try:\n        node.removeKnob(node.knob('inputFetcherSuffix'))\n        node.removeKnob(node.knob('inputFetcherTag'))\n    except ValueError:\n        pass\n\ndef rsPaste():\n    nuke.nodePaste('%clipboard%')\n    for node in nuke.selectedNodes(input_fetcher_class):\n        if hasDuplicateOutput(node):\n            convertToInput(node)\n        if validateFetchInput(node) and not outputExists(node):\n            createOutputFromInput(node)\n        if validateFetchInput(node):\n            id = utils.get_fetcher_id(node)\n            targetNode = findFetcherOutputFrom(id, node.name())\n            utils.connect_input(node, targetNode)\n        hideFetcherKnobs(node)\n    for node in nuke.selectedNodes():\n        if fetcher_is_tagged(node):\n            untag_fetcher(node)\n\n\nnuke.menu('Nuke').addCommand('Edit/Input_Fetcher_Copy', rsCopy, 'ctrl+c')\nnuke.menu('Nuke').addCommand('Edit/Input_Fetcher_Paste', rsPaste, 'ctrl+v')\n\n\nclass InputFetcher(QtWidgets.QDialog):\n    def __init__(self):\n        QtWidgets.QDialog.__init__(self)\n\n        # Config input/output node class\n        self.node_class = 'Dot'\n\n        # Config window defaults\n        self.setWindowTitle('Input Fetcher')\n\n        # Config font defaults;\n        self.button_font = 'Times'\n\n        # Config search variables\n        self.outputPrefix = 'OUT'\n        self.inputPrefix = 'IN'\n        self.separator = '_'\n        self.tag_knob = 'inputFetcherTag'\n        self.id_knob = 'inputFetcherId'\n\n        # Config group prefixes and colors\n        self.prefix_color = \{\n    'PLATE': '#F5F5DC',\n    'MATTE': '#3CB371',\n    'RENDER': '#66FF66',\n    'DEEP': '#00BFFF',\n    'CAM': \"#FA8072\",\n    'GEO': '#FFA500',\n\}\n\n        # Config label variables\n        self.outputLabels = \[]\n        self.cleanedLabels = \[]\n        self.uniquePrefixList = \[]\n        self.outputNodes = \[]\n        # Prepare a dict with LABEL + ID // Reset each instance\n        self.outputInfo = \[]\n\n        # Config tagged nodes\n        self.taggedNodes = \[]\n\n        # Config commands\n        self.commands = \['TAG', 'UNTAG']\n        # Config layout\n        self.mainLayout = QtWidgets.QVBoxLayout()\n\n    def initLayout(self):\n        # Config labeller\n        placeHolderText = 'Ex. OUT_MATTE_CHARACTER_FG'\n        if len(nuke.selectedNodes()) == 1:\n            n = nuke.selectedNode()\n            placeHolderText = n\['label'].getValue()\n        self.labeller = QtWidgets.QLineEdit(placeHolderText)\n        self.labeller.setPlaceholderText(\"Enter a command or label ... \")\n        self.labeller.returnPressed.connect(self.labelNode)\n        self.labeller.selectAll()\n        QtCore.QTimer.singleShot(0, self.labeller.setFocus)\n        self.labellerLabel = QtWidgets.QLabel('ENTER LABEL:')\n        self.labellerLabel.setFont(QtGui.QFont(self.button_font, 15, QtGui.QFont.Bold))\n        self.warningLabel = QtWidgets.QLabel('')\n        self.warningLabel.setFont(QtGui.QFont(self.button_font, 15, QtGui.QFont.Bold))\n        self.warningLabel.setStyleSheet('color : yellow')\n\n        # Config divider\n        self.labelDivider = QtWidgets.QFrame()\n        self.labelDivider.setFrameShape(QtWidgets.QFrame.HLine)\n        self.labelDivider.setFrameShadow(QtWidgets.QFrame.Sunken)\n        self.mainLayout.addWidget(self.labellerLabel)\n        self.mainLayout.addWidget(self.warningLabel)\n        self.mainLayout.addWidget(self.labeller)\n        self.mainLayout.addWidget(self.labelDivider)\n\n\n    def is_duplicate_label(self, label):\n        return label in \[item\['label'] for item in self.outputInfo]\n\n    def has_valid_id(self, node):\n        return self.id_knob in node.knobs()\n\n    def is_valid_output(self, node):\n        try:\n            label = node\['label'].getValue()\n            has_valid_id = self.has_valid_id(node)\n            has_valid_label = label.startswith(self.outputPrefix + self.separator) and label.count(self.separator) >= 2\n            return has_valid_id and has_valid_label\n        except NameError:\n            return False\n\n    def is_valid_input(self, node):\n        try:\n            label = node\['label'].getValue()\n            return node\[self.id_knob] and label.startswith(self.inputPrefix + self.separator) and label.count(\n                self.separator) >= 2\n        except NameError:\n            return False\n\n    def getFetcherLabel(self, node):\n        return node\['label'].getValue().upper()\n\n    def getFetcherPrefix(self, node):\n        if self.is_valid_input(node) or self.is_valid_output(node):\n            return node\['label'].getValue().split('_')\[1]\n\n    def makeDict(self, name, ident, label):\n        return (\n            \{\"name\": name,\n             self.id_knob: ident,\n             \"label\": label\}\n        )\n\n    def collectOutputs(self):\n        for node in nuke.allNodes(self.node_class):\n            if self.is_valid_output(node):\n                self.outputLabels.append(self.getFetcherLabel(node))\n                self.outputNodes.append(node)\n                self.outputInfo.append(self.makeDict(node.name(), utils.get_fetcher_id(node),\n                                                     self.getFetcherLabel(node)))\n\n    def findUniquePrefixes(self):\n        # EXAMPLE: MATTE_CHARACTER --> MATTE\n        try:\n            for item in self.outputInfo:\n                prefix = item\['label'].replace(self.outputPrefix + self.separator, \"\").split(self.separator)\[0]\n                if prefix not in self.uniquePrefixList:\n                    self.uniquePrefixList.append(prefix)\n        except:\n            print('something gone wrong')\n\n    def sortUniquePrefixes(self):\n        # get all unique prefixes\n        origList = self.uniquePrefixList\n        # get all deafult prefixes\n        defaultList = self.prefix_color.keys()\n\n        # remove default prefixes that aren't in current script\n        # we end up with a new default prefix list in proper order\n        for label in defaultList:\n            defaultList = \[i for i in defaultList if i in origList]\n\n        # remove valid default prefixes from current script's prefix list\n        for label in origList:\n            origList = \[i for i in origList if i not in defaultList]\n\n        # join the two lists together which will have the correct default prefix ordering\n        defaultList += origList\n        # update uniquePrefixList with new defaultList\n        self.uniquePrefixList = defaultList\n\n    def groupOutputs(self):\n        tmpList = \[]\n        # first loop to find first prefix\n        for item in self.outputInfo:\n            curPrefix = item\['label'].split(self.separator)\[1]\n            for item in self.outputInfo:\n                lookupPrefix = item\['label'].split(self.separator)\[1]\n                if lookupPrefix == curPrefix:\n                    tmpList.append(\n                        \{\n                            'label': '_'.join(item\['label'].split(self.separator)\[2:]).upper(),\n                            self.id_knob: item\[self.id_knob],\n                        \}\n                    )\n            setattr(self, 'group\{\}'.format(curPrefix.capitalize()), tmpList)\n            # reset tmpList before new loop begins\n            tmpList = \[]\n\n    def createButtonsFromLabels(self):\n        # config font\n        labelFont = QtGui.QFont(self.button_font, 15, QtGui.QFont.Bold)\n        buttonFont = QtGui.QFont(self.button_font, 10, QtGui.QFont.Bold)\n        for p in self.uniquePrefixList:\n            # config color by prefix\n            color = self.prefix_color.get(p)\n            x = getattr(self, 'group\{\}'.format(p.capitalize()))\n            label = QtWidgets.QLabel(p)\n            label.setFont(labelFont)\n            label.setStyleSheet('color : \{\}'.format(color))\n            labelDivider = QtWidgets.QFrame()\n            labelDivider.setFrameShape(QtWidgets.QFrame.HLine)\n            labelDivider.setFrameShadow(QtWidgets.QFrame.Sunken)\n            # dynamically create QHBoxLayout for each label as class attribs\n            labelLayout = setattr(self, '\{\}LabelLayout'.format(p.lower()), QtWidgets.QHBoxLayout())\n            # reference newly created QHBoxLayout obj\n            labelLayoutRef = getattr(self, '\{\}LabelLayout'.format(p.lower()))\n\n            labelLayoutRef.addWidget(label)\n            # dynamically create QHBoxLayout for each button as class attribs\n            buttonsLayout = setattr(self, '\{\}ButtonsLayout'.format(p.lower()), QtWidgets.QGridLayout())\n            # reference newly created QHBoxLayout obj\n            buttonsLayoutRef = getattr(self, '\{\}ButtonsLayout'.format(p.lower()))\n            buttonsLayoutRef.setColumnStretch(10,1)\n\n            x.reverse()\n            for i, l in enumerate(x):\n                row = i//10\n                column = i % 10\n                button = QtWidgets.QPushButton(l\['label'])\n                button.setObjectName(l\[self.id_knob])\n                button.setStyleSheet(\"color : \{\}\".format(color))\n                button.setFont(buttonFont)\n                button.clicked.connect(self.eventButtonClicked)\n                buttonsLayoutRef.addWidget(button, row, column)\n            self.mainLayout.addLayout(labelLayoutRef)\n            self.mainLayout.addWidget(labelDivider)\n            self.mainLayout.addLayout(buttonsLayoutRef)\n            self.mainLayout.addStretch()\n\n    def setMainLayout(self):\n        self.setLayout(self.mainLayout)\n\n    def convertHexColor(self, color):\n        format = '0x_ff'\n        return int(format.replace('_', color\[1:]), 16)\n\n    def colorNodeByPrefix(self, node, prefix):\n        try:\n            color = self.convertHexColor(self.prefix_color.get(prefix))\n            node\['tile_color'].setValue(color)\n            node\['note_font_color'].setValue(color)\n        except:\n            node\['tile_color'].setValue(0)\n            node\['note_font_color'].setValue(0)\n\n    def updateId(self, node, newId):\n        try:\n            if node\[self.id_knob].getValue() != newId:\n                node\[self.id_knob].setValue(newId)\n        except NameError:\n            return False\n\n    def reset_labeller_state(self):\n        QtCore.QTimer.singleShot(0, self.labeller.setFocus)\n        self.labeller.selectAll()\n\n    def eventButtonClicked(self):\n        if self.output_in_selection():\n            self.warningLabel.setText(\n                \"SORRY, CAN'T CONVERT AN OUTPUT INTO AN INPUT.  \\nPLEASE DESELECT ANY OUTPUT NODES!\")\n            self.reset_labeller_state()\n            return False\n\n        buttonId = \\\n        \[item\[self.id_knob] for item in self.outputInfo if item\[self.id_knob] == self.sender().objectName()]\[0]\n        buttonLabel = \\\n        \[item\['label'] for item in self.outputInfo if item\[self.id_knob] == self.sender().objectName()]\[0]\n        parent = self.getParentFromId(buttonId)\n\n        if nuke.selectedNodes():\n            for node in nuke.selectedNodes():\n                if self.is_valid_input(node) and utils.get_fetcher_id(node) != buttonId:\n                    self.updateId(node, buttonId)\n                    utils.update_label(node, self.convertLabelToInput(buttonLabel))\n                    utils.connect_input(node, parent)\n                    self.colorNodeByPrefix(node, self.getFetcherPrefix(node))\n                    self.close()\n                elif self.is_valid_input(node) and utils.get_fetcher_id(node) == buttonId:\n                    self.close()\n                elif node.Class() == self.node_class:\n                    self.convert_default_node_to_input(node, buttonLabel, buttonId, parent)\n                    self.close()\n                elif node.Class() != self.node_class:\n                    self.warningLabel.setText(\"COULDN'T CREATE INPUT NODES FOR SOME NODES!\\nBECAUSE THEY AREN'T \{\} NODES!\".format(self.node_class.upper()))\n        else:\n            fetchNode = self.createFetchNode(self.convertLabelToInput(buttonLabel), buttonId)\n            utils.connect_input(fetchNode, parent)\n            self.close()\n            return True\n\n    def set_label(self, node, label_text):\n        font_size = 100 if node.Class() == 'BackdropNode' else 45\n        node\['note_font_size'].setValue(font_size)\n        node\['label'].setValue(label_text)\n        node\['note_font'].setValue('Bold')\n\n    def updateOuputAndChildren(self, ident, label):\n        for item in self.outputInfo:\n            if item\[self.id_knob] == ident:\n                parent = nuke.toNode(item\['name'])\n                prefix = label.split(self.separator)\[1]\n                if self.is_valid_output(parent):\n                    self.set_label(parent, label)\n                    self.colorNodeByPrefix(parent, prefix)\n                for node in nuke.allNodes(self.node_class):\n                    if self.is_valid_input(node) and node\[self.id_knob].getValue() == ident:\n                        self.set_label(node, label.replace(self.outputPrefix + self.separator,\n                                                           self.inputPrefix + self.separator))\n                        self.colorNodeByPrefix(node, prefix)\n\n    def output_in_selection(self):\n        try:\n            if nuke.selectedNodes(self.node_class):\n                for node in nuke.selectedNodes():\n                    if self.is_valid_output(node):\n                        raise StopIteration\n        except StopIteration:\n            return True\n        else:\n            return False\n\n    def multiple_outputs_selected(self, nodes):\n        outputCounter = 0\n        for node in nodes:\n            if self.is_valid_output(node):\n                outputCounter += 1\n        if outputCounter > 1:\n            return True\n        return False\n\n    def input_nodes_selected(self, nodes):\n        foundInput = False\n        foundOutput = False\n        for node in nodes:\n            if self.is_valid_input(node):\n                foundInput = True\n                break\n        for node in nodes:\n            if self.is_valid_output(node):\n                foundOutput = True\n                break\n        if foundOutput:\n            return False\n        else:\n            return foundInput\n\n    def inputIsCommand(self, input):\n        return input.split(' ')\[0] in self.commands\n\n    def multiple_default_node_selected(self, nodes):\n        default_node_counter = 0\n        try:\n            for node in nodes:\n                if node.Class() == self.node_class and not self.is_valid_output(node) and not self.is_valid_input(node):\n                    default_node_counter += 1\n                if default_node_counter == 2:\n                    raise StopIteration\n        except StopIteration:\n            return True\n        return False\n\n    def labelNode(self):\n        input = self.labeller.text().upper()\n        n = nuke.selectedNodes()\n\n        if self.inputIsCommand(input):\n            for node in n:\n                if self.is_valid_input(node) or self.is_valid_output(node):\n                    self.warningLabel.setText(\"CAN'T TAG INPUT OR OUTPUT NODES.\\nPLEASE CHECK YOUR SELECTION!\")\n                    return\n                cmd = getattr(self, input.split(' ')\[0].lower())\n                suffix = ' '.join(input.split(' ')\[1:])\n                cmd(nuke.toNode(node.name()), suffix)\n            self.close()\n            return\n\n        if not n:\n            # print(\"\\nFailed at \{\}.\".format(inputFetcher.setLabel.__name__)) this prints the name of the function\n            self.createFetchNode(input)\n            self.close()\n            return False\n\n        if self.input_nodes_selected(n):\n            self.warningLabel.setText(\"CAN'T RENAME INPUT NODES.\")\n            self.reset_labeller_state()\n            return False\n\n        if self.is_duplicate_label(input):\n            self.warningLabel.setText(input + ' already exists.  Please enter a different name.')\n            self.reset_labeller_state()\n            return False\n\n        if self.multiple_outputs_selected(n):\n            self.warningLabel.setText(\"CAN'T RENAME MULTIPLE OUTPUTS AT THE SAME TIME.  RENAME ONE AT A TIME PLEASE!\")\n            self.reset_labeller_state()\n            return False\n\n        if self.multiple_default_node_selected(n) and utils.validate_output_label(input):\n            self.warningLabel.setText(\n                \"CAN'T CREATE MORE THAN ONE OUTPUT AT THE SAME TIME!\\nMULTIPLE \{\} NODES SELECTED!\".format(\n                    self.node_class.upper()))\n            self.reset_labeller_state()\n            return False\n\n\n        if len(n) == 1 and nuke.selectedNode().Class() == 'BackdropNode' and not self.inputIsCommand(input):\n            self.set_label(nuke.selectedNode(), input)\n            self.close()\n            return\n\n        if len(n) == 1 and self.is_valid_output(\n                nuke.selectedNode()) and utils.validate_output_label(input):\n            self.updateOuputAndChildren(utils.get_fetcher_id(nuke.selectedNode()), input.upper())\n            self.close()\n            return\n\n        if len(n) == 1 and not self.is_valid_output(nuke.selectedNode()) and not self.is_valid_input(\n                nuke.selectedNode()) and utils.validate_output_label(input):\n            if nuke.selectedNode().Class() == self.node_class:\n                self.createFetchNode(input, node=nuke.selectedNode())\n                self.close()\n                return\n            else:\n                self.createFetchNode(input)\n                self.close()\n                return\n\n        selected_node_classes = \[]\n        for node in n:\n            selected_node_classes.append(node.Class())\n            if self.node_class not in selected_node_classes and utils.validate_output_label(input):\n                self.warningLabel.setText(\n                    \"I DON'T KNOW WHICH NODE YOU WANT TO CREATE AN OUTPUT FOR.\\nPLEASE HAVE ONLY ONE NODE SELECTED!\")\n                self.reset_labeller_state()\n                return False\n            if not self.is_valid_input(node):\n                if input not in self.commands:\n                    if self.is_valid_output(node):\n                        self.warningLabel.setText(\n                            \"TRYING TO RENAME AN OUTPUT NODE WITH AN INVALID LABEL.  SYNTAX = OUT_PREFIX_LABEL\")\n                        self.reset_labeller_state()\n                        return False\n                    elif not input.startswith(self.outputPrefix + self.separator):\n                        self.set_label(node, input)\n                    elif input.startswith(self.outputPrefix + self.separator):\n                        if node.Class() == self.node_class:\n                            self.createFetchNode(input, node=node)\n                self.close()\n\n    def tag(self, node, suffix=None):\n        try:\n            node.removeKnob(node.knob('inputFetcherSuffix'))\n            node.removeKnob(node.knob(self.tag_knob))\n        except ValueError:\n            pass\n        if not node.knob(self.tag_knob):\n            knob = nuke.Boolean_Knob(self.tag_knob, self.tag_knob, 1)\n            node.addKnob(knob)\n            knob.setVisible(False)\n            if suffix:\n                suffix_knob = nuke.String_Knob('inputFetcherSuffix')\n                node.addKnob(suffix_knob)\n                node\['inputFetcherSuffix'].setValue(suffix)\n                suffix_knob.setVisible(False)\n            node.knob(0).setFlag(0)  # or node.setTab(0)\n        elif node.knob(self.tag_knob) and suffix:\n            try:\n                suffix_knob = nuke.String_Knob('inputFetcherSuffix')\n                node.addKnob(suffix_knob)\n                node\['inputFetcherSuffix'].setValue(suffix)\n                suffix_knob.setVisible(False)\n            except ValueError:\n                pass\n        else:\n            node\['inputFetcherSuffix'].setValue(suffix)\n\n    def findTaggedNodes(self):\n        for node in nuke.allNodes():\n            if node.knob(self.tag_knob):\n                self.taggedNodes.append(node)\n\n    def convertLabelToInput(self, label):\n        return label.replace(self.outputPrefix + self.separator, self.inputPrefix + self.separator)\n\n    def assign_id(self, node, ident=''):\n        if not ident:\n            id = uuid.uuid4().hex\[:16]\n            knob = nuke.String_Knob(self.id_knob)\n            node.addKnob(knob)\n            node\[self.id_knob].setValue(id)\n        else:\n            knob = nuke.String_Knob(self.id_knob)\n            node.addKnob(knob)\n            node\[self.id_knob].setValue(ident)\n        node\[self.id_knob].setFlag(0x0000000000000080)\n\n    def getParentFromId(self, id):\n        for node in nuke.allNodes(self.node_class):\n            if self.is_valid_output(node) and node\[self.id_knob].getValue() == id:\n                return node\n\n    def interface2rgb(self, hexValue):\n        return \[(0xFF & hexValue >> i) / 255.0 for i in \[24, 16, 8]]\n\n    def rgb_to_hex(self, rgb):\n        return '#\{:02x\}\{:02x\}\{:02x\}'.format(int(rgb\[0] * 255), int(rgb\[1] * 255), int(rgb\[2] * 255))\n\n    def invert_rgb(self, rgb):\n        return \[1 - rgb\[0], 1 - rgb\[1], 1 - rgb\[2]]\n\n    def calc_rgb_luminance(self, rgb):\n        luminance = rgb\[0] * 0.2126 + rgb\[1] * 0.7152 + rgb\[2] * 0.0722\n        return luminance\n\n    def has_custom_tile_color(self, node):\n        return bool(node\['tile_color'].getValue())\n\n    def layoutTaggedNodes(self):\n        if self.taggedNodes:\n            labelFont = QtGui.QFont(self.button_font, 15, QtGui.QFont.Bold)\n            buttonFont = QtGui.QFont('PMingLiU-ExtB', 10, QtGui.QFont.Bold)\n            # get rid of this stupid drop shadow arrrrrg\n            label = QtWidgets.QLabel('TAGGED')\n            label.setFont(labelFont)\n\n            buttonsLayout = setattr(self, '\{\}ButtonsLayout'.format('tagged'), QtWidgets.QGridLayout())\n            buttonsLayoutRef = getattr(self, '\{\}ButtonsLayout'.format('tagged'))\n            buttonsLayoutRef.setColumnStretch(10, 1)\n\n            self.taggedNodes.reverse()\n            for i, node in enumerate(self.taggedNodes):\n                row = i//10\n                column = i % 10\n                for knob in node.knobs():\n                    if 'inputFetcherSuffix' == knob:\n                        name = node\['inputFetcherSuffix'].getValue()\n                        break\n                    else:\n                        name = node.name()\n                if self.has_custom_tile_color(node):\n                    node_tile_color = int(node\['tile_color'].getValue())\n                else:\n                    node_tile_color = nuke.defaultNodeColor(node.Class())\n                node_rgb_tile_color = self.interface2rgb(node_tile_color)\n                if self.calc_rgb_luminance(node_rgb_tile_color) < .5:\n                    text_color = 'white'\n                else:\n                    text_color = 'black'\n                node_default_hex_code = self.rgb_to_hex(node_rgb_tile_color)\n                button = QtWidgets.QPushButton(name)\n                button.setObjectName(node.name())\n                button.setStyleSheet(\"background-color : \{\}; color : \{\}\".format(node_default_hex_code, text_color))\n                button.setFont(buttonFont)\n                button.clicked.connect(self.taggedButton)\n                buttonsLayoutRef.addWidget(button, row, column)\n\n            labelDivider = QtWidgets.QFrame()\n            labelDivider.setFrameShape(QtWidgets.QFrame.HLine)\n            labelDivider.setFrameShadow(QtWidgets.QFrame.Sunken)\n\n            self.mainLayout.addWidget(label)\n            self.mainLayout.addWidget(labelDivider)\n            self.mainLayout.addLayout(buttonsLayoutRef)\n\n    def taggedButton(self):\n        senderName = self.sender().objectName()\n        utils.clear_selection()\n        node = nuke.toNode(senderName)\n        if node.Class() != 'BackdropNode':\n            utils.duplicate_expression_linked(node)\n            self.untag(nuke.selectedNode())\n        else:\n            node.selectNodes()\n            node.setSelected(True)\n            nuke.duplicateSelectedNodes()\n            for node in nuke.selectedNodes():\n                self.untag(node)\n        self.close()\n\n    def untag(self, node, *args):\n        for knob in node.knobs():\n            if 'inputFetcherSuffix' == knob or self.tag_knob == knob:\n                node.removeKnob(node.knob(knob))\n\n\n    def resetLayout(self, layout):\n        self.resize(500, 100)\n        self.outputLabels = \[]\n        self.cleanedLabels = \[]\n        self.uniquePrefixList = \[]\n        self.outputNodes = \[]\n        self.outputInfo = \[]\n        self.taggedNodes = \[]\n        if layout is not None:\n            while layout.count():\n                item = layout.takeAt(0)\n                widget = item.widget()\n                if widget is not None:\n                    widget.deleteLater()\n\n                else:\n                    self.resetLayout(item.layout())\n\n    def get_prefix_from_label(self, label):\n        return label.split(self.separator)\[1]\n\n    def convert_default_node_to_input(self, node, label, ident, parent):\n        self.set_label(node, self.convertLabelToInput(label))\n        utils.label_as_name(node)\n        self.assign_id(node, ident)\n        self.colorNodeByPrefix(node, self.get_prefix_from_label(label))\n        utils.connect_input(node, parent)\n\n    def hide_fetcher_knobs(self, node):\n        for knob in node.knobs():\n            if knob != self.id_knob:\n                node\[knob].setVisible(False)\n\n    def createFetchNode(self, label, ident=None, node=None, parent=None):\n        if not node:\n            fetchNode = nuke.createNode(self.node_class)\n            self.set_label(fetchNode, label)\n        else:\n            fetchNode = node\n\n        self.set_label(fetchNode, label)\n        utils.label_as_name(fetchNode)\n        self.hide_fetcher_knobs(fetchNode)\n        try:\n            if utils.validate_output_label(label) or utils.validate_input_label(label):\n                prefix = label.split(self.separator)\[1].upper()\n                self.colorNodeByPrefix(fetchNode, prefix)\n        except IndexError:\n            return False\n        if utils.validate_output_label(label) or utils.validate_input_label(label):\n            try:\n                if fetchNode\[self.id_knob]:\n                    pass\n            except NameError:\n                self.assign_id(fetchNode, ident)\n        return fetchNode\n\n    def goFetch(self):\n        self.resetLayout(self.mainLayout)\n        self.setModal(True)\n        self.collectOutputs()\n        self.initLayout()\n        self.show()\n        self.groupOutputs()\n        self.findUniquePrefixes()\n        self.sortUniquePrefixes()\n        self.findTaggedNodes()\n        self.layoutTaggedNodes()\n        self.createButtonsFromLabels()\n\n        self.setMainLayout()\n\n\ninputFetcher = InputFetcher()\nutils = InputFetcherUtils()\nnuke.menu('Nuke').addCommand('Edit/Input Fetcher', inputFetcher.goFetch, 'shift+n')\n" +STARTLINE}
}
BackdropNode {
 inputs 0
 name BackdropNode2
 tile_color 0x191919ff
 label MATTES
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 1424
 ypos -1110
 bdwidth 5898
 bdheight 898
}
BackdropNode {
 inputs 0
 name BackdropNode3
 tile_color 0x191919ff
 label CAM
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 7773
 ypos -1118
 bdwidth 2342
 bdheight 942
}
BackdropNode {
 inputs 0
 name BackdropNode4
 tile_color 0x191919ff
 label GEO
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 10411
 ypos -1128
 bdwidth 3944
 bdheight 937
}
BackdropNode {
 inputs 0
 name BackdropNode5
 tile_color 0x191919ff
 label RENDERS
 note_font " Bold"
 note_font_size 100
 selected true
 xpos -1092
 ypos 5
 bdwidth 8428
 bdheight 1495
}
BackdropNode {
 inputs 0
 name BackdropNode6
 tile_color 0x191919ff
 label REFERENCE
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 7784
 ypos 11
 bdwidth 2338
 bdheight 1461
}
BackdropNode {
 inputs 0
 name BackdropNode7
 tile_color 0x191919ff
 label TRACKERS
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 10403
 ypos 1
 bdwidth 2726
 bdheight 1492
}
BackdropNode {
 inputs 0
 name BackdropNode8
 tile_color 0x191919ff
 label UTILS
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 13324
 ypos 13
 bdwidth 4617
 bdheight 1470
}
BackdropNode {
 inputs 0
 name BackdropNode9
 tile_color 0x717171ff
 note_font_size 42
 selected true
 xpos 6220
 ypos 5485
 bdwidth 2619
 bdheight 2342
}
BackdropNode {
 inputs 0
 name BackdropNode20
 tile_color 0x388e8e00
 note_font_size 42
 selected true
 xpos 9391
 ypos -6839
 bdwidth 401
 bdheight 291
 z_order 1
}
BackdropNode {
 inputs 0
 name BackdropNode21
 tile_color 0x388e8e00
 note_font_size 42
 selected true
 xpos 9103
 ypos -5130
 bdwidth 325
 bdheight 304
 z_order 1
}
BackdropNode {
 inputs 0
 name BackdropNode22
 tile_color 0x4b4b4bff
 note_font_size 42
 selected true
 xpos 9019
 ypos -4488
 bdwidth 665
 bdheight 192
 z_order 1
}
BackdropNode {
 inputs 0
 name BackdropNode23
 tile_color 0x7171c600
 note_font_size 42
 selected true
 xpos 9354
 ypos -3177
 bdwidth 1300
 bdheight 158
 z_order 1
}
BackdropNode {
 inputs 0
 name BackdropNode24
 tile_color 0x510000ff
 note_font_size 42
 selected true
 xpos 9129
 ypos -2879
 bdwidth 1552
 bdheight 177
 z_order 1
}
BackdropNode {
 inputs 0
 name BackdropNode25
 tile_color 0x8e8e3800
 note_font_size 42
 selected true
 xpos 8869
 ypos -4079
 bdwidth 1897
 bdheight 257
 z_order 1
}
BackdropNode {
 inputs 0
 name BackdropNode13
 tile_color 0x515151ff
 label "LENS FX"
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 15717
 ypos 99
 bdwidth 1700
 bdheight 1256
 z_order 3
 addUserKnob {20 User}
 addUserKnob {6 inputFetcherTag -STARTLINE +HIDDEN}
 addUserKnob {1 inputFetcherSuffix +HIDDEN}
 inputFetcherSuffix LENS_FX
}
BackdropNode {
 inputs 0
 name BackdropNode14
 tile_color 0x515151ff
 label "LENS FX"
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 4975
 ypos 13354
 bdwidth 1700
 bdheight 1256
 z_order 3
 addUserKnob {20 User}
}
BackdropNode {
 inputs 0
 name BackdropNode15
 tile_color 0x515151ff
 label "LENS FX"
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 8469
 ypos 16930
 bdwidth 1700
 bdheight 1256
 z_order 3
 addUserKnob {20 User}
}
BackdropNode {
 inputs 0
 name BackdropNode16
 tile_color 0x515151ff
 label "LENS FX"
 note_font " Bold"
 note_font_size 100
 selected true
 xpos 9382
 ypos 9424
 bdwidth 1700
 bdheight 1256
 z_order 3
 addUserKnob {20 User}
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read6
 selected true
 xpos 3327
 ypos -911
 postage_stamp false
}
Dot {
 name Dot6
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label OUT_MATTE_BG_CHAR_01
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 3361
 ypos -379
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId f8c1cb39a6ac4b2e
}
push $cut_paste_input
ReadGeo {
 name ReadGeo1
 selected true
 xpos 10633
 ypos -952
}
Dot {
 name Dot14
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label OUT_GEO_CAR
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 10667
 ypos -332
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 293128d92765499d
}
Card2 {
 inputs 0
 control_points {3 3 3 6

1 {-0.5 -0.5 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {0 0 0}
1 {0 -0.5 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {0.5 0 0}
1 {0.5 -0.5 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {1 0 0}
1 {-0.5 0 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {0 0.5 0}
1 {0 0 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {0.5 0.5 0}
1 {0.5 0 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {1 0.5 0}
1 {-0.5 0.5 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {0 1 0}
1 {0 0.5 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {0.5 1 0}
1 {0.5 0.5 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {1 1 0} }
 name Card1
 selected true
 xpos 12135
 ypos -972
}
Dot {
 name Dot16
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label OUT_GEO_CARD_01
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 12169
 ypos -344
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId cf09f159979241d4
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read12
 selected true
 xpos 584
 ypos 269
 postage_stamp false
}
Dot {
 name Dot20
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x66ff66ff
 label OUT_RENDER_TREES
 note_font " Bold"
 note_font_size 45
 note_font_color 0x66ff66ff
 selected true
 xpos 618
 ypos 1026
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 6c7390f791894034
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read14
 selected true
 xpos 4061
 ypos 211
 postage_stamp false
}
Dot {
 name Dot22
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x66ff66ff
 label OUT_RENDER_MOUNTAINS
 note_font " Bold"
 note_font_size 45
 note_font_color 0x66ff66ff
 selected true
 xpos 4095
 ypos 991
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8a18f982264e4eb2
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read13
 selected true
 xpos 2269
 ypos 230
 postage_stamp false
}
Dot {
 name Dot21
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x66ff66ff
 label OUT_RENDER_CABLES
 note_font " Bold"
 note_font_size 45
 note_font_color 0x66ff66ff
 selected true
 xpos 2303
 ypos 1001
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 604ca5d1191d4484
}
DeepRead {
 inputs 0
 name DeepRead1
 selected true
 xpos -258
 ypos 291
}
Dot {
 name Dot23
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xbfffff
 label OUT_DEEP_CAR
 note_font " Bold"
 note_font_size 45
 note_font_color 0xbfffff
 selected true
 xpos -224
 ypos 1040
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 871502c4202549d8
}
DeepRead {
 inputs 0
 name DeepRead3
 selected true
 xpos 2876
 ypos 219
}
Dot {
 name Dot25
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xbfffff
 label OUT_DEEP_CABLES
 note_font " Bold"
 note_font_size 45
 note_font_color 0xbfffff
 selected true
 xpos 2910
 ypos 1007
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8d558e5ed4894d4a
}
DeepRead {
 inputs 0
 name DeepRead4
 selected true
 xpos 4676
 ypos 203
}
Dot {
 name Dot26
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xbfffff
 label OUT_DEEP_MOUNTAINS
 note_font " Bold"
 note_font_size 45
 note_font_color 0xbfffff
 selected true
 xpos 4710
 ypos 990
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 49366a53e1e44afe
}
Transform {
 inputs 0
 center {1024 778}
 name Transform1
 label REF:1001
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 10797
 ypos 698
 addUserKnob {20 User}
 addUserKnob {6 inputFetcherTag -STARTLINE +HIDDEN}
 addUserKnob {1 inputFetcherSuffix +HIDDEN}
 inputFetcherSuffix TRACKER_01(1001)
}
Transform {
 inputs 0
 center {1024 778}
 name Transform2
 label REF:1001
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 11415
 ypos 697
 addUserKnob {20 User}
 addUserKnob {6 inputFetcherTag -STARTLINE +HIDDEN}
 addUserKnob {1 inputFetcherSuffix +HIDDEN}
 inputFetcherSuffix TRACKER_02(1001)
}
Transform {
 inputs 0
 center {1024 778}
 name Transform3
 label REF:1010
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 12010
 ypos 697
 addUserKnob {20 User}
 addUserKnob {6 inputFetcherTag -STARTLINE +HIDDEN}
 addUserKnob {1 inputFetcherSuffix +HIDDEN}
 inputFetcherSuffix TRACKER_3(1010)
}
Transform {
 inputs 0
 center {1024 778}
 name Transform4
 label REF:1001
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 12613
 ypos 691
 addUserKnob {20 User}
 addUserKnob {6 inputFetcherTag -STARTLINE +HIDDEN}
 addUserKnob {1 inputFetcherSuffix +HIDDEN}
 inputFetcherSuffix TRACKER_4(1001)
}
Group {
 inputs 0
 name SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION
 tile_color 0x3afff6ff
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 14454
 ypos 376
 addUserKnob {20 User}
 addUserKnob {7 test_knob_0}
 addUserKnob {7 test_knob_1}
 addUserKnob {7 test_knob_2}
 addUserKnob {6 test_knob_4 +STARTLINE}
 addUserKnob {4 test_knob_5 M {"item 0" "item 1" "item 2" "item 4" "item 5"}}
 addUserKnob {6 inputFetcherTag -STARTLINE +HIDDEN}
 addUserKnob {1 inputFetcherSuffix +HIDDEN}
 inputFetcherSuffix LENS_DISTORTION
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
push $cut_paste_input
Group {
 name SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE
 tile_color 0xff3900ff
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 14452
 ypos 831
 addUserKnob {20 User}
 addUserKnob {7 test_knob_0}
 addUserKnob {7 test_knob_1}
 addUserKnob {7 test_knob_2}
 addUserKnob {6 test_knob_4 +STARTLINE}
 addUserKnob {4 test_knob_5 M {"item 0" "item 1" "item 2" "item 4" "item 5"}}
 addUserKnob {6 inputFetcherTag -STARTLINE +HIDDEN}
 addUserKnob {1 inputFetcherSuffix +HIDDEN}
 inputFetcherSuffix NEUTRAL_GRADE
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
push $cut_paste_input
Dot {
 name Dot57
 label IN
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 16494
 ypos 189
}
ZDefocus2 {
 legacy_resize_mode false
 show_legacy_resize_mode false
 name ZDefocus1
 selected true
 xpos 16460
 ypos 373
}
Group {
 name Group1
 label "CHROMATIC ABB"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 16460
 ypos 560
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Group {
 name Group2
 label "LENS FLARES"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 16460
 ypos 832
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Dot {
 name Dot58
 autolabel "nuke.thisNode()\['label'].getValue()"
 label OUT
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 16494
 ypos 1280
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read2
 selected true
 xpos -160
 ypos -869
 postage_stamp false
}
Dot {
 name Dot2
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label OUT_PLATE_DENOISED
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos -126
 ypos -385
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8863bf114c5d438c
}
set N9809d000 [stack 0]
Dot {
 name Dot65
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label IN_PLATE_DENOISED
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos 7962
 ypos 20387
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8863bf114c5d438c
}
Dot {
 name Dot68
 selected true
 xpos 7962
 ypos 20644
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read1
 selected true
 xpos -761
 ypos -866
 postage_stamp false
}
Dot {
 name Dot1
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label OUT_PLATE_NATIVE
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos -727
 ypos -387
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId ef23dc5c4e704b1f
}
set N98086400 [stack 0]
Dot {
 name Dot66
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label IN_PLATE_NATIVE
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos 6992
 ypos 20399
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId ef23dc5c4e704b1f
}
Dot {
 name Dot67
 selected true
 xpos 6992
 ypos 20644
}
Dot {
 inputs 0
 name Dot13
 selected true
 xpos 9712
 ypos 16195
}
Roto {
 inputs 0
 output alpha
 curves {{{v x3f99999a}
  {f 0}
  {n
   {layer Root
    {f 0}
    {t x44800000 x44428000}
    {a pt1x 0 pt1y 0 pt2x 0 pt2y 0 pt3x 0 pt3y 0 pt4x 0 pt4y 0 ptex00 0 ptex01 0 ptex02 0 ptex03 0 ptex10 0 ptex11 0 ptex12 0 ptex13 0 ptex20 0 ptex21 0 ptex22 0 ptex23 0 ptex30 0 ptex31 0 ptex32 0 ptex33 0 ptof1x 0 ptof1y 0 ptof2x 0 ptof2y 0 ptof3x 0 ptof3y 0 ptof4x 0 ptof4y 0 pterr 0 ptrefset 0 ptmot x40800000 ptref 0}}}}}
 toolbox {createBezier {
  { createBezier str 1 ssx 1 ssy 1 sf 1 sb 1 tt 4 }
  { createBezierCusped str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createBSpline str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createEllipse str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createRectangle str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createRectangleCusped str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { brush str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { eraser src 2 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { clone src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { reveal src 3 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { dodge src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { burn src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { blur src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { sharpen src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { smear src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
} }
 toolbar_brush_hardness 0.200000003
 toolbar_source_transform_scale {1 1}
 toolbar_source_transform_center {1024 778}
 name Roto2
 selected true
 xpos 9212
 ypos 15515
}
Project3D2 {
 name Project3D1
 selected true
 xpos 9212
 ypos 15639
}
Card2 {
 inputs 0
 control_points {3 3 3 6

1 {-0.5 -0.5 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {0 0 0}
1 {0 -0.5 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {0.5 0 0}
1 {0.5 -0.5 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {1 0 0}
1 {-0.5 0 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {0 0.5 0}
1 {0 0 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {0.5 0.5 0}
1 {0.5 0 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {1 0.5 0}
1 {-0.5 0.5 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {0 1 0}
1 {0 0.5 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {0.5 1 0}
1 {0.5 0.5 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {1 1 0} }
 name Card2
 selected true
 xpos 12863
 ypos -987
}
Dot {
 name Dot17
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label OUT_GEO_CARD_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 12897
 ypos -362
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 1960750fd2c74f1b
}
set N9806c000 [stack 0]
Dot {
 name Dot51
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label IN_GEO_CARD_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 9467
 ypos 15808
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 1960750fd2c74f1b
}
ApplyMaterial {
 inputs 2
 name ApplyMaterial1
 selected true
 xpos 9212
 ypos 15805
}
push 0
ScanlineRender {
 inputs 3
 conservative_shader_sampling false
 motion_vectors_type distance
 name ScanlineRender2
 selected true
 xpos 9212
 ypos 16192
}
Dot {
 name Dot61
 label IN
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 9246
 ypos 17020
}
ZDefocus2 {
 legacy_resize_mode false
 show_legacy_resize_mode false
 name ZDefocus3
 selected true
 xpos 9212
 ypos 17204
}
Group {
 name Group5
 label "CHROMATIC ABB"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 9212
 ypos 17391
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Group {
 name Group6
 label "LENS FLARES"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 9212
 ypos 17663
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Dot {
 name Dot62
 autolabel "nuke.thisNode()\['label'].getValue()"
 label OUT
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 9246
 ypos 18111
}
Group {
 name SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION3
 tile_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.tile_color}}
 gl_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.gl_color x1 0}}
 label "CHILD OF SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION"
 note_font " Bold"
 note_font_size {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.note_font_size}}
 note_font_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.note_font_color x1 0}}
 selected true
 xpos 9212
 ypos 18414
 hide_input {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.hide_input}}
 cached {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.cached}}
 disable {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.disable}}
 dope_sheet {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.dope_sheet}}
 postage_stamp {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.postage_stamp}}
 postage_stamp_frame {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.postage_stamp_frame}}
 lifetimeStart {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lifetimeStart}}
 lifetimeEnd {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lifetimeEnd}}
 useLifetime {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.useLifetime}}
 lock_connections {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lock_connections}}
 mapsize {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.mapsize}}
 addUserKnob {20 User}
 addUserKnob {7 test_knob_0}
 test_knob_0 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_0}}
 addUserKnob {7 test_knob_1}
 test_knob_1 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_1}}
 addUserKnob {7 test_knob_2}
 test_knob_2 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_2}}
 addUserKnob {6 test_knob_4 +STARTLINE}
 test_knob_4 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_4}}
 addUserKnob {4 test_knob_5 M {"item 0" "item 1" "item 2" "item 4" "item 5"}}
 test_knob_5 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_5}}
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Dot {
 name Dot54
 selected true
 xpos 9246
 ypos 18680
}
Dot {
 inputs 0
 name Dot12
 selected true
 xpos 6279
 ypos 12454
}
ReadGeo {
 inputs 0
 name ReadGeo3
 selected true
 xpos 13715
 ypos -989
}
Dot {
 name Dot18
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label OUT_GEO_LIDAR
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 13749
 ypos -376
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId b409a8b449f34ef6
}
Dot {
 name Dot40
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label IN_GEO_LIDAR
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 6222
 ypos 11761
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId b409a8b449f34ef6
}
Dot {
 name Dot41
 selected true
 xpos 6222
 ypos 12024
}
push $N9806c000
Dot {
 name Dot39
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label IN_GEO_CARD_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 5752
 ypos 11762
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 1960750fd2c74f1b
}
Scene {
 inputs 2
 name Scene1
 selected true
 xpos 5728
 ypos 12000
}
push 0
ScanlineRender {
 inputs 3
 conservative_shader_sampling false
 motion_vectors_type distance
 name ScanlineRender1
 selected true
 xpos 5718
 ypos 12451
}
Dot {
 name Dot59
 label IN
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 5752
 ypos 13444
}
ZDefocus2 {
 legacy_resize_mode false
 show_legacy_resize_mode false
 name ZDefocus2
 selected true
 xpos 5718
 ypos 13628
}
Group {
 name Group3
 label "CHROMATIC ABB"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 5718
 ypos 13815
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Group {
 name Group4
 label "LENS FLARES"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 5718
 ypos 14087
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Dot {
 name Dot60
 autolabel "nuke.thisNode()\['label'].getValue()"
 label OUT
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 5752
 ypos 14535
}
Group {
 name SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION2
 tile_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.tile_color}}
 gl_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.gl_color x1 0}}
 label "CHILD OF SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION"
 note_font " Bold"
 note_font_size {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.note_font_size}}
 note_font_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.note_font_color x1 0}}
 selected true
 xpos 5718
 ypos 14808
 hide_input {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.hide_input}}
 cached {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.cached}}
 disable {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.disable}}
 dope_sheet {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.dope_sheet}}
 postage_stamp {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.postage_stamp}}
 postage_stamp_frame {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.postage_stamp_frame}}
 lifetimeStart {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lifetimeStart}}
 lifetimeEnd {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lifetimeEnd}}
 useLifetime {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.useLifetime}}
 lock_connections {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lock_connections}}
 mapsize {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.mapsize}}
 addUserKnob {20 User}
 addUserKnob {7 test_knob_0}
 test_knob_0 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_0}}
 addUserKnob {7 test_knob_1}
 test_knob_1 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_1}}
 addUserKnob {7 test_knob_2}
 test_knob_2 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_2}}
 addUserKnob {6 test_knob_4 +STARTLINE}
 test_knob_4 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_4}}
 addUserKnob {4 test_knob_5 M {"item 0" "item 1" "item 2" "item 4" "item 5"}}
 test_knob_5 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_5}}
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Dot {
 name Dot42
 selected true
 xpos 5752
 ypos 15055
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read7
 selected true
 xpos 4105
 ypos -936
 postage_stamp false
}
Dot {
 name Dot7
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label OUT_MATTE_BG_CHAR_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 4139
 ypos -368
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 7138c00984314c34
}
set N9800c800 [stack 0]
Dot {
 name Dot43
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_BG_CHAR_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 11344
 ypos 11287
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 7138c00984314c34
}
Dot {
 name Dot44
 selected true
 xpos 11344
 ypos 11428
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read9
 selected true
 xpos 5815
 ypos -957
 postage_stamp false
}
Dot {
 name Dot9
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label OUT_MATTE_SL_TREE
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 5849
 ypos -359
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8549e65ef96d441f
}
set N9800dc00 [stack 0]
Dot {
 name Dot35
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_SL_TREE
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 10705
 ypos 11284
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8549e65ef96d441f
}
Merge2 {
 inputs 2
 name Merge4
 selected true
 xpos 10671
 ypos 11425
}
Blur {
 name Blur1
 selected true
 xpos 10671
 ypos 11503
}
Dot {
 name Dot37
 selected true
 xpos 10705
 ypos 11696
}
Roto {
 inputs 0
 output alpha
 curves {{{v x3f99999a}
  {f 0}
  {n
   {layer Root
    {f 0}
    {t x44800000 x44428000}
    {a pt1x 0 pt1y 0 pt2x 0 pt2y 0 pt3x 0 pt3y 0 pt4x 0 pt4y 0 ptex00 0 ptex01 0 ptex02 0 ptex03 0 ptex10 0 ptex11 0 ptex12 0 ptex13 0 ptex20 0 ptex21 0 ptex22 0 ptex23 0 ptex30 0 ptex31 0 ptex32 0 ptex33 0 ptof1x 0 ptof1y 0 ptof2x 0 ptof2y 0 ptof3x 0 ptof3y 0 ptof4x 0 ptof4y 0 pterr 0 ptrefset 0 ptmot x40800000 ptref 0}}}}}
 toolbox {createBezier {
  { createBezier str 1 ssx 1 ssy 1 sf 1 sb 1 tt 4 }
  { createBezierCusped str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createBSpline str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createEllipse str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createRectangle str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { createRectangleCusped str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { brush str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { eraser src 2 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { clone src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { reveal src 3 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { dodge src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { burn src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { blur src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { sharpen src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
  { smear src 1 str 1 ssx 1 ssy 1 sf 1 sb 1 }
} }
 toolbar_brush_hardness 0.200000003
 toolbar_source_transform_scale {1 1}
 toolbar_source_transform_center {1024 778}
 name Roto1
 selected true
 xpos 10693
 ypos 8413
}
Transform {
 translate {{Transform4.translate} {Transform4.translate}}
 rotate {{Transform4.rotate}}
 scale {{Transform4.scale}}
 skewX {{Transform4.skewX}}
 skewY {{Transform4.skewY}}
 skew_order {{Transform4.skew_order}}
 center {{Transform4.center} {Transform4.center}}
 invert_matrix {{Transform4.invert_matrix}}
 filter {{Transform4.filter}}
 clamp {{Transform4.clamp}}
 black_outside {{Transform4.black_outside}}
 motionblur {{Transform4.motionblur}}
 shutter {{Transform4.shutter}}
 shutteroffset {{Transform4.shutteroffset}}
 shuttercustomoffset {{Transform4.shuttercustomoffset}}
 name Transform5
 tile_color {{Transform4.tile_color x1 0}}
 gl_color {{Transform4.gl_color x1 0}}
 label "CHILD OF Transform4"
 note_font " Bold"
 note_font_size {{Transform4.note_font_size}}
 note_font_color {{Transform4.note_font_color x1 0}}
 selected true
 xpos 10693
 ypos 8583
 hide_input {{Transform4.hide_input}}
 cached {{Transform4.cached}}
 disable {{Transform4.disable}}
 dope_sheet {{Transform4.dope_sheet}}
 postage_stamp {{Transform4.postage_stamp}}
 postage_stamp_frame {{Transform4.postage_stamp_frame}}
 lifetimeStart {{Transform4.lifetimeStart}}
 lifetimeEnd {{Transform4.lifetimeEnd}}
 useLifetime {{Transform4.useLifetime}}
 addUserKnob {20 User}
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read15
 selected true
 xpos 5893
 ypos 197
 postage_stamp false
}
Dot {
 name Dot27
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x66ff66ff
 label OUT_RENDER_DRIVER
 note_font " Bold"
 note_font_size 45
 note_font_color 0x66ff66ff
 selected true
 xpos 5927
 ypos 1010
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8be229cab77b443c
}
Dot {
 name Dot33
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x66ff66ff
 label IN_RENDER_DRIVER
 note_font " Bold"
 note_font_size 45
 note_font_color 0x66ff66ff
 selected true
 xpos 10159
 ypos 8067
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8be229cab77b443c
}
Grade {
 inputs 1+1
 name Grade1
 selected true
 xpos 10125
 ypos 8627
}
DeepRead {
 inputs 0
 name DeepRead5
 selected true
 xpos 6508
 ypos 189
}
Dot {
 name Dot28
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xbfffff
 label OUT_DEEP_DRIVER
 note_font " Bold"
 note_font_size 45
 note_font_color 0xbfffff
 selected true
 xpos 6542
 ypos 1023
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 162a671c80504e6a
}
Dot {
 name Dot32
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xbfffff
 label IN_DEEP_DRIVER
 note_font " Bold"
 note_font_size 45
 note_font_color 0xbfffff
 selected true
 xpos 9350
 ypos 8623
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 162a671c80504e6a
}
Dot {
 name Dot34
 selected true
 xpos 9350
 ypos 8863
}
DeepRecolor {
 inputs 2
 name DeepRecolor1
 selected true
 xpos 10125
 ypos 8860
}
DeepToImage2 {
 name DeepToImage1
 selected true
 xpos 10125
 ypos 9150
}
Dot {
 name Dot63
 label IN
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 10159
 ypos 9514
}
ZDefocus2 {
 legacy_resize_mode false
 show_legacy_resize_mode false
 name ZDefocus4
 selected true
 xpos 10125
 ypos 9698
}
Group {
 name Group7
 label "CHROMATIC ABB"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 10125
 ypos 9885
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Group {
 name Group8
 label "LENS FLARES"
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 10125
 ypos 10157
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Dot {
 name Dot64
 autolabel "nuke.thisNode()\['label'].getValue()"
 label OUT
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 10159
 ypos 10605
}
Group {
 name SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION1
 tile_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.tile_color}}
 gl_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.gl_color x1 0}}
 label "CHILD OF SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION"
 note_font " Bold"
 note_font_size {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.note_font_size}}
 note_font_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.note_font_color x1 0}}
 selected true
 xpos 10125
 ypos 11357
 hide_input {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.hide_input}}
 cached {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.cached}}
 disable {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.disable}}
 dope_sheet {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.dope_sheet}}
 postage_stamp {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.postage_stamp}}
 postage_stamp_frame {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.postage_stamp_frame}}
 lifetimeStart {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lifetimeStart}}
 lifetimeEnd {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lifetimeEnd}}
 useLifetime {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.useLifetime}}
 lock_connections {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.lock_connections}}
 mapsize {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.mapsize}}
 addUserKnob {20 User}
 addUserKnob {7 test_knob_0}
 test_knob_0 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_0}}
 addUserKnob {7 test_knob_1}
 test_knob_1 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_1}}
 addUserKnob {7 test_knob_2}
 test_knob_2 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_2}}
 addUserKnob {6 test_knob_4 +STARTLINE}
 test_knob_4 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_4}}
 addUserKnob {4 test_knob_5 M {"item 0" "item 1" "item 2" "item 4" "item 5"}}
 test_knob_5 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_LENS_DISOTRTION.test_knob_5}}
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Merge2 {
 inputs 2
 name Merge2
 selected true
 xpos 10125
 ypos 11693
}
Dot {
 name Dot36
 selected true
 xpos 10159
 ypos 11923
}
push $N9800dc00
Dot {
 name Dot48
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_SL_TREE
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 8151
 ypos 7568
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8549e65ef96d441f
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read4
 selected true
 xpos 1756
 ypos -896
 postage_stamp false
}
Dot {
 name Dot4
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label OUT_MATTE_FG_CHAR_01
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 1790
 ypos -398
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 7663921e3cef4ba0
}
Dot {
 name Dot47
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_FG_CHAR_01
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 8143
 ypos 7467
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 7663921e3cef4ba0
}
push 0
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read5
 selected true
 xpos 2523
 ypos -903
 postage_stamp false
}
Dot {
 name Dot5
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label OUT_MATTE_FG_CHAR_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 2557
 ypos -383
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 5b16ee3e755a4080
}
Dot {
 name Dot46
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_FG_CHAR_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 8141
 ypos 7380
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 5b16ee3e755a4080
}
push $N9800c800
Dot {
 name Dot45
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_BG_CHAR_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 8137
 ypos 7274
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 7138c00984314c34
}
Merge2 {
 inputs 4+1
 name Merge5
 selected true
 xpos 7835
 ypos 7413
}
push $N98086400
Dot {
 name Dot50
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label IN_PLATE_NATIVE
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos 6671
 ypos 5994
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId ef23dc5c4e704b1f
}
Dot {
 name Dot55
 selected true
 xpos 6671
 ypos 6415
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read3
 selected true
 xpos 460
 ypos -884
 postage_stamp false
}
Dot {
 name Dot3
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label OUT_PLATE_PAINT
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos 494
 ypos -384
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 4771ad6f2e064aca
}
Dot {
 name Dot49
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label IN_PLATE_PAINT
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos 8335
 ypos 5981
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 4771ad6f2e064aca
}
Dot {
 name Dot56
 selected true
 xpos 8335
 ypos 6415
}
push $N9809d000
Dot {
 name Dot31
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xf5f5dcff
 label IN_PLATE_DENOISED
 note_font " Bold"
 note_font_size 45
 note_font_color 0xf5f5dcff
 selected true
 xpos 7512
 ypos 5994
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8863bf114c5d438c
}
Switch {
 inputs 3
 name Switch1
 selected true
 xpos 7478
 ypos 6412
}
Group {
 name SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE1
 tile_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.tile_color}}
 gl_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.gl_color x1 0}}
 label "CHILD OF SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE"
 note_font " Bold"
 note_font_size {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.note_font_size}}
 note_font_color {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.note_font_color x1 0}}
 selected true
 xpos 7478
 ypos 6864
 hide_input {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.hide_input}}
 cached {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.cached}}
 disable {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.disable}}
 dope_sheet {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.dope_sheet}}
 postage_stamp {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.postage_stamp}}
 postage_stamp_frame {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.postage_stamp_frame}}
 lifetimeStart {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.lifetimeStart}}
 lifetimeEnd {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.lifetimeEnd}}
 useLifetime {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.useLifetime}}
 lock_connections {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.lock_connections}}
 mapsize {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.mapsize}}
 addUserKnob {20 User}
 addUserKnob {7 test_knob_0}
 test_knob_0 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.test_knob_0}}
 addUserKnob {7 test_knob_1}
 test_knob_1 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.test_knob_1}}
 addUserKnob {7 test_knob_2}
 test_knob_2 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.test_knob_2}}
 addUserKnob {6 test_knob_4 +STARTLINE}
 test_knob_4 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.test_knob_4}}
 addUserKnob {4 test_knob_5 M {"item 0" "item 1" "item 2" "item 4" "item 5"}}
 test_knob_5 {{SHOW_EPISODE_SEQUENCE_SHOT_SHOT_NEUTRAL_GRADE.test_knob_5}}
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
end_group
Grade {
 inputs 1+1
 name Grade2
 selected true
 xpos 7478
 ypos 7413
}
Merge2 {
 inputs 2
 name Merge1
 selected true
 xpos 7478
 ypos 11920
}
Merge2 {
 inputs 2
 name Merge3
 selected true
 xpos 7478
 ypos 15052
}
Merge2 {
 inputs 2
 name Merge6
 selected true
 xpos 7478
 ypos 18677
}
Crop {
 box {0 0 2048 1556}
 name Crop1
 selected true
 xpos 7478
 ypos 20006
}
Remove {
 operation keep
 channels rgba
 name Remove1
 selected true
 xpos 7478
 ypos 20096
}
Group {
 inputs 3
 name GRAIN
 selected true
 xpos 7478
 ypos 20641
}
 Input {
  inputs 0
  name Input1
  xpos 0
 }
 Output {
  name Output1
  xpos 0
  ypos 300
 }
 Input {
  inputs 0
  name Input2
  xpos 182
  ypos -2
  number 1
 }
 Input {
  inputs 0
  name Input3
  xpos 381
  ypos -12
  number 2
 }
end_group
Write {
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Write1
 selected true
 xpos 7478
 ypos 21117
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read17
 selected true
 xpos 8836
 ypos 227
 postage_stamp false
}
Dot {
 name Dot30
 autolabel "nuke.thisNode()\['label'].getValue()"
 label OUT_REFERENCE_ANGLE_2
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 8870
 ypos 1046
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 61d0f9248db641a5
}
Dot {
 name Dot69
 autolabel "nuke.thisNode()\['label'].getValue()"
 label IN_REFERENCE_ANGLE_2
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 8965
 ypos 20413
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 61d0f9248db641a5
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read16
 selected true
 xpos 8052
 ypos 239
 postage_stamp false
}
Dot {
 name Dot29
 autolabel "nuke.thisNode()\['label'].getValue()"
 label OUT_REFERENCE_ANGLE_1
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 8086
 ypos 1046
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId fb40b3492277417f
}
Dot {
 name Dot70
 autolabel "nuke.thisNode()\['label'].getValue()"
 label IN_REFERENCE_ANGLE_1
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 9927
 ypos 20404
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId fb40b3492277417f
}
DeepRead {
 inputs 0
 name DeepRead2
 selected true
 xpos 1196
 ypos 256
}
Dot {
 name Dot24
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xbfffff
 label OUT_DEEP_TREES
 note_font " Bold"
 note_font_size 45
 note_font_color 0xbfffff
 selected true
 xpos 1230
 ypos 1026
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 4145f130c1e34295
}
push $cut_paste_input
Camera2 {
 name Camera2
 selected true
 xpos 8034
 ypos -900
}
StickyNote {
 inputs 0
 name StickyNote2
 label "<h1>2. INPUT FETCHER HAS 3 MAIN FUNCTIONALITIES:\n    1. LABELLER ( LABEL NODES )\n    2. TAGGER ( TAG NODES AND CALL THEM ANYWHERE IN THE SCRIPT )\n    3. FETCHER ( CREATE OUTPUT NODES AND FETCH THEM ANYWHERE IN THE SCRIPT )\n<br>"
 note_font_size 15
 selected true
 xpos 7683
 ypos -7126
}
StickyNote {
 inputs 0
 name StickyNote3
 label "<h1>3. LABELLER IS A VERY STRAIGHT FORWARD FEATURE.\n\n    LET'S BEGIN BY SELECTING THE GRADE NODE TO THE RIGHT OF ME.                                                               <br>\n    WE CAN USE THE HOTKEY \"SHIFT + N\" TO CALL INPUT FETCHER, AND     ENTER A NEW LABEL FOR OUR GRADE NODE.\n  \n    HIT ENTER WHEN COMPLETED.\n  <br><br>"
 note_font_size 15
 selected true
 xpos 7688
 ypos -6863
}
StickyNote {
 inputs 0
 name StickyNote4
 label "<h1>4. NEXT, LET'S LOOK AT TAGGING.\n    WITH THE  GRADE NODE SELECTED, LET'S CALL INPUT FETCHER ( \"SHIFT + N\" ) AND \\n    ENTER IN THE TAG COMMAND (NOT CASE SENSITIVE, SO WE CAN TYPE IN 'tag' OR 'TAG'):\n\n                                                                          <font color='red'>'TAG'\n\n    HIT ENTER WHEN COMPLETED.<br><br><br>\n\n    * IF YOU WANT TO TAG THE CONTENTS OF A BACKDROP NODE, ONLY TAG THE BACKDROP NODE ITSELF!\n <br>"
 note_font_size 15
 selected true
 xpos 7685
 ypos -6463
}
StickyNote {
 inputs 0
 name StickyNote7
 label "<h1>6. YOU CAN ALSO ASSIGN A LABEL FOR TAGGED NODES FOR CASES WHERE THE NODE'S NAME ISN'T DESCRIPTIVE ENOUGH!\n    \n    LET'S TRY TO RETAG OUR GRADE NODE WITH A NEW LABEL.\n    SELECT IT AGAIN AND CALL INPUT FETCHER ( \"SHIFT + N\" )\n    ENTER THE SAME TAG COMMAND LIKE THIS:\n\n                                                          <font color='red'>'tag My Grade Node'</font>\n\n    IT'S NOW RETAGGED WITH A NEW LABEL IN INPUT FETCHER!\n\n\n    YOU CAN UNTAG ANY NODE BY SELECTING IT AND ENTERING THE COMMAND:\n\n                                                                     <font color='red'>'untag'</font><br><br><br><br>"
 note_font_size 15
 selected true
 xpos 7689
 ypos -5715
}
StickyNote {
 inputs 0
 name StickyNote12
 label "<h1>10.  WITH THE SAME DOTS SELECTED, OPEN INPUT FETCHER AND SET THEM ALL TO A DIFFERNT INPUT IN ONE GO!<br><br>"
 note_font_size 15
 selected true
 xpos 7695
 ypos -4215
}
StickyNote {
 inputs 0
 name StickyNote11
 label "<h1>9.  YOU CAN ALSO CREATE MULTIPLE INPUTS AT ONCE!\n\n    SELECT ALL THE DOT NODES TO THE RIGHT, AND CALL INPUT FETCHER ( \"SHIFT + N\" ).\n    THEN FETCH ANY INPUT!<br><br>"
 note_font_size 15
 selected true
 xpos 7693
 ypos -4486
}
Read {
 inputs 0
 origset true
 name Read10
 selected true
 xpos 6673
 ypos -962
 postage_stamp false
}
Dot {
 name Dot10
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label OUT_MATTE_SR_TREE
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 6707
 ypos -352
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId f9a70a7a73074246
}
set N95ee6000 [stack 0]
Dot {
 name Dot11
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_SR_TREE
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 9497
 ypos -3124
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId f9a70a7a73074246
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read11
 selected true
 xpos -782
 ypos 299
 postage_stamp false
}
Dot {
 name Dot19
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x66ff66ff
 label OUT_RENDER_CAR
 note_font " Bold"
 note_font_size 45
 note_font_color 0x66ff66ff
 selected true
 xpos -748
 ypos 1043
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId a25b0b621d5e47df
}
Dot {
 name Dot38
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x66ff66ff
 label IN_RENDER_CAR
 note_font " Bold"
 note_font_size 45
 note_font_color 0x66ff66ff
 selected true
 xpos 10168
 ypos -3118
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId a25b0b621d5e47df
}
Dot {
 inputs 0
 name Dot53
 selected true
 xpos 9085
 ypos -4386
}
Dot {
 inputs 0
 name Dot72
 selected true
 xpos 9305
 ypos -4392
}
Dot {
 inputs 0
 name Dot73
 selected true
 xpos 9539
 ypos -4393
}
push $N95ee6000
Viewer {
 frame_range 1-100
 name Viewer1
 selected true
 xpos 5452
 ypos 7260
 hide_input true
}
Read {
 inputs 0
 origset true
 in_colorspace scene_linear
 out_colorspace scene_linear
 name Read8
 selected true
 xpos 4999
 ypos -951
 postage_stamp false
}
Dot {
 name Dot8
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label OUT_MATTE_GROUND
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 5033
 ypos -357
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 48cdd9734b574f8e
}
Dot {
 name Dot52
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_GROUND
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 9385
 ypos -2782
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 48cdd9734b574f8e
}
ReadGeo {
 inputs 0
 name ReadGeo2
 selected true
 xpos 11423
 ypos -960
}
Dot {
 name Dot15
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label OUT_GEO_TREES
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 11457
 ypos -342
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 7d1a7658d66f416e
}
Dot {
 name Dot74
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label IN_GEO_TREES
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 10156
 ypos -2777
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 7d1a7658d66f416e
}
StickyNote {
 inputs 0
 name StickyNote8
 label "<h1>13. IF AN INPUT IS DISCONNECTED, YOU CAN QUICKLY RECONNECT IS BY PRESSING THE HOTKEY \"CTRL + C\".  \n    IT WILL FIND ITS PARENT IF IT'S IN THE SCRIPT!\n\n    TRY IT ON THE INPUTS TO THE RIGHT!\n<br><br>"
 note_font_size 15
 selected true
 xpos 7696
 ypos -3173
}
StickyNote {
 inputs 0
 name StickyNote17
 label "<h1>14. YOU CAN QUICKLY JUMP TO AN INPUT'S OUTPUT WITH THE HOTKEY \"a\".\n\nYOU CAN ALSO QUICKLY JUMP BACK TO PREVIOUS INPUT WITH THE SAME HOTKEY!\nTRY IT WITH THE INPUTS TO THE RIGHT!\n<br><br>"
 note_font_size 15
 selected true
 xpos 7701
 ypos -2879
}
StickyNote {
 inputs 0
 name StickyNote10
 label "<h1>8.  CALL INPUT FETCHER NOW AND YOU WILL SEE A NEW <font color = 'red'>MAIN</font> OUTPUT HAS BEEN CREATED IN THE CAMERA ROW.\n\n    CLICK THE BUTTON TO FETCH IT!<br><br>"
 note_font_size 15
 selected true
 xpos 7681
 ypos -4684
}
Grade {
 inputs 0
 name Grade3
 note_font Arial
 selected true
 xpos 9563
 ypos -6711
}
StickyNote {
 inputs 0
 name StickyNote5
 label "<h1>5. NOW THAT THE GRADE NODE HAS BEEN TAGGED, WE CAN CALL IT ANYWHERE IN THE SCRIPT!\n    CALL INPUT FETCHER AGAIN ( \"SHIFT + N\" ) AND YOU WILL SEE THE GRADE NODE HAS BEEN ADDED    TO THE TAGGED ROW AT THE TOP.\n\n    CLICK ON IT AND YOU WILL SEE IT CREATES A CHILD OF THE ORIGINAL GRADE!<br><br>"
 note_font_size 15
 selected true
 xpos 7689
 ypos -5973
}
Camera2 {
 inputs 0
 name Camera1
 selected true
 xpos 9242
 ypos -5021
}
StickyNote {
 inputs 0
 name StickyNote6
 label "<h1>7.  NOW LET'S LOOK AT THE MAIN FUNCTIONALITY OF INPUT FETCHER, WHICH IS ... FETCHING!\n    TO THE RIGHT IS A CAMERA, LET'S CREATE AN OUTPUT FOR IT!\n    THE SYNTAX TO CREATE AN OUTPUT IS (not case sensitive) : \n                                                             <font color='red'> \"OUT_CATEGORY_LABEL\"</font>\n    \n    SELECT THE CAMERA AND CALL INPUT FETCHER ( \"SHIFT + N\" ), AND ENTER THE  COMMAND:\n    \n                                                             <font color='red'> \"OUT_CAM_MAIN\"</font>\n\n    HIT ENTER WHEN COMPLETED.<br>\n\n"
 note_font_size 15
 selected true
 xpos 7688
 ypos -5127
}
push $N9806c000
Dot {
 name Dot76
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0xffa500ff
 label IN_GEO_CARD_02
 note_font " Bold"
 note_font_size 45
 note_font_color 0xffa500ff
 selected true
 xpos 9607
 ypos -3954
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 1960750fd2c74f1b
}
push $N9800dc00
Dot {
 name Dot75
 autolabel "nuke.thisNode()\['label'].getValue()"
 tile_color 0x3cb371ff
 label IN_MATTE_SL_TREE
 note_font " Bold"
 note_font_size 45
 note_font_color 0x3cb371ff
 selected true
 xpos 10176
 ypos -3953
 hide_input true
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId 8549e65ef96d441f
}
Dot {
 inputs 0
 name Dot71
 autolabel "nuke.thisNode()\['label'].getValue()"
 label OUT_TEST_1
 note_font " Bold"
 note_font_size 45
 selected true
 xpos 9034
 ypos -3950
 addUserKnob {20 User}
 addUserKnob {1 inputFetcherId +DISABLED}
 inputFetcherId c344c757f511442d
}
StickyNote {
 inputs 0
 name StickyNote13
 label "<h1>11. WE CAN ALSO CREATE INPUTS BY COPY/PASTE OUTPUT/INPUT NODES.      \\n    GIVE IT A TRY ON THE NODES TO THE RIGHT!\n    ALSO TRY TO SELECT THEM ALL AND PASTING!<br><br>"
 note_font_size 15
 selected true
 xpos 7692
 ypos -4026
}
StickyNote {
 inputs 0
 name StickyNote9
 label "<h1>12. BY DEFAULT, THE FETCH FEATURE RECOGNIZES THESE CATEGORIES OF INPUTS:\n- PLATE\n- MATTE\n- RENDER\n- DEEP\n- CAM\n- GEO\n\nTHEY ARE COLOR CODED BY DEFAULT, AND WILL ALWAYS APPEAR IN THE SAME ORDER AS ABOVE.\n\nALL OF WHICH CAN BE CONFIGURED.\n\nYOU CAN CREATE A NEW CATEGORY BY ENTERING:\n\n                                  <font color='red'>\"OUT_MYCATEGORY_MYOUT\"</font>\n<br><br><br>"
 note_font_size 15
 selected true
 xpos 7693
 ypos -3802
}
StickyNote {
 inputs 0
 name StickyNote15
 label "<h1>15. COPY/PASTING OUTPUTS TO ANOTHER SCRIPT WITH THE SAME OUTPUT \nWILL CONVERT THE PASTED OUTPUT TO AN INPUT AND CONNECT IT TO THE EXISTING OUTPUT.\n<br>"
 note_font_size 15
 selected true
 xpos 7702
 ypos -2606
}
StickyNote {
 inputs 0
 name StickyNote16
 label "<h1>16. COPY/PASTING INPUTS TO ANOTHER SCRIPT WILL AUTO CONNECT IF OUTPUTS ARE AVAILABLE.\n<br>"
 note_font_size 15
 selected true
 xpos 7698
 ypos -2411
}
StickyNote {
 inputs 0
 name StickyNote14
 label "<h1>17. THANK YOU FOR TRYING THE DEMO FOR INPUT FETCHER!\n    FEEL FREE TO PLAY AROUND WITH THE SCRIPT BELOW AND GET A BETTER FEEL OF HOW IT'D WORK IN A REAL SHOT!\n    I'M EAGER TO HEAR TO ANY FEEDBACK AND IF YOU DISCOVER ANY BUGS OR UNWANTED BEHAVIOURS!\n    YOU MAY CONTACT ME AT:\n                                      <font color='red'>raysunvfx@gmail.com<br><br></font>\n\n    FOR DETAILED KNOWN ISSUES OR README OR INSTALLATION PLEASE GO TO:\n\n                                       <font color='red'>https://github.com/raysunvfx/Input-Fetcher\n\n<br><br>"
 note_font_size 15
 selected true
 xpos 7694
 ypos -2233
}
StickyNote {
 inputs 0
 name StickyNote1
 label "<h1>1. WELCOME TO THE INPUT FETCHER DEMO!  \nTHIS IS A TOOL I'VE BEEN DEVELOPING AND HAVE BEEN SUCCESSFULLY USING AT MANY STUDIOS ON MANY SHOWS!\nMY GOAL WITH THIS TOOL IS TO MAKE SCRIPT ORGANIZATION A BREEZE WHILE KEEPING THINGS INTUITIVE!\n\nLET'S SEE WHAT IT CAN DO!\n<br><br>"
 note_font_size 15
 selected true
 xpos 7690
 ypos -7428
}
