# -*- coding: UTF-8 -*-
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
        Transaction, Document, BuiltInParameter
from pyrevit import revit, EXEC_PARAMS

doc = EXEC_PARAMS.event_doc

left = "L"
right = "P"

def door_swing_setter(doc):
    # Auto Door flip setter
    doors = FilteredElementCollector(doc) \
            .OfCategory(BuiltInCategory.OST_Doors) \
            .WhereElementIsNotElementType()
    param_name = 'Door Swing'
    with revit.Transaction('Auto Door Flip Setter'):
        for d in doors:
            param = d.LookupParameter(param_name)
            if param:
                # # default door is Left
                if d.Mirrored:
                    param.Set(right)
                else:
                    param.Set(left)

def win_swing_setter(doc):
    # Auto Window flip setter
    windows = FilteredElementCollector(doc) \
            .OfCategory(BuiltInCategory.OST_Windows) \
            .WhereElementIsNotElementType()
    param_name = 'Window Swing'
    with revit.Transaction('Auto Window Flip Setter'):
        for w in windows:
            w_type_Id = w.GetTypeId()
            w_type = Document.GetElement(doc,w_type_Id)
            # skipping the wall penetration modelled in the window category
            filterp = w_type.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)
            if filterp and filterp.AsString() != "stavebne upravy":
                param = w.LookupParameter(param_name)
                if param:
                    # default window is Right
                    if w.Mirrored:
                        param.Set(left)
                    else:
                        param.Set(right)


if not doc.IsFamilyDocument:
    # WINDOWS
    # getting project info
    # if there is shared parameter NOT checked, script is not triggered
    win_settings = doc.ProjectInformation.LookupParameter("ctWindowSwingSetterOFF")
    try:
        # if parameter is turned on
        if not win_settings or win_settings.AsInteger() == 0:
            win_swing_setter(doc)
    except AttributeError:
        # if parameter doesn't exist
        if not win_settings:
            win_swing_setter(doc)

    # DOORS
    # getting project info
    # if there is shared parameter NOT checked, script is not triggered
    door_settings = doc.ProjectInformation.LookupParameter("ctDoorSwingSetterOFF")
    try:
        # if parameter is nurned on
        if not door_settings or door_settings.AsInteger() == 0:
            door_swing_setter(doc)
    except AttributeError:
        # if parameter doesn't exist
        if not door_settings:
            door_swing_setter(doc)