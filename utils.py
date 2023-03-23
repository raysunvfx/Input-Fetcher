import re


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