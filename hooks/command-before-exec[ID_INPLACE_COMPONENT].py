# -*- coding: UTF-8 -*-\n"
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

from hook_translate import hook_texts

doc = __revit__.ActiveUIDocument.Document

title = "In Place Family"
# the language value will be read from the pyRevit config file - I will add this later
lang = "EN"

# WARNING WINDOW
res = forms.alert(hook_texts[lang][title]["text"],
                  options = hook_texts[lang][title]["buttons"],
                  title = title,
                  footer = "CustomTools Hooks")

# BUTTONS
# Create
if res  == hook_texts[lang][title]["buttons"][0]:
   EXEC_PARAMS.event_args.Cancel = False
   # logging to server
   from hooksScripts import hooksLogger
   hooksLogger("Inplace Component", doc)

# Cancel
elif res  == hook_texts[lang][title]["buttons"][1]:
   EXEC_PARAMS.event_args.Cancel = True
# More info
elif res  == hook_texts[lang][title]["buttons"][2]:
   EXEC_PARAMS.event_args.Cancel = True
   url = 'https://gfi.miraheze.org/wiki/In-place_Families'
   script.open_url(url)
else:
   EXEC_PARAMS.event_args.Cancel = True