# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script
from hooksScripts import hookTurnOff

doc = __revit__.ActiveUIDocument.Document
docName = doc.PathName
fileExtension = docName[-3:]

def dialogBox():
   from hook_translate import hook_texts, lang
   title = "Import CAD file"
   # the language value is read from pyrevit config file
   lang = lang()

   # for not showing the hook in families - not saved families have no extension
   if fileExtension == "rvt" or fileExtension == "rte":
      res = forms.alert(hook_texts[lang][title]["text"],
                  options = hook_texts[lang][title]["buttons"],
                  title = title,
                  footer = "CustomTools Hooks")

      # Import
      if res  == hook_texts[lang][title]["buttons"][0]:
         EXEC_PARAMS.event_args.Cancel = False
         # logging to server
         from hooksScripts import hooksLogger
         hooksLogger("CAD file import", doc)

      # Cancel
      elif res  == hook_texts[lang][title]["buttons"][1]:
         EXEC_PARAMS.event_args.Cancel = True
      # More info
      elif res  == hook_texts[lang][title]["buttons"][2]:
         EXEC_PARAMS.event_args.Cancel = True
         url = 'https://gfi.miraheze.org/wiki/Postupy,_ktor%C3%BDm_je_potrebn%C3%A9_sa_vyhn%C3%BA%C5%A5_-_Revit#Importovanie_DWG'
         script.open_url(url)
      else:
         EXEC_PARAMS.event_args.Cancel = True

hookTurnOff(dialogBox,2)