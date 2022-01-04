# -*- coding: UTF-8 -*-
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script

from hook_translate import hook_texts, lang

doc = __revit__.ActiveUIDocument.Document

title = "Architectural column"
# the language value is read from pyrevit config file
lang = lang()

# WARNING WINDOW
res = forms.alert(hook_texts[lang][title]["text"],
                  options = hook_texts[lang][title]["buttons"],
                  title = title,
                  footer = "CustomTools Hooks")

# Create
if res  == hook_texts[lang][title]["buttons"][0]:
   EXEC_PARAMS.event_args.Cancel = False
   # logging to server
   from hooksScripts import hooksLogger
   hooksLogger(title, doc)
# Cancel
elif res  == hook_texts[lang][title]["buttons"][1]:
   EXEC_PARAMS.event_args.Cancel = True
# More info
elif res  == hook_texts[lang][title]["buttons"][2]:
   EXEC_PARAMS.event_args.Cancel = True
   url = 'https://gfi.miraheze.org/wiki/Postupy,_ktor%C3%BDm_je_potrebn%C3%A9_sa_vyhn%C3%BA%C5%A5_-_Revit#St.C4.BApy'
   script.open_url(url)
else:
   EXEC_PARAMS.event_args.Cancel = True