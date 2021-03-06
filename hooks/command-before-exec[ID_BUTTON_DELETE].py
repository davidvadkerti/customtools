# -*- coding: UTF-8 -*-

from pyrevit import EXEC_PARAMS
from pyrevit import forms, script, revit

doc = __revit__.ActiveUIDocument.Document
selection = revit.get_selection()
from hooksScripts import hookTurnOff

def dialogBox(viewNames):
    from hook_translate import hook_texts, lang

    title = "View, Schedule or Sheet Deletion"
    # the language value is read from pyrevit config file
    lang = lang()

    # WARNING WINDOW
    res = forms.alert(hook_texts[lang][title]["text"]+"\n"\
                      + "\n".join(viewNames),
                      options = hook_texts[lang][title]["buttons"],
                      title = title,
                      footer = "CustomTools Hooks")

    # Delete
    if res == hook_texts[lang][title]["buttons"][1]:
        EXEC_PARAMS.event_args.Cancel = False
        from hooksScripts import hooksLogger
        hooksLogger("View, Schedule or Sheet Deletion",doc)
    # Cancel
    elif res == hook_texts[lang][title]["buttons"][0]:
        EXEC_PARAMS.event_args.Cancel = True
    else:
        EXEC_PARAMS.event_args.Cancel = True

# treating just Views, Schedules and Sheets
viewNames = []
for element in selection:
    try:
        catName = element.Category.Name
        # print(catName)
        # print(element.Name)
        if catName == "Views" or catName == "Schedules" or catName == "Sheets":
            name = element.Name
            # noaccents conversion
            import unicodedata
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore')
            # name = name.decode('utf-8')
            viewNames.append(name)
    except:
        pass


# If there is at least one View or Schedule in selection show alert window
if len(viewNames) > 0:
    # try to find config file for people who dont want to see the hook
    hookTurnOff(dialogBox, 11, viewNames)
    # dialogBox(viewNames)