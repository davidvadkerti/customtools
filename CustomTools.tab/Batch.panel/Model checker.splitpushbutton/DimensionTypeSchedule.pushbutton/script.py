# -*- coding: UTF-8 -*-
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import RevisionCloud, Revision, Dimension, DimensionType

from pyrevit.coreutils import Timer
from customOutput import hmsTimer, ct_icon, file_name_getter

doc = __revit__.ActiveUIDocument.Document
output = script.get_output()
output.set_width(1300)

# changing icon
ct_icon(output)


def showDimensionSchedule(sortByParam):
    timer = Timer()
    # heading
    output.print_md("# DIMENSION TYPE SCHEDULE")

    dimensionType_collector = FilteredElementCollector(doc).OfClass(DimensionType).ToElements()
    dimension_collector = FilteredElementCollector(doc).OfClass(Dimension).WhereElementIsNotElementType().ToElements()

    # count of instances per type
    dimension_types = {}
    for tn in dimension_collector:
        tn_type_id = tn.GetTypeId().ToString()
        try:
            dimension_types[tn_type_id] += 1
        except:
            dimension_types[tn_type_id] = 1

    # text notes type parameters
    scheduleData = []
    for dimension in dimensionType_collector:
        dimension_name = dimension.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
        font = dimension.get_Parameter(DB.BuiltInParameter.TEXT_FONT).AsString()
        size = dimension.get_Parameter(DB.BuiltInParameter.TEXT_SIZE).AsDouble() * 304.8
        bold = dimension.get_Parameter(DB.BuiltInParameter.TEXT_STYLE_BOLD).AsInteger()
        background = dimension.get_Parameter(DB.BuiltInParameter.DIM_TEXT_BACKGROUND).AsInteger()
        show_opening_ht = dimension.get_Parameter(DB.BuiltInParameter.DIM_STYLE_SHOW_OPENING_HT).AsInteger()
        width_factor = dimension.get_Parameter(DB.BuiltInParameter.TEXT_WIDTH_SCALE).AsDouble()
        style_type = dimension.StyleType
        wtns_ln_ctrl = dimension.get_Parameter(DB.BuiltInParameter.DIM_WITNS_LINE_CNTRL).AsInteger()
        if wtns_ln_ctrl == 0:
            wtns_ln_ctrl_v = "Gap to Element"
        if wtns_ln_ctrl == 1:
            wtns_ln_ctrl_v = "Fixed"

        witns_ln_gap = dimension.get_Parameter(DB.BuiltInParameter.WITNS_LINE_GAP_TO_ELT).AsDouble() * 304.8
        witns_ln_ext = dimension.get_Parameter(DB.BuiltInParameter.WITNS_LINE_EXTENSION).AsDouble() * 304.8


        dimension_id = dimension.Id
        dimension_type_creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, dimension_id).Creator 
        try:
            count = dimension_types[dimension_id.ToString()]
        except:
            count = 0

        # list only items with names not settings items
        if dimension_name:
            paramList = [dimension_name, font, size, bold, background, show_opening_ht, width_factor, wtns_ln_ctrl_v, witns_ln_gap, witns_ln_ext, style_type, output.linkify(dimension_id), count, dimension_type_creator]

            scheduleData.append(paramList)

    # sort by parameters
    if sortByParam == "By Style Type":
        sortedScheduleData = sorted(scheduleData, key=lambda x: int(x[10]))
    elif sortByParam == "By Creator":
        sortedScheduleData = sorted(scheduleData, key=lambda x: x[13].lower())
    elif sortByParam == "By Dimension Type Name":
        sortedScheduleData = sorted(scheduleData, key=lambda x: x[0].lower())
    else:
        sortedScheduleData = sorted(scheduleData, key=lambda x: int(x[12]))

    # printing the schedule if there are data
    if sortedScheduleData:
        output.print_table(table_data=sortedScheduleData,
                           title = file_name_getter(doc),
                           columns=["Dimension Type", "Font", "Size", "Bold", "Background", "Text Box Visibility" ,"Width Factor" ,"Witness line extension", "Witness Line Gap", "Witness line extension", "Style Type","Text Note Type ID", "Count", "Creator"],
                           formats=['', '', '', '', '', '', '', '', '', '', '', '', ''])
    # if there are no data print status claim
    else:
        print("There are no Dimension Types in the Project")
      # for timing------
    endtime = timer.get_time()
    print(hmsTimer(endtime))

my_config = script.get_config()

selected_option = \
    forms.CommandSwitchWindow.show(
        ['By Style Type',
         'By Dimension Type Name',
         'By Count of Instances',
         'By Creator'],
        message='Sort by:'
        )

if selected_option:
    showDimensionSchedule(selected_option)