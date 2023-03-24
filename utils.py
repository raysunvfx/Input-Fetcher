import re
import nuke


class InputFetcherUtils():
    def label_as_name(self, node):
        node['autolabel'].setValue("nuke.thisNode()['label'].getValue()")

    def connect_input(self, node, targetNode):
        node.setInput(0, targetNode)
        node['hide_input'].setValue(True)

    def get_fetcher_id(self, node):
        return node['inputFetcherId'].getValue()

    def validate_output_label(self, label):
        pattern = r'^OUT_[^_]+_(.*)$'
        return bool(re.match(pattern, label))

    def validate_input_label(self, label):
        pattern = r'^IN_[^_]+_(.*)$'
        return bool(re.match(pattern, label))

    def clear_selection(self):
        for node in nuke.allNodes():
            node.setSelected(False)

    def duplicate_expression_linked(self, node):
        node.setSelected(True)
        nuke.duplicateSelectedNodes()

        ignoreKnobs = ['onDestroy', 'bookmark', 'autolabel', 'selected', 'rootNodeUpdated', 'help', 'updateUI',
                       'onCreate', 'icon', 'xpos', 'ypos', 'panelDropped', 'maskFromFlag', 'name', 'maskFrom',
                       'indicators', 'process_mask', 'label', 'knobChanged']

        for knob in nuke.selectedNode().knobs():
            if not any(item in knob for item in ignoreKnobs):
                nuke.selectedNode()[knob].setExpression('{}.{}'.format(node.name(), knob))
        nuke.selectedNode()['label'].setValue('CHILD OF {}'.format(node.name()))

    def update_label(self, node, newLabel):
        try:
            if node['label'].getValue() != newLabel:
                node['label'].setValue(newLabel)
        except NameError:
            return False