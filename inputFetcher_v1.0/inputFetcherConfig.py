"""
CONFIG SETTINGS FOR INPUT-FETCHER
"""

#GUI CONFIG
_TITLE = 'Input Fetcher'
_WINDOW_SIZE_WIDTH = 500
_WINDOW_SIZE_HEIGHT = 100
_BUTTON_FONT = 'Times'
_PLACE_HOLDER_TEXT = 'Ex. OUT_MATTE_CHARACTER_FG'
_BUTTONS_PER_ROW = 12

#TAG CONFIG
_TAG_KNOB = 'inputFetcherTag'
_ID_KNOB = 'inputFetcherId'

#INPUT CONFIG
_OUTPUT_PREFIX = 'OUT'
_INPUT_PREFIX = 'IN'
_SEPARATOR = '_'

#NODE CONFIG
#RECOMMENDED NODE CLASSES = 'Dot', 'NoOp'
_NODE_CLASS = 'Dot'
_DISTANCE = 100

_PREFIX_COLOR = {
    'PLATE': '#F5F5DC',
    'MATTE': '#3CB371',
    'RENDER': '#66FF66',
    'DEEP': '#00BFFF',
    'CAM': "#FA8072",
    'GEO': '#FFA500',
}

#COMMAND CONFIG
_COMMANDS = ['TAG', 'UNTAG']