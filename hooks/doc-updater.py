# -*- coding: UTF-8 -*-
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
        Transaction, Document, BuiltInParameter
from pyrevit import revit, EXEC_PARAMS

doc = EXEC_PARAMS.event_doc

left = "L"
right = "P"

if not doc.IsFamilyDocument:
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