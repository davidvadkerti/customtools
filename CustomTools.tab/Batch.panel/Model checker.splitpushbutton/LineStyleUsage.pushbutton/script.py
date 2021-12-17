# -*- coding: UTF-8 -*-

__title__ = 'Lin Style Usage'
__author__ = 'David Vadkerti'
__doc__ = "Lists the count of each Line Style in the project."

from pyrevit import revit, DB
from pyrevit import script
from pyrevit import output

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from customOutput import file_name_getter, ct_icon

doc = __revit__.ActiveUIDocument.Document

output = script.get_output()
# changing icon
ct_icon(output)

output.print_md("# LINE STYLE USAGE")
output.print_md("### " + file_name_getter(doc))
scheduleData = []

# lines
line_collector = DB.FilteredElementCollector(revit.doc).OfCategory(DB.BuiltInCategory.OST_Lines\
    or DB.BuiltInCategory.OST_SketchLines).WhereElementIsNotElementType()


ls_name_list = []
ls_id_list = []
ls_name_u = []
ls_id_u = []
ls_creators = []
for line in line_collector:
    ls_name = line.LineStyle.Name
    ls_name_list.append(ls_name)
    # get ids of linestyles
    ls_id = line.LineStyle.Id
    ls_id_list.append(ls_id)
    # get creator of the line style
    ls_creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, ls_id).Creator 
    # create unique list
    if ls_name not in ls_name_u:
        ls_name_u.append(ls_name)
        ls_id_u.append(ls_id)
        ls_creators.append(ls_creator)

# for ls in line_style_collector:
#     print ls
#     if ls.Name not in ls_name_u:
#         ls_name_u.append(ls.Name)
#         ls_id_u.append(ls.Id)


scheduleData = []
# get a count for a line style
ls_counts = []
counter = 0
# creating a list of lists: name, count, ID, creator
for ls_name in ls_name_u:
    count_record = [ls_name, ls_name_list.count(ls_name), ls_id_u[counter], ls_creators[counter]]
    # count_record = [ls_name, ls_name_list.count(ls_name), ls_id_list[counter]]
    ls_counts.append(count_record)
    counter += 1

# setting the columns of the schedule
for i in ls_counts:
    line_style_name = i[0]
    # removing "<>" characters from line style names because of html compatibility
    line_style_name = line_style_name.replace('<', '&lt;')
    line_style_name = line_style_name.replace('>', '&gt;')

    line_style_count = i[1]
    line_style_id =  i[2]
    line_style_creator = i[3]
    # print line_style_name

    paramList = [line_style_name, output.linkify(line_style_id), line_style_count, line_style_creator]
    scheduleData.append(paramList)

    sortedScheduleData = sorted(scheduleData, reverse=True, key=lambda x: int(x[2]))

# print schedule if there are more than zero rows
try:
    output.print_table(table_data=sortedScheduleData,
                           title = "LineStyleUsage",
                           columns=["View Name", "Line Style ID", "Number of Elements", "Creator"],
                           formats=['', '', '', ''])
except:
    print("There are no line instances in this model.")