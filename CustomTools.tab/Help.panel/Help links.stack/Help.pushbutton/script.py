from pyrevit import script
from hook_translate import lang

__context__ = 'zero-doc'
lang = lang()

if lang == "SK":
	url = 'https://gfi.miraheze.org/wiki/CustomTools_(Extension_pre_pyRevit)'
else:
	url = 'https://customtools.notion.site/customtools/CustomTools-wiki-76d8472edc6444e5bb3ce90f7998f1ef'
script.open_url(url)