# -*- coding: UTF-8 -*-
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script
from hooksScripts import hookTurnOff

import os.path as op

# showing of dialog box with warning
def dialogBox():
   doc = __eventargs__.Document

   # if family is saved
   try:
      fam_path = __eventargs__.FamilyPath
      fam_name = __eventargs__.FamilyName
      famSize = op.getsize(fam_path + fam_name + ".rfa")

      # checking if family is larger than 1 megabyte 
      if famSize > 1048576:
         from hook_translate import hook_texts, lang

         title = "Load Family"
         # the language value is read from pyrevit config file
         lang = lang()

         # WARNING WINDOW
         res = forms.alert(hook_texts[lang][title]["text"],
                          options = hook_texts[lang][title]["buttons"],
                          title = title,
                          footer = "CustomTools Hooks")
         # BUTTONS
         # Load
         if res  == hook_texts[lang][title]["buttons"][1]:
            pass
            # logging to server - cannot access active document
            from hooksScripts import hooksLogger
            hooksLogger("Family loading over 1 MB", doc)
         # Cancel
         elif res  == hook_texts[lang][title]["buttons"][0]:
            EXEC_PARAMS.event_args.Cancel()
         # More info
         elif res  == hook_texts[lang][title]["buttons"][2]:
            url = 'https://gfi.miraheze.org/wiki/Chyby_vo_families_Revitu#Ve.C4.BEkos.C5.A5_Family'
            script.open_url(url)
            EXEC_PARAMS.event_args.Cancel()
         else:
            EXEC_PARAMS.event_args.Cancel()
      else:
         pass
   # if family is not saved yet famSize does not exist
   except:
      pass


# try to find config file for people who dont want to see the hook
hookTurnOff(dialogBox,7)