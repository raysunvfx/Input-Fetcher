import re
import nuke

class InputFetcherUtils():
    def __init__(self):
        self.input_fetcher_prev_input = None

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

    def zoom_to_parent(self):
        try:
            if len(nuke.selectedNodes()) == 1:
                if 'IN_' not in nuke.selectedNode()['label'].getValue() and 'OUT_' not in nuke.selectedNode()[
                    'label'].getValue():
                    self.input_fetcher_prev_input = None
                    return False
                if self.input_fetcher_prev_input:
                    if nuke.selectedNode()['inputFetcherId'].getValue() != self.input_fetcher_prev_input[
                        'inputFetcherId'].getValue():
                        self.input_fetcher_prev_input = None
                        return False
                if nuke.selectedNode()['label'].getValue().startswith('IN_'):

                    self.input_fetcher_prev_input = nuke.selectedNode()
                    ident = nuke.selectedNode()['inputFetcherId'].getValue()
                    for node in nuke.selectedNodes():
                        node.setSelected(False)
                    for node in nuke.allNodes('Dot'):
                        if 'OUT_' in node['label'].getValue() and node['inputFetcherId'].getValue() == ident:
                            node.setSelected(True)
                            nuke.zoom(.3, [node['xpos'].getValue(), node['ypos'].getValue()])
                else:
                    for node in nuke.selectedNodes():
                        node.setSelected(False)
                    self.input_fetcher_prev_input.setSelected(True)
                    nuke.zoom(.3, [self.input_fetcher_prev_input['xpos'].getValue(),
                                   self.input_fetcher_prev_input['ypos'].getValue()])
                    self.input_fetcher_prev_input = None
        except:
            pass

    def move_node(self, node, x, y):
        node_pos = [node['xpos'].getValue(), node['ypos'].getValue()]
        node['xpos'].setValue(node_pos[0] + x)
        node['ypos'].setValue(node_pos[1] + y)
