# -*- coding: utf-8 -*- 

# overrides lines and patterns in view
def setProjLines(r,g,b, strong = False):
    from pyrevit import revit, DB, forms
    try:
    	selection = revit.get_selection()
        if len(selection)>0:
            with revit.Transaction('Line Color'):
                src_style = DB.OverrideGraphicSettings()
                # constructing RGB value from list
                # color = DB.Color(255,0,0)
                color = DB.Color(r,g,b)
                src_style.SetProjectionLineColor(color)
                src_style.SetCutLineColor(color)
                src_style.SetCutForegroundPatternColor(color)
                src_style.SetCutBackgroundPatternColor(color)

                if strong:
                    src_style.SetSurfaceBackgroundPatternColor(color)
                    src_style.SetCutBackgroundPatternColor(color)

                    # 4 is ElementId of Solid Fill Pattern
                    src_style.SetSurfaceBackgroundPatternId(DB.ElementId(4))
                    src_style.SetCutBackgroundPatternId(DB.ElementId(4))

                for element in selection:
                    revit.active_view.SetElementOverrides(element.Id, src_style)
        else:
            forms.alert('You must select at least one element.', exitscript=True)
    except:
        pass