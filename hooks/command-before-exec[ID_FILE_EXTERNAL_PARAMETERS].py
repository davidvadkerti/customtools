# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script
from hooksScripts import hookTurnOff

doc = __revit__.ActiveUIDocument.Document

def dialogBox():
    from hook_translate import hook_texts, lang

    title = "Shared Parameters"
    # the language value is read from pyrevit config file
    lang = lang()

    # WARNING WINDOW
    res = forms.alert(hook_texts[lang][title]["text"],
                    options = hook_texts[lang][title]["buttons"],
                    title = title,
                    footer = "CustomTools Hooks")
  
    # Edit Parameters
    if res  == hook_texts[lang][title]["buttons"][1]:
        EXEC_PARAMS.event_args.Cancel = False
        # logging to server
        from hooksScripts import hooksLogger
        hooksLogger("Change Shared Parameters", doc)
    # Cancel
    elif res  == hook_texts[lang][title]["buttons"][2]:
        EXEC_PARAMS.event_args.Cancel = True
    # View Shared Parameter list
    elif res  == hook_texts[lang][title]["buttons"][0]:
        EXEC_PARAMS.event_args.Cancel = True
        if lang == "SK":
            url = 'https://gfi.miraheze.org/wiki/Shared_parametre_pre_Revit'
        else:
            url = 'https://customtools.notion.site/Procedures-to-be-avoided-e6e4ce335d544040acee210943afa237'
        script.open_url(url)
    else:
        EXEC_PARAMS.event_args.Cancel = True

# try to find config file for people who dont want to see the hook
hookTurnOff(dialogBox,9)