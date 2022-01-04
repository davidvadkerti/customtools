# -*- coding: UTF-8 -*-
from pyrevit import EXEC_PARAMS
from pyrevit import forms, script
from hooksScripts import hookTurnOff

doc = __revit__.ActiveUIDocument.Document

# showing of dialog box with warning
def dialogBox():
    from hook_translate import hook_texts, lang

    title = "Project Parameters"
    # the language value is read from pyrevit config file
    lang = lang()

    # WARNING WINDOW
    res = forms.alert(hook_texts[lang][title]["text"],
                    options = hook_texts[lang][title]["buttons"],
                    title = title,
                    footer = "CustomTools Hooks")
    # BUTTONS
    # Edit Parameters
    if res  == hook_texts[lang][title]["buttons"][1]:
        EXEC_PARAMS.event_args.Cancel = False
        # logging to server
        from hooksScripts import hooksLogger
        hooksLogger("Project or Shared Parameters", doc)
    # Cancel
    elif res  == hook_texts[lang][title]["buttons"][2]:
        EXEC_PARAMS.event_args.Cancel = True
    # View list of Shared Parameters
    elif res  == hook_texts[lang][title]["buttons"][0]:
        EXEC_PARAMS.event_args.Cancel = True
        url = 'https://gfi.miraheze.org/wiki/Shared_parametre_pre_Revit'
        script.open_url(url)
    else:
        EXEC_PARAMS.event_args.Cancel = True

# try to find config file for people who dont want to see the hook
hookTurnOff(dialogBox,9)