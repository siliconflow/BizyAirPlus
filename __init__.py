from importlib.resources import files

from bizyair_cloudberry import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = str(files("bizyair_cloudberry").joinpath("web"))
