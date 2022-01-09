# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script
from hooksScripts import hookTurnOff

doc = __revit__.ActiveUIDocument.Document

def dialogBox():
  from hook_translate import hook_texts, lang

  title = "Link CAD file"
  # the language value is read from pyrevit config file
  lang = lang()

  # WARNING WINDOW
  res = forms.alert(hook_texts[lang][title]["text"],
                    options = hook_texts[lang][title]["buttons"],
                    title = title,
                    footer = "CustomTools Hooks")
  # BUTTONS
  # Link CAD
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
      if lang == "SK":
        url = 'https://gfi.miraheze.org/wiki/Linknutie_DWG_s%C3%BAboru_do_Revitu'
      else:
        url = 'https://customtools.notion.site/Procedures-to-be-avoided-e6e4ce335d544040acee210943afa237'
      script.open_url(url)
  else:
      EXEC_PARAMS.event_args.Cancel = True

# try to find config file for people who dont want to see the hook
hookTurnOff(dialogBox,3)