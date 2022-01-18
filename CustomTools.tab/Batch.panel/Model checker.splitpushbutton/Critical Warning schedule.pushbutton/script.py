# -*- coding: UTF-8 -*-
"""Warning Schedule.

Lists most Warnings related to architecural elements in the active model in Schedule with clickable Element Ids, Category of elements and Warning descritpions.

"""

__title__ = 'Critical Warning schedule'
__doc__ = 'Lists Warnings related to architecural elements in the active model in Schedule with clickable Element Ids, Category of elements and Warning descritpions.'

from pyrevit import revit, DB, coreutils, script, output, forms
from pyrevit.coreutils import Timer
from pyrevit.output import charts
from customOutput import criticalWarnings, hmsTimer, file_name_getter, colors, ct_icon

# from __future__ import division

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
timer = Timer()

allWarnings = doc.GetWarnings()

output = script.get_output()
# changing icon
ct_icon(output)
output.set_width(700)
output.print_md("# CRITICAL WARNINGS SCHEDULE")
output.print_md("### " + file_name_getter(doc))
output.freeze()

count = 0
cacheWarning = ""
cacheWarningType = ""
# for graph
graphHeadings = []
graphWarnData = []

for warning in allWarnings:
    elementsList=warning.GetFailingElements()
    description=warning.GetDescriptionText()
    # for warning type heading
    # Few warnings have mistakenly no dot in the end.
    try:
        descLen = description.index(".")
    except:
        descLen = len(description)
    # cutting long descriptions
    limit = 50
    if descLen < limit:
        descHeading = description[:descLen]
    # very long and repetetive descriptions
    elif description[:10] == "Mechanical" or description[:8] == "Hydronic":
        descHeading = description[:20] + "..."
    else:
        descHeading = description[:limit] + "..."

    # print descHeading
    if descHeading in criticalWarnings:
        count += 1

        print(coreutils.prepare_html_str("<hr>"))
        output.print_md("### " + str(count))
        print(description)

        for elemID in elementsList:
                # elem = doc.GetElement(elemID)
                # catName = elem.Category.Name
                try:
                    elem = doc.GetElement(elemID)
                    catName = elem.Category.Name
                except:
                    catName = "NA"

                newWarning= " \n " + output.linkify(elemID) + " \t " + catName + " \t "
                print(newWarning)

        # for graph headings
        if descHeading not in graphHeadings:
            graphHeadings.append(descHeading)
        # for graph warnings dataset
        graphWarnData.append(descHeading)
# graph Headings
warnSet=[]
for i in graphHeadings:
    count=graphWarnData.count(i)        
    warnSet.append(count)

output.unfreeze()


# CHART OUTPUT
output = script.get_output()

# chart = output.make_doughnut_chart()
chart = output.make_chart(version='2.8.0')
chart.type = charts.DOUGHNUT_CHART

chart.data.labels = graphHeadings
set_a = chart.data.new_dataset('Not Standard')
set_a.data = warnSet

set_a.backgroundColor = colors

# flexible chart size
# count of warning types
cat_count = len(graphHeadings)
# count of numbers in the legend
legend_len = len("".join(graphHeadings))
legend_metric = cat_count*10 + legend_len
if legend_metric < 450:
    chart.set_height(150)
elif legend_metric < 900:
    chart.set_height(200)
elif legend_metric < 1500:
    chart.set_height(250)
else:
    chart.set_height(300)

chart.draw()
# # for timing------
endtime = timer.get_time()
print(hmsTimer(endtime))